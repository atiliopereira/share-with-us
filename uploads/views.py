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
            
            # Ensure media directory exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Save the file
            filename = default_storage.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            
            messages.success(request, f'File "{uploaded_file.name}" uploaded successfully!')
            return redirect('upload_file')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FileUploadForm()
    
    return render(request, 'uploads/upload.html', {'form': form})
