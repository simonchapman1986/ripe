from django.db import models
from django_extensions.db.fields import UUIDField


class Service(models.Model):
    """
    Service

    As a service that can talk to other services, or be indeed spoken too, we need to operate in the NEXUS
    style platform with various serivce to service authentication and/or claims based.

    When these situations occur, we need to be able to authorise so we use our stored access/secret information
    """
    uuid = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    access_key = models.CharField(max_length=32, unique=True, default='')
    access_secret = models.CharField(max_length=32, unique=True, default='')

    class Meta:
        app_label = 'base'
        db_table = 'service'

    @staticmethod
    def get_by_access_key(access_key):
        try:
            service = Service.objects.get(access_key=access_key)
            return service
        except Service.DoesNotExist:
            return None

    @staticmethod
    def get_secret_by_access_key(access_key):
        try:
            service = Service.objects.get(access_key=access_key)
            return service.access_secret
        except Service.DoesNotExist:
            return None
