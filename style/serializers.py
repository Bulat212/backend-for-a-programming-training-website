from rest_framework import serializers

from style.models import Style


class StyleSerializer(serializers.ModelSerializer):    
    category = serializers.PrimaryKeyRelatedField(source="category.name", read_only="True")

    class Meta:
        model = Style
        fields=["name", "price_in_coin", "price_in_stars", "category"] #поля которые будут возвращаться по запросу
    
