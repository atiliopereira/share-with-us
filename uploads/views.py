import os
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
