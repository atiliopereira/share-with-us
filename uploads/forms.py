from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-input",
                "accept": "*/*",
            }
        ),
        help_text="Tamaño Max: 500 MB",
    )

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            if file.size > 500 * 1024 * 1024:  # 500 MB limit
                raise forms.ValidationError("File size cannot exceed 500 MB.")
        return file
