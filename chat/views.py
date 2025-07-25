from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"error":"Username already exists."}, status=400)
        try:
            validate_password(data["password"])
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        user = User.objects.create_user(
            username=data["username"],
            email=data["email",''],
            password=data["password"]
        )
        return Response({"success": "User created!"}, status=201)


@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        filename = default_storage.save(request.FILES["file"].name, request.FILES["file"])
        url = request.build_absolute_uri(settings.MEDIA_URL + filename)
        return JsonResponse({
            "file_url": url,
            "file_name": request.FILES["file"].name
        })
    return JsonResponse({"error": "No file uploaded."}, status = 400)
    