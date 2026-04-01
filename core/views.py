from decimal import Decimal
import json
import mimetypes
from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.files.storage import default_storage
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.templatetags.static import static
from django.utils import timezone

from django.contrib.auth.models import User

from .models import Listing, ListingImage
from .ytr_media import normalize_image_url
from bookings.models import Booking
from messaging.models import Message
from users.models import UserProfile, is_user_verified

from .mail_utils import feedback_recipients, send_platform_mail

# Launch focus: commercial / fleet body styles first; other verticals marked "coming soon" in UI.
COMMERCIAL_BODY_STYLES = ("Commercial", "Van", "Truck", "Bakkie", "Fleet")


def _public_listings_qs():
    """Listings visible on home, browse, and search."""
    from .models import Listing

    return Listing.objects.filter(
        available=True,
        verification_status=Listing.VERIFICATION_APPROVED,
    )


def account_sidebar_context(request, sidebar_active="", *, topbar_title=None, topbar_subtitle=None):
    if not request.user.is_authenticated:
        return {}
    from users.models import PlatformNotification, UserNotificationRead

    all_user_notifications = PlatformNotification.objects.filter(
        Q(recipient=request.user) | Q(recipient__isnull=True),
        is_active=True,
    )
    read_notification_ids = UserNotificationRead.objects.filter(
        user=request.user,
        notification__in=all_user_notifications,
    ).values_list("notification_id", flat=True)
    unread_notifications = all_user_notifications.exclude(id__in=read_notification_ids).count()
    ctx = {
        "sidebar_active": sidebar_active,
        "sidebar_bookings_count": Booking.objects.filter(user=request.user).count(),
        "sidebar_message_count": Message.objects.filter(receiver=request.user, read=False).count(),
        "sidebar_notification_count": unread_notifications,
    }
    if topbar_title is not None:
        ctx["topbar_title"] = topbar_title
    if topbar_subtitle is not None:
        ctx["topbar_subtitle"] = topbar_subtitle
    return ctx


def home(request):
    base = _public_listings_qs().prefetch_related("images")
    commercial_list = list(
        base.filter(body_style__in=COMMERCIAL_BODY_STYLES).order_by("-created_at")[:8]
    )
    if len(commercial_list) < 4:
        ids = {x.id for x in commercial_list}
        rest = list(base.exclude(id__in=ids).order_by("-created_at")[: 8 - len(commercial_list)])
        featured_listings = commercial_list + rest
    else:
        featured_listings = commercial_list
    platform_stats = {
        "vehicles": _public_listings_qs().count(),
        "members": User.objects.filter(is_active=True).count(),
        "cities": _public_listings_qs().values("location").distinct().count(),
        "bookings": Booking.objects.count(),
    }
    return render(
        request,
        "download/index.html",
        {
            "featured_listings": featured_listings,
            "show_public_reviews": False,
            "platform_stats": platform_stats,
        },
    )


def about(request):
    return render(request, "download/about.html")


def how_it_works(request):
    return render(request, "download/howitworks.html")


def contact(request):
    if request.method == "POST":
        first_name = (request.POST.get("first_name") or "").strip()
        last_name = (request.POST.get("last_name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        subject = (request.POST.get("subject") or "General Inquiry").strip()
        body = (request.POST.get("message") or "").strip()

        if not email or not body:
            messages.error(request, "Please complete required fields.")
            return redirect("contact")

        ok, err = send_platform_mail(
            subject=f"[YTR Contact] {subject}",
            message=(
                f"From: {first_name} {last_name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n\n"
                f"Message:\n{body}\n"
            ),
            recipient_list=feedback_recipients(),
        )
        if ok:
            messages.success(request, "Message sent successfully. Our team will respond shortly.")
        else:
            messages.error(request, err or "Could not send message.")
        return redirect("contact")
    return render(request, "download/contact.html")


def feedback_page(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        subject = (request.POST.get("subject") or "Feedback").strip()
        user_type = (request.POST.get("user_type") or "").strip()
        rating = (request.POST.get("rating") or "").strip()
        body = (request.POST.get("message") or "").strip()

        if not email or not subject or not body:
            messages.error(request, "Please complete required fields.")
            return redirect("feedback")

        ok, err = send_platform_mail(
            subject=f"[YTR Feedback] {subject}",
            message=(
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"User Type: {user_type}\n"
                f"Rating: {rating}\n\n"
                f"Feedback:\n{body}\n"
            ),
            recipient_list=feedback_recipients(),
        )
        if ok:
            messages.success(request, "Thank you for your feedback.")
        else:
            messages.error(request, err or "Could not send feedback.")
        return redirect("feedback")

    return render(request, "download/feedback.html", {"show_public_reviews": False})


def services(request):
    return render(request, "download/services.html")


def newsletter_subscribe(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        if email:
            ok, err = send_platform_mail(
                subject="[YTR Newsletter] New subscription",
                message=f"New newsletter subscriber: {email}",
                recipient_list=feedback_recipients(),
            )
            if ok:
                messages.success(request, "Subscribed successfully.")
            else:
                messages.error(request, err or "Could not record subscription.")
    return redirect("home")


def listings_page(request):
    base_listings = _public_listings_qs()
    browse_total = base_listings.count()
    browse_style_counts = {}
    for row in base_listings.values("body_style").annotate(n=Count("id")):
        key = (row["body_style"] or "").strip() or "Other"
        browse_style_counts[key] = row["n"]

    commercial_focus = request.GET.get("commercial", "").strip() == "1"
    commercial_total = base_listings.filter(body_style__in=COMMERCIAL_BODY_STYLES).count()

    listings = base_listings
    if commercial_focus:
        listings = listings.filter(body_style__in=COMMERCIAL_BODY_STYLES)
    q = (request.GET.get("q") or "").strip()
    location = (request.GET.get("location") or "").strip()
    category = (request.GET.get("category") or "").strip()
    max_price = request.GET.get("max_price")
    min_price = request.GET.get("min_price")
    sort = (request.GET.get("sort") or "recommended").strip()
    style = (request.GET.get("style") or "").strip()
    if q:
        listings = listings.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(location__icontains=q)
        )
    if location:
        listings = listings.filter(location__icontains=location)
    if category in {"car", "tool", "equipment"}:
        listings = listings.filter(category=category)
    if min_price:
        try:
            listings = listings.filter(price_per_day__gte=Decimal(str(min_price)))
        except Exception:
            pass
    if max_price:
        try:
            listings = listings.filter(price_per_day__lte=Decimal(str(max_price)))
        except Exception:
            pass
    if style:
        listings = listings.filter(body_style__iexact=style)
    order_map = {
        "newest": "-created_at",
        "price_low": "price_per_day",
        "price_high": "-price_per_day",
        "recommended": "-created_at",
    }
    listings = (
        listings.order_by(order_map.get(sort, "-created_at")).prefetch_related("images")
    )

    paginator = Paginator(listings, 12)
    page = request.GET.get("page") or 1
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    query_params = request.GET.copy()
    if "page" in query_params:
        del query_params["page"]

    total_pages = paginator.num_pages
    cur = page_obj.number
    if total_pages <= 12:
        page_numbers = list(range(1, total_pages + 1))
    else:
        window = set(range(max(1, cur - 2), min(total_pages, cur + 2) + 1))
        window.update({1, 2, total_pages - 1, total_pages})
        page_numbers = sorted(x for x in window if 1 <= x <= total_pages)

    return render(
        request,
        "download/browse.html",
        {
            "listings": page_obj.object_list,
            "page_obj": page_obj,
            "paginator": paginator,
            "sort": sort,
            "style": style,
            "query_params": query_params,
            "page_numbers": page_numbers,
            "browse_total": browse_total,
            "browse_style_counts": browse_style_counts,
            "commercial_focus": commercial_focus,
            "commercial_total": commercial_total,
        },
    )


def listing_detail(request, listing_id):
    listing = get_object_or_404(
        Listing.objects.prefetch_related("images"),
        id=listing_id,
        available=True,
        verification_status=Listing.VERIFICATION_APPROVED,
    )
    related = (
        _public_listings_qs()
        .filter(category=listing.category)
        .exclude(id=listing.id)
        .order_by("-created_at")[:4]
    )
    if related.count() < 2:
        related = (
            _public_listings_qs()
            .exclude(id=listing.id)
            .order_by("-created_at")[:4]
        )
    return render(
        request,
        "download/vehicle-details.html",
        {"listing": listing, "related_listings": related},
    )


def listing_detail_fallback(request, *args, **kwargs):
    listing = _public_listings_qs().order_by("-created_at").first()
    if not listing:
        return redirect("browse")
    related = _public_listings_qs().exclude(id=listing.id).order_by("-created_at")[:4]
    return render(
        request,
        "download/vehicle-details.html",
        {"listing": listing, "related_listings": related},
    )


def search_listings(request):

    query = request.GET.get("q", "")

    results = _public_listings_qs().filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(location__icontains=query)
    )

    return render(request, "search_results.html", {
        "results": results,
        "query": query
    })


@login_required
def book_listing(request, listing_id):

    listing = get_object_or_404(
        Listing,
        id=listing_id,
        available=True,
        verification_status=Listing.VERIFICATION_APPROVED,
    )
    if listing.owner_id == request.user.id:
        messages.error(request, "You cannot book your own listing.")
        return redirect("listing_detail", listing_id=listing.id)
    if not request.user.is_staff and not is_user_verified(request.user):
        messages.error(request, "Please complete document verification before booking.")
        return redirect("documents_center")

    if request.method == "POST":

        start_raw = request.POST.get("start_date")
        end_raw = request.POST.get("end_date")
        try:
            start_date = datetime.strptime(start_raw, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_raw, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            messages.error(request, "Please choose valid start and end dates.")
            return redirect("book_listing", listing_id=listing.id)
        if end_date < start_date:
            messages.error(request, "Return date must be on or after pick-up date.")
            return redirect("book_listing", listing_id=listing.id)

        Booking.objects.create(
            listing=listing,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
        )
        messages.success(
            request,
            "Booking request submitted. The host will review it — check My Bookings for status.",
        )
        return redirect("my_bookings")

    host_label = listing.owner.get_full_name() or listing.owner.username
    return render(
        request,
        "book_listing.html",
        {"listing": listing, "host_label": host_label},
    )


@login_required
def owner_dashboard(request):
    today = timezone.now().date()

    listings = request.user.listings.all()

    bookings = Booking.objects.filter(
        listing__owner=request.user
    ).order_by("-created_at")

    inbox_messages = Message.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    sent_messages = Message.objects.filter(
        sender=request.user
    ).order_by("-created_at")

    # Placeholder analytics values for dashboard charts/cards.
    total_earnings = Decimal("0")
    earnings_by_month = [0] * 12
    for b in bookings:
        # If hourly exists use it when date range equals same day + times are added later.
        days = (b.end_date - b.start_date).days + 1
        days = max(days, 1)
        total_earnings += (b.listing.price_per_day or 0) * days
        earnings_by_month[b.start_date.month - 1] += int((b.listing.price_per_day or 0) * days)

    completed_count = sum(1 for b in bookings if b.approved and b.end_date < today)
    active_count = sum(1 for b in bookings if b.approved and b.end_date >= today)
    pending_count = sum(1 for b in bookings if not b.approved)
    cancelled_count = 0

    calendar_events = [
        {
            "title": f"{b.listing.title} ({'Booked' if b.approved else 'Pending'})",
            "start": b.start_date.isoformat(),
            "end": b.end_date.isoformat(),
            "backgroundColor": "#ffa500" if b.approved else "#6464ff",
            "borderColor": "#ffa500" if b.approved else "#6464ff",
        }
        for b in bookings[:30]
    ]

    recent_activity = []
    for b in bookings.order_by("-created_at")[:8]:
        recent_activity.append(
            {
                "icon": "calendar-check",
                "title": "Booking",
                "detail": f"{b.listing.title} · {b.start_date} – {b.end_date}",
                "time": b.created_at,
            }
        )
    for m in (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .select_related("listing", "sender", "receiver")
        .order_by("-created_at")[:8]
    ):
        other = m.receiver if m.sender_id == request.user.id else m.sender
        label = other.get_full_name() or other.username
        recent_activity.append(
            {
                "icon": "envelope",
                "title": "Message",
                "detail": f"{label} · {m.listing.title}",
                "time": m.created_at,
            }
        )
    recent_activity.sort(key=lambda x: x["time"], reverse=True)
    recent_activity = recent_activity[:12]

    ctx = {
        "listings": listings,
        "bookings": bookings,
        "recent_bookings": bookings[:4],
        "inbox_messages": inbox_messages,
        "sent_messages": sent_messages,
        "total_earnings": int(total_earnings),
        "listed_vehicles_count": listings.count(),
        "total_bookings": bookings.count(),
        "earnings_chart_values": json.dumps(earnings_by_month),
        "booking_status_counts": json.dumps([completed_count, active_count, pending_count, cancelled_count]),
        "calendar_events": json.dumps(calendar_events),
        "recent_activity": recent_activity,
    }
    ctx.update(
        account_sidebar_context(
            request,
            "dashboard",
            topbar_title="Dashboard",
            topbar_subtitle="Fleet overview & activity",
        )
    )
    return render(request, "dashboard.html", ctx)
@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, listing__owner=request.user)
    booking.approved = True
    booking.save()
    return redirect('owner_dashboard')


def _decimal(val, default="0"):
    try:
        return Decimal(str(val if val not in (None, "") else default))
    except Exception:
        return Decimal(default)


def _body_style_from_vehicle_type(raw: str) -> str:
    raw = (raw or "").strip().lower()
    mapping = {
        "sedan": "Sedan",
        "suv": "SUV",
        "hatchback": "Hatchback",
        "coupe": "Coupe",
        "convertible": "Convertible",
        "pickup": "Bakkie",
        "van": "Van",
        "wagon": "Wagon",
    }
    return mapping.get(raw, raw.replace("-", " ").title() if raw else "Sedan")


@login_required
def add_listing(request):
    require_docs = getattr(settings, "YTR_REQUIRE_VERIFICATION_TO_LIST", True)
    if require_docs and not request.user.is_staff and not is_user_verified(request.user):
        messages.error(request, "Please complete document verification before listing your vehicle.")
        return redirect("documents_center")

    if request.method == "POST":
        make = (request.POST.get("make") or "").strip()
        model_name = (request.POST.get("model") or "").strip()
        year = (request.POST.get("year") or "").strip()
        title = (request.POST.get("title") or "").strip()
        if not title:
            title = f"{make} {model_name}".strip() or "Untitled listing"
        if year:
            title = f"{title} ({year})".strip()

        base_desc = (request.POST.get("description") or "").strip()
        feature_vals = request.POST.getlist("features")
        features_line = ", ".join(feature_vals) if feature_vals else ""
        if base_desc:
            description = base_desc
            if features_line:
                description = f"{description}\n\nFeatures: {features_line}"
        else:
            description = (
                f"{make} {model_name} ({year}) listed on Yours To Rent."
                + (f"\n\nFeatures: {features_line}" if features_line else "")
            )

        raw_category = (request.POST.get("category") or "car").strip().lower()
        category = raw_category if raw_category in {"car", "tool", "equipment"} else "car"

        vtype = (request.POST.get("type") or "").strip().lower()
        transmission = (request.POST.get("transmission") or "").strip().title() or "Automatic"
        fuel_raw = (request.POST.get("fuel") or "").strip().lower()
        fuel_map = {
            "petrol": "Petrol",
            "diesel": "Diesel",
            "hybrid": "Hybrid",
            "electric": "Electric",
        }
        fuel_type = fuel_map.get(fuel_raw, fuel_raw.title() or "Petrol")

        seats_raw = request.POST.get("seats") or "5"
        try:
            seats = int(str(seats_raw).replace("+", "").split()[0])
        except (ValueError, IndexError):
            seats = 5
        seats = max(1, min(seats, 16))

        mileage_raw = request.POST.get("mileage") or "0"
        try:
            mileage_km = int(mileage_raw)
        except ValueError:
            mileage_km = 0
        mileage_km = max(0, mileage_km)

        price_day = request.POST.get("price_day") or request.POST.get("daily_rate")
        price_hour = request.POST.get("price_hour")
        location = (request.POST.get("location") or request.POST.get("city") or "").strip() or "South Africa"

        listing = Listing.objects.create(
            owner=request.user,
            title=title[:255],
            description=description,
            category=category,
            price_per_day=_decimal(price_day, "0"),
            price_per_hour=_decimal(price_hour, "0") if (price_hour not in (None, "")) else None,
            location=location[:255],
            body_style=_body_style_from_vehicle_type(vtype),
            transmission=transmission[:32],
            fuel_type=fuel_type[:32],
            seats=seats,
            mileage_km=mileage_km,
            verification_status=Listing.VERIFICATION_APPROVED,
        )

        files = request.FILES.getlist("images")
        for f in files[:20]:
            ListingImage.objects.create(listing=listing, image=f)

        if files:
            listing.refresh_from_db()
            first_img = listing.images.order_by("uploaded_at").first()
            if first_img and first_img.image:
                url = normalize_image_url(first_img.image.url)
                if url and len(url) <= 500:
                    listing.hero_image_url = url
                    listing.save(update_fields=["hero_image_url"])

        messages.success(request, "Vehicle listing submitted successfully.")
        return redirect("owner_dashboard")

    return render(request, "download/list-vehicle.html")


@login_required
def edit_listing(request, listing_id):

    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)

    if request.method == "POST":

        listing.title = request.POST.get("title")
        listing.description = request.POST.get("description")
        listing.category = request.POST.get("category")
        listing.price_per_day = request.POST.get("price_day") or 0
        listing.price_per_hour = request.POST.get("price_hour") or None
        listing.location = request.POST.get("location")

        listing.save()

        return redirect("owner_dashboard")

    return render(request, "edit_listing.html", {"listing": listing})


@login_required
def delete_listing(request, listing_id):

    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)

    listing.delete()

    return redirect("owner_dashboard")


@login_required
def profile_page(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", request.user.first_name).strip()
        request.user.last_name = request.POST.get("last_name", request.user.last_name).strip()
        request.user.email = request.POST.get("email", request.user.email).strip()
        request.user.save()
        profile.phone = (request.POST.get("phone") or "").strip()
        profile.bio = (request.POST.get("bio") or "").strip()
        if request.FILES.get("avatar"):
            profile.avatar = request.FILES["avatar"]
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")
    ctx = {
        "profile": profile,
        "user_verified": is_user_verified(request.user),
    }
    ctx.update(
        account_sidebar_context(
            request,
            "profile",
            topbar_title="Profile",
            topbar_subtitle="Your public details & avatar",
        )
    )
    return render(request, "download/profile.html", ctx)


@login_required
def settings_page(request):
    if request.method == "POST":
        new_password = (request.POST.get("new_password") or "").strip()
        confirm_password = (request.POST.get("confirm_password") or "").strip()
        if new_password and new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password updated. Please log in again.")
            return redirect("login")
        if new_password or confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            messages.success(request, "Settings saved.")
        return redirect("settings")
    ctx = {}
    ctx.update(
        account_sidebar_context(
            request,
            "settings",
            topbar_title="Settings",
            topbar_subtitle="Security & preferences",
        )
    )
    return render(request, "download/settings.html", ctx)


@login_required
def my_bookings_page(request):
    renter_bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("listing", "listing__owner")
        .order_by("-created_at")
    )
    today = timezone.now().date()
    booking_rows = []
    total_spend = 0
    active_count = 0
    pending_count = 0
    completed_count = 0
    next_trip_date = None
    for b in renter_bookings:
        days = max((b.end_date - b.start_date).days + 1, 1)
        total = (b.listing.price_per_day or Decimal("0")) * days
        if not b.approved:
            status = "upcoming"
            status_label = "Pending"
            pending_count += 1
        elif b.end_date < today:
            status = "completed"
            status_label = "Completed"
            completed_count += 1
        elif b.start_date > today:
            status = "upcoming"
            status_label = "Confirmed"
            if next_trip_date is None or b.start_date < next_trip_date:
                next_trip_date = b.start_date
        else:
            status = "active"
            status_label = "In progress"
            active_count += 1
        total_spend += int(total)
        booking_rows.append(
            {
                "booking": b,
                "days": days,
                "total": int(total),
                "status": status,
                "status_label": status_label,
            }
        )
    ctx = {
        "booking_rows": booking_rows,
        "today": today,
        "booking_summary": {
            "total": len(booking_rows),
            "active": active_count,
            "pending": pending_count,
            "completed": completed_count,
            "total_spend": total_spend,
            "next_trip_date": next_trip_date,
        },
        "hero_title": 'My <span class="text-warning">Bookings</span>',
        "hero_subtitle": "Pending and confirmed trips tied to your account — no demo history.",
    }
    ctx.update(
        account_sidebar_context(
            request,
            "bookings",
            topbar_title="My bookings",
            topbar_subtitle="Trips and rental history",
        )
    )
    return render(request, "download/my-bookings.html", ctx)


@login_required
def my_vehicles_page(request):
    my_listings = request.user.listings.all().order_by("-created_at")
    ctx = {"my_listings": my_listings}
    ctx.update(
        account_sidebar_context(
            request,
            "vehicles",
            topbar_title="My vehicles",
            topbar_subtitle="Listings you host",
        )
    )
    return render(request, "download/my-vehicles.html", ctx)


def _owner_earnings_data(request):
    bookings = Booking.objects.filter(listing__owner=request.user).order_by("-created_at")
    total_earnings = Decimal("0")
    earnings_by_month = [0] * 12
    for b in bookings:
        days = max((b.end_date - b.start_date).days + 1, 1)
        amt = (b.listing.price_per_day or Decimal("0")) * days
        total_earnings += amt
        earnings_by_month[b.start_date.month - 1] += int(amt)
    return int(total_earnings), json.dumps(earnings_by_month)


@login_required
def earnings_page(request):
    total_earnings, earnings_chart_values = _owner_earnings_data(request)
    ctx = {
        "total_earnings": total_earnings,
        "earnings_chart_values": earnings_chart_values,
    }
    ctx.update(
        account_sidebar_context(
            request,
            "earnings",
            topbar_title="Earnings",
            topbar_subtitle="Revenue from your listings",
        )
    )
    return render(request, "download/earnings.html", ctx)


@login_required
def transactions_page(request):
    owner_rows = []
    for b in (
        Booking.objects.filter(listing__owner=request.user)
        .select_related("listing", "user")
        .order_by("-created_at")[:200]
    ):
        days = max((b.end_date - b.start_date).days + 1, 1)
        amt = (b.listing.price_per_day or Decimal("0")) * days
        owner_rows.append(
            {
                "date": b.created_at,
                "label": f"Booking — {b.listing.title}",
                "detail": f"Renter: {b.user.get_full_name() or b.user.username}",
                "amount": int(amt),
                "status": "Completed" if b.approved else "Pending",
                "ref": f"BK-{b.id}",
            }
        )
    renter_rows = []
    for b in (
        Booking.objects.filter(user=request.user)
        .select_related("listing", "listing__owner")
        .order_by("-created_at")[:200]
    ):
        days = max((b.end_date - b.start_date).days + 1, 1)
        amt = (b.listing.price_per_day or Decimal("0")) * days
        renter_rows.append(
            {
                "date": b.created_at,
                "label": f"Booking — {b.listing.title}",
                "detail": f"Host: {b.listing.owner.get_full_name() or b.listing.owner.username}",
                "amount": int(amt),
                "status": "Completed" if b.approved else "Pending",
                "ref": f"BK-{b.id}",
            }
        )
    ctx = {
        "owner_transactions": owner_rows,
        "renter_transactions": renter_rows,
    }
    ctx.update(
        account_sidebar_context(
            request,
            "transactions",
            topbar_title="Transactions",
            topbar_subtitle="Host & renter activity",
        )
    )
    return render(request, "download/transactions.html", ctx)


@login_required
def payouts_page(request):
    ctx = {"payouts_live": False}
    ctx.update(
        account_sidebar_context(
            request,
            "payouts",
            topbar_title="Payouts",
            topbar_subtitle="Bank & payout preferences",
        )
    )
    return render(request, "download/payouts.html", ctx)


@login_required
def help_center_page(request):
    ctx = {}
    ctx.update(
        account_sidebar_context(
            request,
            "help",
            topbar_title="Help center",
            topbar_subtitle="Guides & support",
        )
    )
    return render(request, "download/help-center.html", ctx)


def faq_page(request):
    return render(request, "download/faq.html")


def fleet_solutions(request):
    """Enterprise & fleet — alternative procurement model to traditional leasing."""
    return render(request, "solutions/fleet.html")


def mobility_hub(request):
    """Mobility hub — drivers, operators, and on-demand fleet narrative."""
    return render(request, "solutions/mobility.html")


def dispatch_console(request):
    """Dispatch-focused page for ops teams coordinating multiple vehicles."""
    return render(request, "solutions/dispatch.html")


def partner_network(request):
    """Partner ecosystem page for insurers, workshops, and enterprise operators."""
    return render(request, "solutions/partners.html")


def trust_center(request):
    """Trust, verification, and safety overview for enterprise and retail users."""
    return render(request, "solutions/trust-center.html")


def media_with_fallback(request, path):
    """
    Serve MEDIA files when available, with safe fallback images when files are missing.
    Helps keep avatars/listing photos visible on hosts with ephemeral disks.
    """
    rel_path = (path or "").lstrip("/")
    try:
        if rel_path and default_storage.exists(rel_path):
            f = default_storage.open(rel_path, "rb")
            ctype, _ = mimetypes.guess_type(rel_path)
            return FileResponse(f, content_type=ctype or "application/octet-stream")
    except Exception:
        pass

    if rel_path.startswith("profile_avatars/"):
        return redirect(static("images/ytr-logo-reference.svg"))
    return redirect(
        getattr(
            settings,
            "YTR_DEFAULT_VEHICLE_IMAGE_URL",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=900&q=80",
        )
    )