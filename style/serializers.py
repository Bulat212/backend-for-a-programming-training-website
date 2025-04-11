from pyexpat import model
from unicodedata import category
from rest_framework import serializers

from style.models import Style, UserStyle


class StyleSerializer(serializers.ModelSerializer):    
    category = serializers.PrimaryKeyRelatedField(source="category.name", read_only="True")

    class Meta:
        model = Style
        fields=["id", "name", "price_in_coin", "price_in_stars", "category"] #поля которые будут возвращаться по запросу
    

class UserStyleSerializer(serializers.ModelSerializer):    
    style_id = serializers.PrimaryKeyRelatedField(source='style', queryset=Style.objects.all())
    # style = serializers.SlugRelatedField(slug_field="name", queryset=Style.objects.all())
    currency = serializers.CharField(write_only=True)
    category = serializers.CharField(source="style.category.name", read_only=True)

    class Meta:
        model = UserStyle
        fields=["style_id", "is_active", "currency", "category" ] #поля которые будут возвращаться по запросу
    
    def create(self, validated_data):
        currency = validated_data.pop('currency')
        user_style = UserStyle.objects.create(**validated_data)
        return user_style
    
class UserStyleSetIsActiveSerializer(serializers.ModelSerializer):
    style = serializers.CharField(read_only=True)
    clear_category = serializers.CharField(required=False)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserStyle
        fields = ["style", "is_active", "clear_category"]
        