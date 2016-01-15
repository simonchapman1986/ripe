from itertools import chain
from django.db import models, transaction
from django_extensions.db.fields import UUIDField

from apps.base.models.data import BLANK_UUID
from apps.base.models.debug import to_string
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension import update_or_insert, select_or_insert

from apps.flags.checks.user import missing_user_id

import logging
log = logging.getLogger('reporting')


class DimensionUser(models.Model):
    """
    DimensionUser

    Dim to filter down on users within the reported data facts.

    We store a varied amount of data that links to clients and territories, not every user could expect both an
    internal user id and an external user id, however normally expected.

    Needs some work to migrate some portions of this code into a save part of a model manager to save
    state ifs
    """

    internal_user_id = UUIDField(version=4, null=True, default=BLANK_UUID)
    external_user_id = UUIDField(version=4, null=True, default=BLANK_UUID)
    territory = models.ForeignKey(DimensionTerritory, null=True)
    client = models.ForeignKey(DimensionClient, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, blank=True, null=True, default='')
    marketing_preference = models.NullBooleanField(null=True)
    country_of_residence = models.CharField(max_length=36, blank=True, null=True, default='')
    email = models.CharField(max_length=255, default=None, null=True)

    def __repr__(self):
        return to_string(
            self, 5,
            self.id,
            self.internal_user_id,
            self.external_user_id,
            self.client_id,
            self.territory_id
        )

    class Meta:
        app_label = 'base'
        db_table = 'dim_user'
        unique_together = ("internal_user_id", "external_user_id", "territory", "client")


    # TODO: make use of django 'manager' pattern for all these static / class methods.
    @staticmethod
    @transaction.commit_on_success
    def _replace_user_id(old, new):
        for related in [rel.get_accessor_name() for rel in old._meta.get_all_related_objects()]:
            getattr(old, related).update(user=new)
        old.delete()

    @classmethod
    def _insert_external(cls, external, **values):
        if 'internal_user_id' in values:
            values['internal_user_id'] = BLANK_UUID
        if values.has_key('client'):
            return update_or_insert(cls, values, external_user_id=external, client=values['client'])
        else:
            try:
                unknown_client = DimensionClient.objects.get(id=-1)
                return update_or_insert(cls, values, external_user_id=external, client=unknown_client)
            except:
                return select_or_insert(cls, values, external_user_id=external)


    @classmethod
    def _insert_internal(cls, internal, **values):
        if 'external_user_id' in values:
            values['external_user_id'] = BLANK_UUID
        return update_or_insert(cls, values, internal_user_id=internal)

    @classmethod
    def _insert_both(cls, internal, external, **values):

        result = update_or_insert(cls, values, internal_user_id=internal, external_user_id=external)

        deprecated = []
        deprecated.append(DimensionUser.objects.filter(internal_user_id=internal).exclude(id=result.id))
        if 'client' in values:
            deprecated.append(DimensionUser.objects.filter(external_user_id=external,
                                                           client=values['client']).exclude(id=result.id))

        for deprecated_user in chain(*deprecated):
            cls._replace_user_id(deprecated_user, result)

        return result

    @classmethod
    def insert(cls, **values):
        # TODO flag
        internal = values.get('internal_user_id', None)
        external = values.get('external_user_id', None)

        _values = {name: value for name, value in values.iteritems() if value}

        if internal and external:
            return cls._insert_both(internal, external, **_values)
        elif internal:
            return cls._insert_internal(internal, **_values)
        elif external:
            return cls._insert_external(external, **_values)
        else:
            missing_user_id(event_name='insert_user', description='Inserting a user without any user id.')

