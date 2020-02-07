from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    created_at = models.DateField(auto_now_add=True)
    nickname = models.CharField(max_length=20, default="User")
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    current_bookshelf = models.ForeignKey(
        "shelves.BookShelf", on_delete=models.CASCADE, null=True, blank=True
    )


#
# class SocialLoginUsers(models.Model):
#
#    """
#    Social Login Abstract based model
#    """
#
#    LOGIN_GITHUB = "github"
#    LOGIN_KAKAO = "kakao"
#    LOGIN_CHOICES = (
#        (LOGIN_GITHUB, "Github"),
#        (LOGIN_KAKAO, "Kakao"),
#    )
#    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES,)
#
#    class Meta:
#        abstract = True
#
#
# class KakaoUser(SocialLoginUsers):
#    user = models.ForeignKey(User, related_name="kakao", on_delete=models.CASCADE)
#    id_kakao = models.CharField(max_length=30)
#    kaccount_email = models.EmailField(
#        verbose_name="Kakao Login ID", null=True, blank=True
#    )
#    profile_image = models.ImageField(upload_to="kakao", blank=True)
#    thumbnail_image = models.ImageField(upload_to="kakao", blank=True)
#    nickname = models.CharField(max_length=100)
