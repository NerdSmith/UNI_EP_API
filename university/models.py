from django.conf import settings
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from university.validators import CustomUnicodeUsernameValidator


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = CustomUnicodeUsernameValidator()
    username = models.CharField(
        _('Username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_('First name'), max_length=20, blank=True)
    last_name = models.CharField(_('Last name'), max_length=20, blank=True)
    patronymic = models.CharField(_('Patronymic'), max_length=20, blank=True)
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    GENDER_CHOICES = [
        ('m', "male"),
        ('f', "female"),
        ('o', 'other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='o')

    is_staff = models.BooleanField(
        _('Is stuff'),
        default=False,
        help_text=_(
            'Can access admin panel')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )

    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Curator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name='curator',
        blank=False, null=False)


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name='student',
        blank=False, null=False)
    group = models.ForeignKey(
        "Group",
        on_delete=models.DO_NOTHING,
        related_name='students',
        blank=False, null=False)


class EduDirection(models.Model):
    title = models.CharField(
        _("Direction title"),
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )

    curator = models.ForeignKey(
        "Curator",
        on_delete=models.DO_NOTHING,
        related_name='students',
        blank=True, null=True)

    def __str__(self):
        return self.title


class AcademicDiscipline(models.Model):
    title = models.CharField(
        _("Discipline title"),
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )

    direction = models.ForeignKey(
        "EduDirection",
        on_delete=models.CASCADE,
        related_name='disciplines',
        blank=False, null=False)

    def __str__(self):
        return self.title


class Group(models.Model):
    STUDENT_MAX_COUNT = 20

    course_number = models.IntegerField(_('Course number'), blank=False,
                                        validators=[MinValueValidator(1), MaxValueValidator(5)])
    group_number = models.CharField(_('Group number'), max_length=10, blank=False)
    EDUCATION_LEVELS = [
        ('b', "bachelor"),
        ('m', "magistracy"),
        ('p', "postgraduate"),
        ('s', "specialty")
    ]
    education_level = models.CharField(
        _('Edu level'),
        max_length=1, choices=EDUCATION_LEVELS, blank=True)

    direction = models.ForeignKey(EduDirection, on_delete=models.CASCADE, related_name='groups', blank=False,
                                  null=False)

    def __str__(self):
        return f"{self.course_number} course {self.group_number} group {dict(self.EDUCATION_LEVELS)[self.education_level]}"
