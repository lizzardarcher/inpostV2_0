from django.apps import AppConfig
# from django.core.signals import request_finished, setting_changed


class AppsHomeConfig(AppConfig):

    name = 'apps.home'
    verbose_name = 'Apps Home'

    # def ready(self):
    #     from . import signals
    #     request_finished.connect(signals.my_callback)
