from django.apps import AppConfig


class PageadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PageAdmin'
    
    def ready(self):
        import PageAdmin.signals
