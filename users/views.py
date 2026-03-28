from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.views import account_sidebar_context
from .models import PlatformNotification, UserDocument, UserNotificationRead


@login_required
def documents_center(request):
    if request.method == "POST":
        doc_type = (request.POST.get("document_type") or "").strip()
        doc_file = request.FILES.get("document_file")
        if doc_type and doc_file:
            UserDocument.objects.create(
                user=request.user,
                document_type=doc_type,
                document_file=doc_file,
            )
            messages.success(request, "Document uploaded and sent for admin verification.")
        else:
            messages.error(request, "Please choose a document type and file.")
        return redirect("documents_center")

    documents = UserDocument.objects.filter(user=request.user)
    notifications = PlatformNotification.objects.filter(
        Q(recipient=request.user) | Q(recipient__isnull=True),
        is_active=True,
    ).order_by("-created_at")[:20]
    read_ids = set(
        UserNotificationRead.objects.filter(
            user=request.user,
            notification__in=notifications,
        ).values_list("notification_id", flat=True)
    )
    ctx = {
        "documents": documents,
        "notifications": notifications,
        "notification_read_ids": read_ids,
    }
    ctx.update(
        account_sidebar_context(
            request,
            "documents",
            topbar_title="Documents & verification",
            topbar_subtitle="Uploads & platform notices",
        )
    )
    return render(request, "download/document-verification.html", ctx)


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(PlatformNotification, id=notification_id, is_active=True)
    is_recipient = notification.recipient_id is None or notification.recipient_id == request.user.id
    if is_recipient:
        UserNotificationRead.objects.get_or_create(
            user=request.user,
            notification=notification,
        )
    return redirect("documents_center")
