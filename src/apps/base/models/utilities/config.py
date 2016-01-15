from django.db import models


class Config(models.Model):
    """
    Config

    A very critical part of the system to store informative config information that the RIPE system can
    use to operate.
    """

    ACCESS_KEY = 'access_key'
    ACCESS_SECRET = 'access_secret'

    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = 'base'
        db_table = 'config'

    @staticmethod
    def get_config(config_name):
        config = Config.objects.get(name=config_name)
        return config.value
