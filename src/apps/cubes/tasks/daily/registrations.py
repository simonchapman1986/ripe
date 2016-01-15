import time

from celery.task import task

from apps.cubes.aggregator.registration import build_aggregate
from apps.cubes.aggregator import AssertCubeBuild

from apps.base.models import FactServicesStorefrontRegistration as _Fact

import logging
log = logging.getLogger('reporting')


@task()
def cube_registrations_daily(async=True):
    # get dates missing aggregated data
    start = time.time()
    name = 'REGISTRATIONS_DAILY'

    log.info(' task creating generic cube builder')
    build = AssertCubeBuild(
        name=name,
        fact=_Fact,
        builder=build_aggregate,
        async=async
    )

    build.build()

    end = time.time()
    print 'timeit: {}'.format(end-start)

