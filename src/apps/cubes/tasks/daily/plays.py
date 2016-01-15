import time

from celery.task import task

from apps.cubes.aggregator.plays_by_item import build_aggregate
from apps.cubes.aggregator import AssertCubeBuild

from apps.base.models import FactServicesHeartbeatPlay as _Fact

@task()
def cube_plays_by_item_daily(async=True):
    # get dates missing aggregated data
    start = time.time()
    name = 'PLAYS_BY_ITEM_DAILY'

    build = AssertCubeBuild(
        name=name,
        fact=_Fact,
        builder=build_aggregate,
        async=async
    )

    build.build()

    end = time.time()
    print 'timeit: {}'.format(end-start)
