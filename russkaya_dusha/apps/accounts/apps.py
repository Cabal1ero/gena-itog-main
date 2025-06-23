from django.apps import AppConfig

def create_superuser():
    from django.contrib.auth.models import User
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin'
    )

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
