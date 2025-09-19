from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-input",
                "accept": "*/*",
            }
        ),
        help_text="Tamaño Max: 200 MB",
    )

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            if file.size > 200 * 1024 * 1024:  # 200 MB limit
                raise forms.ValidationError("File size cannot exceed 200 MB.")
        return file
