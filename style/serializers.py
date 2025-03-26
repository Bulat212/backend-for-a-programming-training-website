from pyexpat import model
from rest_framework import serializers

from style.models import Style, UserStyle


class StyleSerializer(serializers.ModelSerializer):    
    category = serializers.PrimaryKeyRelatedField(source="category.name", read_only="True")

    class Meta:
        model = Style
        fields=["name", "price_in_coin", "price_in_stars", "category"] #поля которые будут возвращаться по запросу
    

class UserStyleSerializer(serializers.ModelSerializer):    
    style = serializers.SlugRelatedField(slug_field="name", queryset=Style.objects.all())
    currency = serializers.CharField(write_only=True)

    class Meta:
        model = UserStyle
        fields=["style", "is_active", "currency"] #поля которые будут возвращаться по запросу
    
    def create(self, validated_data):
        currency = validated_data.pop('currency')
        user_style = UserStyle.objects.create(**validated_data)
        return user_style
    
class UserStyleSetIsActiveSerializer(serializers.ModelSerializer):
    style = serializers.CharField(read_only=True)

    class Meta:
        model = UserStyle
        fields = ["style", "is_active"]
        