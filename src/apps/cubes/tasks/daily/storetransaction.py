import time

from celery.task import task

from apps.cubes.aggregator.storetransaction import build_aggregate
from apps.cubes.aggregator import AssertCubeBuild

from apps.base.models import FactServicesStorefrontTransaction as _Fact

import logging
log = logging.getLogger('reporting')


@task()
def cube_storetransaction_daily(async=True):
    # get dates missing aggregated data
    start = time.time()
    name = 'STORETRANSACTION_DAILY'

    build = AssertCubeBuild(
        name=name,
        fact=_Fact,
        builder=build_aggregate,
        async=async
    )

    build.build()

    end = time.time()
    print 'timeit: {}'.format(end-start)
