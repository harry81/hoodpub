# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from .utils import facebook_action_read


@shared_task
def async_facebook_action_read(sns_id, isbn):
    return facebook_action_read(sns_id, isbn)
