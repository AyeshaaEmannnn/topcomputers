from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import StoredFile, FileComment, Contact
from .forms import (
    StoredFileForm,
    FileCommentForm,
    CommentReplyForm,
    ContactForm
)
from .serializers import StoredFileSerializer
from .utils import get_files_with_signed_urls


# =========================
# HOME PAGE
# =========================
@login_required(login_url='login_page')
def home_view(request):
    if request.method == "POST":
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Only admins can upload files."},
                status=403
            )

        form = StoredFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "File uploaded successfully!")
            return redirect("/home/")
        else:
            messages.error(request, "Failed to upload file.")
    else:
        form = StoredFileForm()

    contact_form = ContactForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "contact_form": contact_form,
        }
    )


# =========================
# WASABI FILES API (SIGNED URLS)
# =========================
def get_files_api(request):
    try:
        files = get_files_with_signed_urls(
            prefix="products/",
            expires_in=3600
        )
        return JsonResponse({"files": files}, safe=False)
    except Exception as e:
        return JsonResponse(
            {"files": [], "error": str(e)},
            status=500
        )


# =========================
# DRF API (OPTIONAL)
# =========================
class StoredFileListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        files = StoredFile.objects.all().order_by('-uploaded_at')
        serializer = StoredFileSerializer(
            files,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admins can upload files."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StoredFileSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "File uploaded successfully!", "file": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# LIKE FILE
# =========================
@login_required(login_url='login_page')
def like_file(request, file_id):
    file_obj = get_object_or_404(StoredFile, id=file_id)

    if request.user in file_obj.liked_by.all():
        file_obj.liked_by.remove(request.user)
        file_obj.likes_count -= 1
    else:
        file_obj.liked_by.add(request.user)
        file_obj.likes_count += 1

    file_obj.save()

    return JsonResponse({
        "success": True,
        "likes_count": file_obj.likes_count,
        "liked": request.user in file_obj.liked_by.all()
    })


# =========================
# ADD COMMENT
# =========================
@login_required(login_url='login_page')
def add_comment(request, file_id):
    file_obj = get_object_or_404(StoredFile, id=file_id)

    if request.method == "POST":
        form = FileCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.file = file_obj
            comment.user = request.user
            parent_id = request.POST.get("parent_id")
            if parent_id:
                try:
                    comment.parent_comment_id = int(parent_id)
                except ValueError:
                    comment.parent_comment = None
            comment.save()
            messages.success(request, "Comment added successfully!")

    return redirect("file_detail", file_id=file_obj.id)


# =========================
# FILE DETAIL
# =========================
@login_required(login_url='login_page')
def file_detail(request, file_id):
    file_obj = get_object_or_404(StoredFile, id=file_id)
    comments = file_obj.comments.filter(
        parent_comment__isnull=True
    ).order_by('-created_at')

    comment_form = FileCommentForm()
    user_liked = request.user in file_obj.liked_by.all()

    return render(
        request,
        "file.html",
        {
            "file": file_obj,
            "comments": comments,
            "comment_form": comment_form,
            "user_liked": user_liked,
        }
    )


# =========================
# CONTACT FORM
# =========================
def contact_submit(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            name = contact.name
            email = contact.email
            subject = contact.subject
            message = contact.message
            phone = request.POST.get("phone", "").strip()

            full_message = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone or '-'}\n\n"
                f"Message:\n{message}"
            )

            to_email = getattr(settings, "CONTACT_TO_EMAIL", None) or "itxsash19@gmail.com"
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or email

            try:
                send_mail(
                    subject=subject,
                    message=full_message,
                    from_email=from_email,
                    recipient_list=[to_email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    "Thank you! Your message was sent successfully."
                )
            except Exception:
                messages.error(
                    request,
                    "Saved, but email could not be sent. Please check email settings."
                )
        else:
            messages.error(request, "Please fill all fields correctly.")

        # Stay on the same page (no redirect)
        return render(
            request,
            "home.html",
            {
                "form": StoredFileForm(),
                "contact_form": ContactForm(),
            },
        )

    return redirect("/home/")
