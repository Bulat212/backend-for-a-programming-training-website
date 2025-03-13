from rest_framework import serializers

from style.models import Style, UserStyle


class StyleSerializer(serializers.ModelSerializer):    
    category = serializers.PrimaryKeyRelatedField(source="category.name", read_only="True")

    class Meta:
        model = Style
        fields=["name", "price_in_coin", "price_in_stars", "category"] #поля которые будут возвращаться по запросу
    

class UserStyleSerializer(serializers.ModelSerializer):    
    style = serializers.SlugRelatedField(slug_field="name", queryset=Style.objects.all())

    class Meta:
        model = UserStyle
        fields=["style", "is_active"] #поля которые будут возвращаться по запросу
    