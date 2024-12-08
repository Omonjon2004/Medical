from rest_framework import serializers
from rest_framework.fields import CharField

from apps.account_.models import Users


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = CharField(write_only=True)
    new_password = CharField(write_only=True)
    confirm_new_password = CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('old_password', 'new_password', 'confirm_new_password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your account password is incorrect")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError(
                "Your new password and confirm password do not match"
            )
        return attrs
