from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, full_name, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not full_name:
            raise ValueError('User must have a full name.')
        if not email:
            raise ValueError('User must have an email adress.')
        if not password:
            raise ValueError('User must have a password.')
        else:
            user = self.model(
                email = self.normalize_email(email),
            )
            user.full_name = full_name
            user.email = email
            user.is_staff = is_staff
            user.is_active = is_active
            user.is_admin = is_admin
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_staffuser(self, full_name, email, password=None):
        user = self.create_user(
            full_name = full_name,
            email = email,
            password = password,
            is_staff = True
        )
        return user

    def create_superuser(self, full_name, email, password=None):
        user = self.create_user(
            full_name = full_name,
            email = email,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user
