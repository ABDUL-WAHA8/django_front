from rest_framework import serializers
from .models import Product

class CustomerSerializer(serializers.Serializer):
    first_name=serializers.CharField(max_length=255)
    last_name=serializers.CharField(max_length=255)
    email=serializers.EmailField()
    phone=serializers.CharField()


class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    unit_price=serializers.DecimalField(max_digits=6,decimal_places=2)
    inventory=serializers.IntegerField()
    


