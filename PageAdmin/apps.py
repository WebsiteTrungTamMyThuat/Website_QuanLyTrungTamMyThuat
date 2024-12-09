from django.apps import AppConfig


class PageadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PageAdmin'
    verbose_name = "Trang Quản Trị Tùy Chỉnh"
    def ready(self):
        import PageAdmin.signals
