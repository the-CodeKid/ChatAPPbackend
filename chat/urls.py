from django.urls import path
from .views import upload_file
from chat.views import RegisterView

urlpatterns = [
    path('api/upload/', upload_file, name = "upload_file"),
    path('api/signup/', RegisterView.as_view(), name="register"),
]