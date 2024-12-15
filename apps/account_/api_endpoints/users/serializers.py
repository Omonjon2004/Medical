from rest_framework import serializers
from apps.account_.models import Users, UserProfile


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        source='userprofile.phone_number', allow_blank=True, required=False
    )
    avatar = serializers.ImageField(
        source='userprofile.avatar', required=False
    )

    class Meta:
        model = Users
        fields = (
            'id',
            'full_name',
            'role',
            'email',
            'avatar',
            'phone_number',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        password = validated_data.pop('password', None)


        user = Users(**validated_data)


        if password:
            user.set_password(password)
        user.save()


        user_profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone_number': profile_data.get('phone_number', ''),
                'avatar': profile_data.get('avatar', None)
            }
        )

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        phone_number = profile_data.get('phone_number')
        avatar = profile_data.get('avatar')


        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        user_profile, created = UserProfile.objects.get_or_create(user=instance)

        if phone_number is not None:
            user_profile.phone_number = phone_number
        if avatar is not None:
            user_profile.avatar = avatar
        user_profile.save()

        return instance
