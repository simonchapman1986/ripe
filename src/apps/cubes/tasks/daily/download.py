import time

from celery.task import task

from apps.cubes.aggregator.download import build_aggregate
from apps.cubes.aggregator import AssertCubeBuild

from apps.base.models import FactServicesStorefrontDownload as _Fact


@task()
def cube_download_daily(async=True):
    # get dates missing aggregated data
    start = time.time()
    name = 'DOWNLOAD_DAILY'

    build = AssertCubeBuild(
        name=name,
        fact=_Fact,
        builder=build_aggregate,
        async=async
    )

    build.build()

    end = time.time()
    print 'timeit: {}'.format(end-start)
