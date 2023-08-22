from django.apps import AppConfig


class StrawberryDjangoAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'strawberry_django_auth'
    name = 'strawberry_django_auth'
    verbose_name = 'Strawberry Django Auth'
    
    def ready(self):
        pass