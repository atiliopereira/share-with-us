import os
import boto3
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from .forms import FileUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            
            # Save the file (works with both local storage and S3)
            filename = default_storage.save(uploaded_file.name, uploaded_file)
            
            # Only create local directory if not using S3
            if not getattr(settings, 'USE_S3', False):
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            messages.success(request, f'Archivo "{uploaded_file.name}" subido exitosamente!')
            return redirect('upload_file')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = FileUploadForm()
    
    return render(request, 'uploads/upload.html', {'form': form})


def gallery(request):
    file_urls = []
    try:
        if getattr(settings, 'USE_S3', False):
            # Use boto3 directly for S3
            session = boto3.Session(profile_name='grafiexpress')
            s3 = session.client('s3')
            response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='media/')

            if 'Contents' in response:
                for obj in response['Contents']:
                    # Skip test files and get filename from full path
                    filename = obj['Key'].replace('media/', '')
                    if filename and not filename.startswith('test'):
                        # Use filename only for URL generation since storage backend adds media/ prefix
                        file_url = default_storage.url(filename)
                        file_urls.append({'name': filename, 'url': file_url})
        else:
            # Local storage fallback
            dirs, files = default_storage.listdir('media')
            for file in files:
                if not file.startswith('test'):
                    file_path = f'media/{file}'
                    file_url = default_storage.url(file_path)
                    file_urls.append({'name': file, 'url': file_url})
    except Exception as e:
        print(f"Gallery error: {e}")
        file_urls = []

    return render(request, 'uploads/gallery.html', {'files': file_urls})
