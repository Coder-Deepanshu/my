from rest_framework import serializers
from .models import Product

# Yeh serializer Product ko JSON format mein convert karega
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product          # Konsa model use karna hai
        fields = ['id', 'name', 'price', 'description', 'created_at']  
        # Kaunse fields JSON mein dikhane hain