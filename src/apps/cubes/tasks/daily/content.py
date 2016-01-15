import time

from celery.task import task

from apps.cubes.aggregator.content import build_aggregate
from apps.cubes.aggregator import AssertCubeBuild

from apps.base.models import FactServicesAggregatorAggregation as _Fact


@task()
def cube_content_daily(async=True):
    # get dates missing aggregated data
    start = time.time()
    name = 'CONTENT_DAILY'

    build = AssertCubeBuild(
        name=name,
        fact=_Fact,
        builder=build_aggregate,
        async=async
    )

    build.build()

    end = time.time()
    print 'timeit: {}'.format(end-start)
