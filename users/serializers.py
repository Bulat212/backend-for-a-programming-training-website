from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from style.models import Category, Style, UserStyle

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
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

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


# class UserMinInfoSerializer(serializers.ModelSerializer):
#     nickname_id = serializers.SerializerMethodField()
#     # nickname_id = serializers.PrimaryKeyRelatedField(source='style',
#     #     queryset=Style.objects.all(),
#     #     required=False)
#     username = serializers.CharField(source='user.username')
#     coins = serializers.IntegerField(source='user.coins')
#     stars = serializers.IntegerField(source='user.stars')

#     class Meta:
#         model = UserStyle
#         fields = ['username', 'nickname_id', 'coins', 'stars']
        
#     def get_nickname_id(self, obj):
#         user = self.context['request'].user
#         user_style = UserStyle.objects.filter(user=user, style__category__id=2, is_active=True).first()
#         # user_style = UserStyle.objects.select_related('style__category', 'user').filter(user=user, style__category__id=2, is_active=True).first()
#         if user_style:
#             return user_style.style.id
#         return 0
        
class UserMinInfoSerializer(serializers.ModelSerializer):
    # nickname_id = serializers.PrimaryKeyRelatedField(source='style',
    #     queryset=Style.objects.all(),
    #     required=False)
    username = serializers.CharField()
    coins = serializers.IntegerField()
    stars = serializers.IntegerField()
    nickname_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'coins', 'stars', 'nickname_id']
        
    def get_nickname_id(self, obj):
        user = self.context['request'].user
        user_style = UserStyle.objects.filter(user=user, style__category__id=2, is_active=True).first()
        if user_style:
            return user_style.style.id
        return 0