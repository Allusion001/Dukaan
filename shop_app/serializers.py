from rest_framework import serializers
from .models import Product,Cart,CartItem
from django.contrib.auth import get_user_model


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','slug','image','description','category','price']

class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products=serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields=['id','name','slug','image','description','category','price','similar_products']
    
    def get_similar_products(self,product):
        products=Product.objects.filter(category=product.category).exclude(id=product.id)
        serializer=ProductSerializer(products,many=True)
        return serializer.data
    
class CartItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    total=serializers.SerializerMethodField()

    class Meta:
        model=CartItem
        fields=['id','quantity','product','total']

    def get_total(self,cart_item):
        price=cart_item.product.price * cart_item.quantity
        return price

    
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True)
    sum_total=serializers.SerializerMethodField()
    num_of_items=serializers.SerializerMethodField()

    class Meta:
        model=Cart
        fields=['id','cart_code','items','num_of_items','sum_total','created_at','modified']

    def get_sum_total(self,cart):
        items=cart.items.all()
        total=sum([item.product.price for item in items])
        return total

    def get_num_of_items(self,cart):
        items=cart.items.all()
        num_of_items=sum([item.quantity for item in items])
        return num_of_items



class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items=serializers.SerializerMethodField()
   
    class Meta:
        model=Cart
        fields=['id','cart_code','num_of_items']

    def get_num_of_items(self,cart):
        items=cart.items.all()
        num_of_items=sum([item.quantity for item in items])
        return num_of_items


class UserSerializer(serializers.ModelSerializer):
    class Meta:
      
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name','city','state','address','phone')

    
   
    


