from rest_framework import serializers

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError({'email': 'Этот email уже зарегистрирован.'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        # return User.objects.create_user(**validated_data)