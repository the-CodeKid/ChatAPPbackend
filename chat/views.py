from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage


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
    