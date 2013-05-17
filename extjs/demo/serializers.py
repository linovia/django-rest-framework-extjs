from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class ExtUserSerializer(UserSerializer):

    @property
    def data(self):
        result = super(ExtUserSerializer, self).data

        success = True
        message = getattr(self, '_extjs_message', '')

        if self._errors:
            success = False
            message = self._errors

        return {
            'success': success,
            'message': message,
            'data': result,
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
