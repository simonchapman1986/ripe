import logging
from django.core.exceptions import MultipleObjectsReturned
from django.db import transaction
from django.db import IntegrityError


logger = logging.getLogger('reporting')


def insert_or_update(dimension, update, values, **keys):
    if update:
        return update_or_insert(dimension, values, **keys)
    return select_or_insert(dimension, values, **keys)


@transaction.commit_on_success
def update_or_insert(dimension, values, **keys):
    keys['defaults'] = values
    multiple_objects_returned = False
    try:
        obj, created = dimension.objects.get_or_create(**keys)
    except IntegrityError:
        transaction.commit()
        try:
            obj, created = dimension.objects.get_or_create(**keys)
        except MultipleObjectsReturned:
            multiple_objects_returned = True
    except MultipleObjectsReturned:
        multiple_objects_returned = True

    if multiple_objects_returned:
        logger.warning("Multiple %s objects for %s.", dimension, keys)
        del keys['defaults']
        obj = dimension.objects.filter(**keys)[0]
        for name, value in values.items():
            setattr(obj, name, value)
        obj.save()
        return obj

    if not created:
        for name, value in values.items():
            setattr(obj, name, value)
        obj.save()

    return obj


@transaction.commit_on_success
def select_or_insert(dimension, values, **keys):
    keys['defaults'] = values
    try:
        obj, _ = dimension.objects.get_or_create(**keys)
    except IntegrityError:
        transaction.commit()
        obj, _ = dimension.objects.get_or_create(**keys)
    except MultipleObjectsReturned:
        logger.warning("Multiple %s objects for %s.", dimension, keys)
        del keys['defaults']
        return dimension.objects.filter(**keys)[0]

    return obj
