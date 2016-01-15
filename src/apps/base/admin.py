from django.contrib import admin
from apps.base.models import *

admin.site.register(FactServicesBackstageAssetMatch)
admin.site.register(FactServicesBackstageItemMetadata)

admin.site.register(FactServicesLicensingDelivery)

admin.site.register(FactServicesStorefrontTransaction)
admin.site.register(FactServicesStorefrontDownload)
admin.site.register(FactServicesStorefrontRegistration)
admin.site.register(FactServicesStorefrontSubscription)

admin.site.register(FactServicesHeartbeatPlay)
admin.site.register(FactServicesHeartbeatPlayBuffer)
admin.site.register(FactServicesHeartbeatPlayInit)
