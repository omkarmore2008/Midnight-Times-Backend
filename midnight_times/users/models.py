
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from django.db import models

class User(AbstractUser):
    """
    Default custom user model for Midnight Times.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for users detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Keyword(models.Model):
    keyword = models.CharField(_("Keyword"), max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    searched_at = models.DateTimeField(_("last_search At"), auto_now=True)
    last_record_final_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.keyword


class SearchResult(models.Model):
    keyword = models.OneToOneField(Keyword, related_name="articles", on_delete=models.CASCADE)
    articles_list = models.JSONField()

    def __str__(self):
        return str(self.pk)
