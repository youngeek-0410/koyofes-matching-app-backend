from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModelMixin
from .department import Department
from .sex import Sex


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a user with the given username, email, and
        password."""
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModelMixin):
    objects = UserManager()

    MAX_LENGTH_EMAIL = 30
    email = models.EmailField(_("email address"), unique=True)
    MIN_LENGTH_USERNAME = 1
    MAX_LENGTH_USERNAME = 15
    username = models.CharField(
        _("username"),
        max_length=MAX_LENGTH_USERNAME,
    )

    # optional user info
    department = models.CharField(
        _("department"), blank=True, choices=Department.choices(), max_length=20
    )
    grade = models.PositiveSmallIntegerField(
        _("grade"),
        blank=True,
        null=True,
    )
    sex = models.CharField(_("sex"), blank=True, choices=Sex.choices(), max_length=20)
    # profile_image
    MAX_LENGTH_DESCRIPTION = 200
    description = models.CharField(
        _("description"), blank=True, max_length=MAX_LENGTH_DESCRIPTION
    )

    # management info
    is_banned = models.BooleanField(
        _("is banned"),
        default=False,
    )

    # permissions
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def images(self):
        return UserImage.objects.filter(user=self)


def upload_to(instance, filename):
    local_part, _ = instance.user.email.split("@")
    return f"user/{local_part}/{filename}"


class UserImage(BaseModelMixin):
    user = models.ForeignKey(
        "matching.User",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=upload_to,
    )

    class Meta:
        verbose_name = _("user image")
        verbose_name_plural = _("user images")

    def __str__(self):
        return self.image.url
