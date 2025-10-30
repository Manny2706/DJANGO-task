from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
from .models import Post
from django.http import HttpRequest, HttpResponse


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ["title", "content"]
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


def create_post(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save()
			return redirect("post_detail", pk=post.pk)
	else:
		form = PostForm()
	return render(request, "posts/post_form.html", {"form": form, "is_create": True})


def update_post(request, pk: int):
	try:
		post = Post.objects.get(id=pk)
	except Post.DoesNotExist:
		raise Http404("Post not found")
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save()
			return redirect("post_detail", pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, "posts/post_form.html", {"form": form, "is_create": False, "post": post})


def delete_post(request, pk: int):
	try:
		post = Post.objects.get(id=pk)
	except Post.DoesNotExist:
		raise Http404("Post not found")
	if request.method == "POST":
		post.delete()
		return redirect("home")
	return render(request, "posts/post_confirm_delete.html", {"post": post})

