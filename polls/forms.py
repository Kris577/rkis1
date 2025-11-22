from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django import forms
from .models import Question, Choice
from django.forms.models import inlineformset_factory

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    def save(self, commit=True):
        new_user = super().save(commit=False)
        new_user.set_password(self.cleaned_data.get("password"))
        if commit:
            new_user.save()
        return new_user

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get("password")
        pwd2 = self.cleaned_data.get("password2")
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError({"password2": ValidationError("Пароли должны совпадать", code="password_mismatch")})

    class Meta:
        model = CustomUser
        fields = ("avatar", "first_name", "last_name", "username", "email")

class UpdateForm(forms.ModelForm):
    avatar = forms.ImageField(label="Фото профиля", required=False)
    last_name = forms.CharField(label="Фамилия", required=False)
    first_name = forms.CharField(label="Имя", required=False)
    email = forms.CharField(label="Почта", required=False)
    username = forms.CharField(label="Логин", required=False)

    class Meta:
        model = CustomUser
        fields = ("avatar", "last_name","first_name", "email","username")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'short_description', 'description', 'image']
        labels = {
            'text': 'Вопрос',
            'short_description': 'Краткое описание',
            'description': 'Полное описание',
            'image': 'Изображение',
        }

ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=('choice_text',),
    extra=2,
    can_delete=True,
    labels={'choice_text': 'Вариант ответа'},
)