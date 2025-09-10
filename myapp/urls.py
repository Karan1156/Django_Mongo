from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_data.as_view(), name="get_data"),
    path("update/<str:id>/", views.update, name="update"),
    path("delete/<str:id>/", views.delete, name="del"),
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
]
