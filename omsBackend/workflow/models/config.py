# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from jsonfield import JSONField
from lbutils import create_instance, get_or_none


class ProcessCategory(models.Model):
    name = models.CharField('Name', max_length=255, db_index=True)
    oid = models.SmallIntegerField('Order', default=486)
    is_active = models.BooleanField('is_active', default=True)

    class Meta:
        ordering = ["oid"]

    def __str__(self):
        return self.name


class Process(models.Model):
    name = models.CharField('Name', max_length=255, help_text='Name for this process')
    code = models.CharField('Code', max_length=100, unique=True, help_text='code to identify process')
    prefix = models.CharField('Prefix', max_length=8, default='', blank=True, help_text='prefix for process NO.')
    category = models.ForeignKey(ProcessCategory, blank=True, null=True, on_delete=models.SET_NULL,
                                 verbose_name='Category')
    desc = models.TextField('desc', blank=True)
    oid = models.SmallIntegerField('Order', default=486)
    is_active = models.BooleanField('Is active', default=True)
    ext_data = JSONField(default="{}")

    class Meta:
        verbose_name = 'Process'
        ordering = ["oid"]

    def __str__(self):
        return self.name

    def get_draft_active(self):
        node = get_or_none(Node, process=self, status='draft')
        return node

    def get_rejected_active(self):
        node = get_or_none(Node, process=self, status='rejected')
        return node

    def get_given_up_active(self):
        node = get_or_none(Node, process=self, status='cancel')
        return node

    def get_rollback_transition(self, in_node, out_node):
        transition = Transition(
            name='rollback',
            code='rollback',
            process=self,
            is_agree=False,
            can_auto_agree=False,
            input_node=in_node,
            output_node=out_node,
        )
        return transition

    def get_give_up_transition(self, in_node):
        output = self.get_given_up_active()
        transition = Transition(
            name='cancel',
            code='cancel',
            process=self,
            is_agree=False,
            can_auto_agree=False,
            input_node=in_node,
            output_node=output,
        )
        return transition

    def get_back_to_transition(self, in_node, out_node=None):
        transition = Transition(
            name='back',
            code='back',
            process=self,
            is_agree=False,
            can_auto_agree=False,
            input_node=in_node,
            output_node=out_node,
        )
        return transition

    def get_reject_transition(self, in_node):
        transition = Transition(
            name='reject',
            code='reject',
            process=self,
            is_agree=False,
            can_auto_agree=False,
            input_node=in_node,
            output_node=self.get_rejected_active(),
        )
        return transition


class Node(models.Model):
    """
    Node is the states of an instance.
    """

    STATUS_CHOICES = {
        'draft': 'draft',
        'cancel': 'cancel',
        'rejected': 'rejected',
        'processing': 'processing',
        'completed': 'completed',
    }

    TYPE_CHOICES = {
        'node': 'node',
        'router': 'router',
    }

    process = models.ForeignKey('Process', on_delete=models.CASCADE, verbose_name='Process')
    name = models.CharField('Name', max_length=255)
    step = models.IntegerField('Step', default=0, help_text="", )
    status = models.CharField('Status', max_length=16, default='processing', choices=STATUS_CHOICES.items())
    type = models.CharField('Status', max_length=16, default='node', choices=TYPE_CHOICES.items())
    can_edit = models.BooleanField('Can edit', default=False)
    can_reject = models.BooleanField('Can reject', default=True)
    can_cancel = models.BooleanField('Can cancel', default=True)
    operators = models.TextField('Audit users', blank=True)
    desc = models.TextField('desc', blank=True)
    is_active = models.BooleanField('Is active', default=True)
    ext_data = JSONField(default="{}")

    def __str__(self):
        return '{} - {}'.format(self.process, self.name)

    def is_submitted(self):
        return self.status in ['processing', 'completed']


class Transition(models.Model):
    ROUTING_RULE_CHOICES = {
        'split': 'split',
        'joint': 'joint'
    }
    process = models.ForeignKey('Process', on_delete=models.CASCADE, verbose_name='Process')
    name = models.CharField('Name', max_length=100, default='Agree', help_text="action's name, like: Agree/Submit")
    is_agree = models.BooleanField('Is agree', default=True, help_text='选中生成通过时间')
    can_auto_agree = models.BooleanField('If can auto agree', default=True, help_text='选中那么上个步骤自动通过')
    routing_rule = models.CharField('Routing rule', max_length=16, default='split',
                                    choices=ROUTING_RULE_CHOICES.items(),
                                    help_text="joint: 所有完成后流转. split: 立即流转")
    input_node = models.ForeignKey(Node, verbose_name='input_node', null=True, on_delete=models.SET_NULL,
                                   related_name='input_node')
    output_node = models.ForeignKey(Node, verbose_name='output_node', null=True, on_delete=models.SET_NULL,
                                    related_name='output_node')
    desc = models.TextField('desc', blank=True)
    oid = models.SmallIntegerField('Order', default=999)
    is_active = models.BooleanField('is_active', default=True)
    ext_data = JSONField(default="{}")

    def __str__(self):
        return '{} - {}'.format(self.process.name, self.name)
