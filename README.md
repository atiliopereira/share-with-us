# File Upload Web Application

A simple Django web application that allows anonymous users to upload files via a mobile-friendly web interface.

## Features

- **Simple file upload interface** - Clean, responsive design that works on desktop and mobile
- **Security features** - CSRF protection, file size limits (10MB), secure file handling
- **Anonymous uploads** - No user authentication required
- **Success feedback** - Visual confirmation when files are uploaded successfully

## Requirements

- Python 3.10+
- uv package manager

## Installation & Setup

### 1. Install Dependencies

```bash
# Install Django using uv
uv add Django==5.2.6
```

### 2. Run Database Migrations

```bash
# Apply initial database migrations
uv run python manage.py migrate
```

### 3. Start the Development Server

```bash
# Start the Django development server
uv run python manage.py runserver
```

### 4. Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Project Structure

```
share-with-us/
├── fileupload/             # Main Django project
│   ├── __init__.py
│   ├── settings.py         # Project settings with file upload config
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── uploads/                # Django app for file uploads
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # File upload form with validation
│   ├── models.py
│   ├── tests.py
│   ├── urls.py             # App URL configuration
│   ├── views.py            # Upload handling logic
│   └── templates/
│       └── uploads/
│           └── upload.html # Mobile-friendly upload interface
├── media/                  # Directory for uploaded files (created automatically)
├── manage.py               # Django management script
├── pyproject.toml          # uv project configuration
└── uv.lock                 # uv lock file
```

## Key Files Overview

### `fileupload/settings.py`
- Configures the Django project
- Sets up file upload limits (10MB)
- Configures media file handling
- Includes security settings with CSRF protection

### `uploads/forms.py`
- Defines the file upload form
- Includes file size validation
- Sets up proper HTML attributes for mobile compatibility

### `uploads/views.py`
- Handles file upload processing
- Manages file saving to the media directory
- Provides user feedback via Django messages

### `uploads/templates/uploads/upload.html`
- Responsive HTML template
- Mobile-first design with CSS Grid/Flexbox
- Success/error message display
- Clean, modern interface

## Configuration

### File Upload Settings

The following settings in `fileupload/settings.py` control file upload behavior:

```python
# Maximum file size: 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# File permissions
FILE_UPLOAD_PERMISSIONS = 0o644

# Media files location
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **File Size Validation**: Both client-side and server-side validation
- **Secure File Handling**: Uses Django's default storage backend
- **Input Sanitization**: Django's built-in form validation

## Usage

1. Navigate to the application URL
2. Click "Choose File" to select a file from your device
3. Click "Upload File" to submit
4. See success confirmation or error messages
5. Uploaded files are stored in the `media/` directory

## Mobile Compatibility

The application is designed to work seamlessly on mobile devices:

- Responsive design adapts to screen size
- Touch-friendly interface elements
- Optimized file selection for mobile browsers
- Clear visual feedback for all actions

## Customization

### Changing File Size Limits

Edit the values in `fileupload/settings.py`:

```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MB
```

And update the validation in `uploads/forms.py`:

```python
if file.size > 20 * 1024 * 1024:  # 20 MB limit
    raise forms.ValidationError('File size cannot exceed 20 MB.')
```

### Modifying the Interface

Edit `uploads/templates/uploads/upload.html` to customize:
- Colors and styling
- Layout and typography
- Success/error messages
- Form labels and help text

## Troubleshooting

### Common Issues

1. **"Permission denied" errors**
   - Ensure the `media/` directory is writable
   - Check file permissions on the project directory

2. **File uploads not working**
   - Verify `MEDIA_ROOT` and `MEDIA_URL` settings
   - Check that the `uploads` app is in `INSTALLED_APPS`

3. **Template not found**
   - Ensure the templates directory structure is correct
   - Verify `APP_DIRS = True` in `TEMPLATES` setting

### Development vs Production

This setup is configured for development. For production deployment:

1. Set `DEBUG = False`
2. Configure proper `ALLOWED_HOSTS`
3. Use a production-grade web server (not `runserver`)
4. Set up proper media file serving (nginx, CDN, etc.)
5. Configure database settings for production use
