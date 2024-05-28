from django.db import models
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'users'

    # for management
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    # basic information
    email = models.EmailField("email address", blank=False, null=False, unique=True)
    phone_number = models.CharField('phone number', max_length=10, blank=True, null=True)

    first_name = models.CharField("first name", max_length=150, blank=False, null=False)
    last_name = models.CharField("last name", max_length=150, blank=False, null=False)

    date_joined = models.DateTimeField("date joined", null=True, blank=True)
    date_left = models.DateTimeField("date left", null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Addresses(models.Model):
    user_object = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    address1 = models.CharField('adress1', help_text='Street address or P.O. Box', max_length=255, null=False, blank=False)
    address2 = models.CharField('adress2', help_text='(Optional) Apt, Suite, Unit, Building', max_length=255, null=True, blank=True)
    city = models.CharField('city', max_length=255, null=False, blank=False)
    postal_code = models.CharField('postal code', max_length=255, null=False, blank=False)
    province = models.CharField('province', max_length=255, null=False, blank=False)


class EmployeeTypes(models.Model):
    type = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.type


class EmployeeInformations(models.Model):
    WAGE_BASE_CHOICES = [
        (0, 'hour'), (1, 'month'), (2, 'year')
    ]

    def only_int(value): 
        if value.isdigit()==False:
            raise ValidationError('Only number is allowed')

    user_object = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    institution_number = models.CharField('institution number', max_length=3, blank=False, null=False, validators=[only_int])
    transit_number = models.CharField('transit number', max_length=5, blank=False, null=False, validators=[only_int])
    account_number = models.CharField('account number', max_length=7, blank=False, null=False, validators=[only_int])
    sin_number = models.CharField('sin number', max_length=9, blank=False, null=False, validators=[only_int])
    wage = models.FloatField('wage', null=True, blank=True)
    wage_is_based_on = models.IntegerField(choices=WAGE_BASE_CHOICES, null=True, blank=True)
    employee_type_object = models.ForeignKey(EmployeeTypes, on_delete=models.SET_NULL, null=True, blank=True)


class Images(models.Model):
    user_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    image_name = models.CharField('image name', max_length=255, null=False, blank=False)
    image = models.ImageField('image', upload_to='user_images/', null=False, blank=False)


class Notes(models.Model):
    user_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_notes_user')
    editor_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_notes_editor')
    note = models.TextField(null=False, blank=False)


class ChangeLogs(models.Model):
    user_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_changelogs_user')
    editor_object = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user_changelogs_editor')
    field = models.CharField('field', max_length=255, blank=False, null=False)
    before = models.CharField('before', max_length=255, blank=False, null=False)
    after = models.CharField('after', max_length=255, blank=False, null=False)
    timestamp = models.DateTimeField('timestamp', default=timezone.now)
