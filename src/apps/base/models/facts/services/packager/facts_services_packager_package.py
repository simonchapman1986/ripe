from django.db import models

from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_job_manager import DimensionJobManager
from apps.base.models.dimensions.dimension_assets import DimensionAssets


class FactServicesPackagerPackage(models.Model):

    job_manager_id = models.ForeignKey(DimensionJobManager)
    item_id = models.ForeignKey(DimensionItem)
    asset_ids = models.ManyToManyField(DimensionAssets)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    profile = models.TextField()

    event_utc_date = models.ForeignKey(DimensionUTCDate)
    event_utc_datetime = models.DateTimeField()
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_packager_package'

    @classmethod
    def create_fact(cls, **data):
        job_manager = DimensionJobManager.insert(job_manager_id=data['job_manager_id'])
        item = DimensionItem.objects.get(item_id=data['item_id'])

        fact = FactServicesPackagerPackage.objects.create(
            job_manager_id=job_manager,
            item_id=item,
            start_time=data['start_time'],
            end_time=data['end_time'],
            profile=data['profile'],
            event_utc_date=DimensionUTCDate.date_from_datetime(datetime=data['event_time']),
            event_utc_datetime=data['event_time']
        )

        for asset in data['asset_ids']:
            asset_dim = DimensionAssets.objects.create(asset_id=asset)
            fact.asset_ids.add(asset_dim)
            fact.save()

        return fact
