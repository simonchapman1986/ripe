from django.contrib import admin
from apps.cubes.models import *

admin.site.register(CubeAssetMatch)

admin.site.register(CubeLicenseDeliveryRawDaily)

admin.site.register(CubeStoreTransaction)
admin.site.register(CubeDownload)
admin.site.register(CubeRegistrationsDaily)
admin.site.register(CubeSubscriptionsDaily)
admin.site.register(CubeSubscriptionRevenueDaily)

admin.site.register(CubePlaysByItem)

admin.site.register(Log)
