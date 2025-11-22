import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    last_name = models.CharField(max_length=254, verbose_name="Фамилия")
    first_name = models.CharField(max_length=254, verbose_name="Имя")
    email = models.EmailField(max_length=254, verbose_name="Почта", unique=True)
    username = models.CharField(max_length=254, verbose_name="Логин", unique=True)
    password = models.CharField(max_length=254, verbose_name="Пароль")
    avatar = models.ImageField(upload_to="polls/user", verbose_name="Фото профиля")
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Question(models.Model):
    text = models.CharField("Вопрос",max_length=250)
    pub_date = models.DateTimeField('Дата публикации')
    short_description = models.CharField("Краткое описание",max_length=450, null=True)
    description = models.CharField("Полное описание", max_length=1500, null=True)
    image = models.ImageField("Изображение", upload_to='polls/questions', blank=True)
    votes = models.IntegerField(default=0, blank=True)
    voted_by = models.ManyToManyField(CustomUser, related_name='voted_by', blank=True)

    def published_recently(self):
        recent_threshold = timezone.now() - datetime.timedelta(days=3)
        return self.pub_date >= recent_threshold

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Вариант ответа",max_length=200)
    votes = models.IntegerField("Голоса",default=0)

    def calculate_percent(self):
        if self.question.votes > 0:
            return round(self.votes * 100 / self.question.votes)
        return 0

    def __str__(self):
        return self.choice_text