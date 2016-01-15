from django.db import models

subscription_status_none = 0
subscription_status_active = 1
subscription_status_cancelled = 2
subscription_status_lapsed = 3
subscription_status_expired = 4
subscription_status_payment_failed = 5
subscription_status_payment_pending = 6

subscription_status_lookup = {
    subscription_status_none: 'inactive',
    subscription_status_active: 'active',
    subscription_status_expired: 'expired',
    subscription_status_cancelled: 'cancelled',
    subscription_status_lapsed: 'lapsed',
    subscription_status_payment_pending: 'payment_pending',
}

_SUBSCRIPTION_STATUS_LOOKUP = dict([(v, k) for k, v in subscription_status_lookup.items()])
_SUBSCRIPTION_STATUS_CHOICES = tuple([(k, v) for k, v in subscription_status_lookup.items()])


class DimensionSubscriptionStatus(models.Model):
    """
    DimensionSubscriptionStatus

    Dim to filter down on a subscriptions status within the reported data facts
    The incoming information is as an integer, however we translate this into its meaning as a description
    """
    id = models.IntegerField(choices=_SUBSCRIPTION_STATUS_CHOICES,
                             default=subscription_status_active, primary_key=True
                            )
    description = models.CharField(max_length=20, default='unknown')

    class Meta:
        app_label = 'base'
        db_table = 'dim_subscription_status'


    @classmethod
    def insert(cls, event=0):
        try:
            desc = subscription_status_lookup[event]
        except:
            desc = subscription_status_lookup[0]

        return DimensionSubscriptionStatus.objects.get_or_create(id=event, description=desc)
