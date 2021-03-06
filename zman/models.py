# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
import uuid


class OwedItem(models.Model):
    id = models.CharField(max_length=128,
                          default=lambda: uuid.uuid4().hex, primary_key=True)
    created = models.DateTimeField(default=lambda: datetime.utcnow())
    item_type = models.CharField(max_length=128, default="zman")
    owed_username = models.CharField(max_length=128)
    ower_username = models.CharField(max_length=128)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("item_type", "owed_username", "ower_username")

    @classmethod
    def ensure_owed_item(cls, owed_username,
                         ower_username, item_type, count=1):
        """Will ensure that an item being owed will be created."""
        try:
            item = cls.objects.get(owed_username=owed_username,
                                   ower_username=ower_username,
                                   item_type=item_type)
            item.count = item.count + count
        except OwedItem.DoesNotExist:
            item = cls()
            item.item_type = item_type.lower()
            item.owed_username = owed_username.lower()
            item.ower_username = ower_username.lower()
            item.count = count
        item.save()
        return item

    @classmethod
    def ensure_paid_item(cls, owed_username,
                         ower_username, item_type, count=1):
        """Retruns true if the item actually paid a debt, False
        if no debt needed to be paid."""
        try:
            item = cls.objects.get(owed_username=owed_username,
                                   ower_username=ower_username,
                                   item_type=item_type)
            item.count = item.count - count
            if item.count < 0:
                item.count = 0
            item.save()
            if item.count == 0:
                item.delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def total_to_give_count(cls, username):
        """Returns the total count of items for the username to give"""
        count = 0
        for item in cls.objects.filter(ower_username=username.lower()):
            count = count + item.count
        return count

    @classmethod
    def total_getting_count(cls, username):
        """Returns the total count of items owed to the username"""
        count = 0
        for item in cls.objects.filter(owed_username=username.lower()):
            count = count + item.count
        return count

    @classmethod
    def to_give(cls, username, item_type="zman"):
        """Will return a query set of the item type a person has to give.  Defaults to zmans"""
        return cls.objects.filter(ower_username=username.lower(), item_type=item_type)

    @classmethod
    def to_get(cls, username, item_type="zman"):
        """"Will return a query set of the item type a person is owed.  Defaults to zmans"""
        return cls.objects.filter(owed_username=username.lower(), item_type=item_type)
