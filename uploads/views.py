import os

import boto3
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render

from .forms import FileUploadForm


def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data["file"]

            # Save the file (works with both local storage and S3)
            filename = default_storage.save(uploaded_file.name, uploaded_file)

            # Only create local directory if not using S3
            if not getattr(settings, "USE_S3", False):
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            messages.success(
                request,
                f'Archivo "{uploaded_file.name}" subido exitosamente! gracias por compartir!',
            )
            return redirect("upload_file")
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = FileUploadForm()

    return render(request, "uploads/upload.html", {"form": form})


def gallery(request):
    file_urls = []
    try:
        if getattr(settings, "USE_S3", False):
            # Use boto3 directly for S3
            session = boto3.Session(profile_name="grafiexpress")
            s3 = session.client("s3")
            response = s3.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="media/"
            )

            if "Contents" in response:
                # Sort by LastModified in descending order (newest first)
                sorted_objects = sorted(
                    response["Contents"], key=lambda x: x["LastModified"], reverse=True
                )
                for obj in sorted_objects:
                    # Skip test files and get filename from full path
                    filename = obj["Key"].replace("media/", "")
                    if filename and not filename.startswith("test"):
                        # Use filename only for URL generation since storage backend adds media/ prefix
                        file_url = default_storage.url(filename)
                        file_urls.append({"name": filename, "url": file_url})
        else:
            # Local storage fallback
            dirs, files = default_storage.listdir("media")
            files_with_time = []
            for file in files:
                if not file.startswith("test"):
                    file_path = f"media/{file}"
                    # Get file modification time
                    file_full_path = default_storage.path(file_path)
                    mod_time = os.path.getmtime(file_full_path)
                    file_url = default_storage.url(file_path)
                    files_with_time.append(
                        {"name": file, "url": file_url, "mod_time": mod_time}
                    )

            # Sort by modification time in descending order (newest first)
            files_with_time.sort(key=lambda x: x["mod_time"], reverse=True)
            file_urls = [{"name": f["name"], "url": f["url"]} for f in files_with_time]
    except Exception as e:
        print(f"Gallery error: {e}")
        file_urls = []

    return render(request, "uploads/gallery.html", {"files": file_urls})
