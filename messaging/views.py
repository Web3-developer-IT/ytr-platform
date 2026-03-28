from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
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
        listing_id = request.POST.get("listing_id")
        other_id = request.POST.get("other_user_id")
        content = (request.POST.get("content") or "").strip()
        listing = get_object_or_404(Listing, id=listing_id)
        other = get_object_or_404(User, id=other_id)
        if content and other.id != request.user.id:
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

    if threads:
        if listing_id and other_id:
            active_listing = get_object_or_404(Listing, id=listing_id)
            active_other = get_object_or_404(User, id=other_id)
            if not _pair_has_messages(request.user, active_listing, active_other):
                active_listing = threads[0]["listing"]
                active_other = threads[0]["other"]
        else:
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
    return redirect(f"{reverse('inbox')}?listing={listing_id}&user={user_id}")
