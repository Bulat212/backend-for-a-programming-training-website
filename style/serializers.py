from rest_framework import serializers

from style.models import Style


class StyleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Style
        fields=["name", "price_in_coin", "price_in_stars", "category"] #поля которые будут возвращаться по запросу
    
