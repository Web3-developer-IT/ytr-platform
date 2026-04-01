from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.models import Listing
from core.views import account_sidebar_context
from users.models import UserProfile
from .models import Message


def _build_threads(user):
    qs = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .select_related("listing", "sender", "receiver")
        .order_by("-created_at")[:400]
    )
    threads = []
    seen = set()
    for m in qs:
        other = m.receiver if m.sender_id == user.id else m.sender
        key = (m.listing_id, other.id)
        if key in seen:
            continue
        seen.add(key)
        unread = Message.objects.filter(
            receiver=user,
            sender=other,
            listing_id=m.listing_id,
            read=False,
        ).count()
        other_profile, _ = UserProfile.objects.get_or_create(user=other)
        threads.append(
            {
                "listing": m.listing,
                "other": other,
                "other_profile": other_profile,
                "last_message": m,
                "unread_count": unread,
            }
        )
    return threads


def _pair_has_messages(user, listing, other):
    return Message.objects.filter(
        listing=listing,
        sender__in=[user, other],
        receiver__in=[user, other],
    ).exists()


@login_required
def inbox(request):
    if request.method == "POST":
        listing_id = (request.POST.get("listing_id") or "").strip()
        other_id = (request.POST.get("other_user_id") or "").strip()
        content = (request.POST.get("content") or "").strip()
        if not listing_id or not other_id:
            return redirect("inbox")
        listing = get_object_or_404(Listing, id=listing_id)
        other = get_object_or_404(User, id=other_id)
        if other.id == request.user.id:
            return redirect("inbox")
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other,
                listing=listing,
                content=content,
            )
        return redirect(f"{reverse('inbox')}?listing={listing_id}&user={other_id}")

    threads = _build_threads(request.user)
    listing_id = request.GET.get("listing")
    other_id = request.GET.get("user")

    active_listing = None
    active_other = None
    active_other_profile = None
    active_messages = []

    if listing_id and other_id:
        active_listing = Listing.objects.filter(id=listing_id).first()
        active_other = User.objects.filter(id=other_id).first()
        if not active_listing or not active_other:
            active_listing = None
            active_other = None
        # Never open a conversation with yourself.
        if active_other and active_other.id == request.user.id:
            active_listing = None
            active_other = None
        elif active_listing and active_other:
            active_other_profile, _ = UserProfile.objects.get_or_create(user=active_other)
            active_messages = list(
                Message.objects.filter(
                    listing=active_listing,
                    sender__in=[request.user, active_other],
                    receiver__in=[request.user, active_other],
                ).order_by("created_at")
            )
            for m in active_messages:
                m.sender_profile, _ = UserProfile.objects.get_or_create(user=m.sender)
            Message.objects.filter(
                receiver=request.user,
                sender=active_other,
                listing=active_listing,
                read=False,
            ).update(read=True)
    elif threads:
        # Default to latest existing thread if no explicit target was requested.
        if not active_listing or not active_other:
            active_listing = threads[0]["listing"]
            active_other = threads[0]["other"]
        active_other_profile, _ = UserProfile.objects.get_or_create(user=active_other)
        active_messages = list(
            Message.objects.filter(
                listing=active_listing,
                sender__in=[request.user, active_other],
                receiver__in=[request.user, active_other],
            ).order_by("created_at")
        )
        for m in active_messages:
            m.sender_profile, _ = UserProfile.objects.get_or_create(user=m.sender)

        Message.objects.filter(
            receiver=request.user,
            sender=active_other,
            listing=active_listing,
            read=False,
        ).update(read=True)

    ctx = {
        "threads": threads,
        "active_listing": active_listing,
        "active_other": active_other,
        "active_other_profile": active_other_profile,
        "active_messages": active_messages,
    }
    ctx.update(
        account_sidebar_context(
            request,
            "messages",
            topbar_title="Messages",
            topbar_subtitle="Inbox & threads",
        )
    )
    return render(request, "download/messages.html", ctx)


@login_required
def conversation(request, listing_id, user_id):
    if request.user.id == user_id:
        messages.warning(request, "You cannot open a conversation with yourself.")
        return redirect("inbox")
    listing = Listing.objects.filter(id=listing_id).first()
    if not listing:
        messages.error(request, "That listing no longer exists.")
        return redirect("inbox")
    return redirect(f"{reverse('inbox')}?listing={listing_id}&user={user_id}")
