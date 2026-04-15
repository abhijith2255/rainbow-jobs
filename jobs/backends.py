from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class MultiAuthBackend(ModelBackend):
    """Allows users to log in using their Username, Email, or Phone Number."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the "username" entered is an actual username, an email, or a phone number
            user = User.objects.get(
                Q(username=username) | 
                Q(email=username) | 
                Q(profile__phone_number=username) # Looks up the related profile
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None