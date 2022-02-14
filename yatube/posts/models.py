from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField("наименование группы", max_length=200)
    slug = models.SlugField("часть URL группы", unique=True)
    description = models.TextField("описание группы")

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("текст поста")
    pub_date = models.DateTimeField("дата публикации поста", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="автор поста"
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="наименование группы",
    )

    class Meta:
        ordering = (
            "-pub_date",
        )
        verbose_name = "пост"
        verbose_name_plural = "посты"

    def __str__(self):
        return self.text[:15]
