from rest_framework import serializers
from apps.account_.models import Users


class ChangeEmailSerializer(serializers.ModelSerializer):
    old_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    new_email = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('old_email', 'password', 'new_email')

    def validate_old_email(self, value):
        user = self.context['request'].user
        if user.email != value:
            raise serializers.ValidationError("The old email is invalid.")
        return value

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password.")
        return value

    def validate_new_email(self, value):

        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("The new email is already in use.")
        return value

    def validate(self, attrs):
        if attrs['old_email'] == attrs['new_email']:
            raise serializers.ValidationError("The old and new email cannot be the same.")
        return attrs

