from rest_framework import serializers
from we_robot.models import Mode


class ModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode
        fields = ('id', 'user', 'mode')
