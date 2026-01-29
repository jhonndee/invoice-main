from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "phone",
            "company_name",
            "statut",
            "is_client",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_classes = (
            "w-full px-3 py-2 border rounded "
            "bg-white dark:bg-gray-700 "
            "text-gray-900 dark:text-white "
            "border-gray-300 dark:border-gray-600 "
            "focus:outline-none focus:ring-2 focus:ring-blue-500"
        )

        for field in self.fields.values():
            field.widget.attrs.update({"class": base_classes})

        self.fields["is_client"].widget = forms.HiddenInput()
        self.fields["statut"].required = True  # statut obligatoire
