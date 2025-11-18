from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
from .models import Post
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ["title", "content", "image"]
		widgets = {
			"title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
			"content": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Write your post..."}),
		}


def home(request):
	posts = Post.objects.order_by("-created_at")
	return render(request, "posts/home.html", {"posts": posts})




def post_detail(request, pk: int):
	try:
		post = Post.objects.get(id=pk)
	except Post.DoesNotExist:
		raise Http404("Post not found")
	return render(request, "posts/post_detail.html", {"post": post})


@login_required

def create_post(request):
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post: Post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect("post_detail", pk=post.pk)
	else:
		form = PostForm()
	return render(request, "posts/post_form.html", {"form": form, "is_create": True})


@login_required

def update_post(request, pk: int):
	try:
		post = Post.objects.get(id=pk)
	except Post.DoesNotExist:
		raise Http404("Post not found")
	if post.author != request.user:
		raise Http404("Not allowed")
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save()
			return redirect("post_detail", pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, "posts/post_form.html", {"form": form, "is_create": False, "post": post})


@login_required

def delete_post(request, pk: int):
	try:
		post = Post.objects.get(id=pk)
	except Post.DoesNotExist:
		raise Http404("Post not found")
	if post.author != request.user:
		raise Http404("Not allowed")
	if request.method == "POST":
		post.delete()
		return redirect("home")
	return render(request, "posts/post_confirm_delete.html", {"post": post})


# Auth: Signup, Login, Logout

def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "posts/signup.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm(request)
    return render(request, "posts/login.html", {"form": form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


# Contact form
class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Your message"}))


def contact_view(request: HttpRequest) -> HttpResponse:
    sent = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Send acknowledgement email to the user
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                subject = "Thanks for contacting us!"
                body = f"Hello {name},\n\nWe received your message and will get back to you soon.\n\nYour message:\n{message}\n\nBest,\nMini Blog"
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER, [email], fail_silently=True)
            sent = True
    else:
        form = ContactForm()
    return render(request, "posts/contact.html", {"form": form, "sent": sent})
