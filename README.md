# File Upload Web Application

A simple Django web application that allows anonymous users to upload files via a mobile-friendly web interface.

## Features

- **Simple file upload interface** - Clean, responsive design that works on desktop and mobile
- **Security features** - CSRF protection, file size limits (200MB), secure file handling
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
- Sets up file upload limits (200MB)
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
# Maximum file size: 200 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024

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
FILE_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024  # 200 MB
```

And update the validation in `uploads/forms.py`:

```python
if file.size > 200 * 1024 * 1024:  # 200 MB limit
    raise forms.ValidationError('File size cannot exceed 200 MB.')
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

## AWS EC2 + S3 Deployment

### Prerequisites

1. **AWS S3 Bucket**: Create an S3 bucket for file storage
2. **AWS IAM User**: Create an IAM user with S3 permissions
3. **EC2 Instance**: Ubuntu server with Python 3.10+

### IAM Permissions Required

Create an IAM user with the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::your-bucket-name"
    }
  ]
}
```

### Server Setup

1. **Install Dependencies on EC2:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Clone repository
git clone https://github.com/your-repo/share-with-us.git
cd share-with-us
```

2. **Environment Configuration:**

Create `.env` file on the server:

```bash
# Django Configuration
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,ec2-18-221-73-203.us-east-2.compute.amazonaws.com

# AWS S3 Configuration
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-2
```

3. **Install and Run:**

```bash
# Install dependencies
uv add Django==5.2.6 boto3 django-storages python-decouple

# Run migrations
uv run python manage.py migrate

# Collect static files (if needed)
uv run python manage.py collectstatic --noinput

# Start server (for production, use gunicorn)
uv run python manage.py runserver 0.0.0.0:8000
```

### Production Web Server Setup

For production, install and configure Gunicorn + Nginx:

```bash
# Install Gunicorn
uv add gunicorn

# Create systemd service
sudo tee /etc/systemd/system/fileupload.service > /dev/null <<EOF
[Unit]
Description=Django File Upload App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/share-with-us
Environment="PATH=/home/ubuntu/share-with-us/.venv/bin"
ExecStart=/home/ubuntu/share-with-us/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 fileupload.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable fileupload
sudo systemctl start fileupload
```

### S3 Bucket Configuration

1. **Create S3 Bucket** with the name specified in your environment variables
2. **Configure CORS** (if needed for web uploads):

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "POST", "PUT"],
    "AllowedOrigins": [
      "https://ec2-18-221-73-203.us-east-2.compute.amazonaws.com"
    ],
    "ExposeHeaders": []
  }
]
```

3. **Block Public Access**: Keep enabled for security

### Security Considerations

- Files are stored with private ACL by default
- Pre-signed URLs are generated for file access with 1-hour expiration
- CSRF protection is enabled
- File size limits are enforced (200MB)

### Troubleshooting AWS Deployment

1. **S3 Access Issues**:
   - Verify IAM user has correct permissions
   - Check AWS credentials in environment variables
   - Ensure bucket name and region are correct

2. **File Upload Errors**:
   - Check Django logs: `sudo journalctl -u fileupload -f`
   - Verify S3 bucket policy and CORS configuration

3. **Static Files Issues**:
   - For production, consider separate S3 bucket for static files
   - Configure `STATIC_ROOT` and run `collectstatic`

### Development vs Production

**Development** (Local):

- `USE_S3=False` - Files stored locally
- `DEBUG=True`
- `ALLOWED_HOSTS=localhost,127.0.0.1`

**Production** (EC2 + S3):

- `USE_S3=True` - Files stored in S3
- `DEBUG=False`
- `ALLOWED_HOSTS=ec2-18-221-73-203.us-east-2.compute.amazonaws.com`
- Use Gunicorn + Nginx for serving
