import time

from celery.task import task

from apps.cubes.aggregator.registration_raw import build_aggregate
from apps.cubes.aggregator import AssertCubeBuild

from apps.base.models import FactServicesStorefrontRegistration as _Fact

@task()
def cube_registrations_raw_daily(async=True):

    start = time.time()
    name = 'REGISTRATION_RAW_DAILY'

    build = AssertCubeBuild(
        name=name,
        fact=_Fact,
        builder=build_aggregate,
        async=async
    )

    build.build()

    end = time.time()
    print 'timeit: {}'.format(end-start)



