# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from salts.models import SaltState, StateJob
from users.models import User
from omsBackend.settings import sapi


class SaltStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaltState
        fields = ['url', 'id', 'name', 'cmd', 'desc']


class StateJobSerializer(serializers.ModelSerializer):
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    job = serializers.SlugRelatedField(queryset=SaltState.objects.all(), slug_field='name')

    class Meta:
        model = StateJob
        fields = ['url', 'id', 'statejob', 'j_id', 'status', 'hosts', 'action_user', 'result', 'create_time']

    def create(self, validated_data):
        cmd = SaltState.objects.get(name=validated_data["statejob"]).cmd
        hosts = validated_data["hosts"]
        jid = sapi.remote_state(tgt=hosts.split(','), arg=cmd)
        validated_data["j_id"] = jid
        job = StateJob.objects.create(**validated_data)
        job.save()
        return job