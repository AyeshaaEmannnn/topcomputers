from django import forms
from .models import StoredFile, FileComment, Contact

class StoredFileForm(forms.ModelForm):
    class Meta:
        model = StoredFile
        fields = ["title", "description", "file"]


class FileCommentForm(forms.ModelForm):
    class Meta:
        model = FileComment
        fields = ["comment_text"]
        widgets = {
            "comment_text": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Add a comment...",
                "class": "w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"
            })
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = FileComment
        fields = ["comment_text"]
        widgets = {
            "comment_text": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Write a reply...",
                "class": "w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"
            })
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name", "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your Email", "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject", "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"}),
            "message": forms.Textarea(attrs={"placeholder": "Your Message", "rows": 5, "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"})
        }
