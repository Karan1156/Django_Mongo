from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from bson import ObjectId

from .models import Crud, User  # MongoEngine models


def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).first():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).first():
            messages.error(request, "Email already exists")
            return redirect("signup")

        user = User(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Registered Successfully! Please login.")
        return redirect("login")

    return render(request, "login_signup.html")


def log_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session["user_id"] = str(user.id)
            request.session["username"] = user.username
            messages.success(request, f"Welcome {user.username}!")
            return redirect("get_data")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "login_signup.html")


class get_data(View):
    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")

        tasks = Crud.objects.filter(user=user_id)
        return render(request, "index.html", {"tasks": tasks})

    def post(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")

        task = request.POST.get("task")
        crud = Crud(task=task, user=user_id)  # store user reference
        crud.save()
        return redirect("get_data")


def update(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    crud = Crud.objects.filter(user=user_id, id=ObjectId(id)).first()
    if not crud:
        messages.error(request, "Task not found")
        return redirect("get_data")

    if request.method == "POST":
        crud.task = request.POST.get("task")
        crud.save()
        return redirect("get_data")

    return render(request, "update.html", {"task": crud})


def delete(request, id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    crud = Crud.objects.filter(user=user_id, id=ObjectId(id)).first()
    if crud:
        crud.delete()

    return redirect("get_data")

def log_out(request):
    request.session.flush()
    return redirect(request,"login")
