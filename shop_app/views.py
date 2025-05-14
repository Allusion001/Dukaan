from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Product,CartItem,Cart
from rest_framework.response import Response
from .serializers import ProductSerializer
from .serializers import DetailedProductSerializer
from .serializers import CartItemSerializer
from .serializers import SimpleCartSerializer
from .serializers import CartSerializer
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import paypalrestsdk
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
import uuid
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model



BASE_URL=settings.REACT_BASE_URL
User = get_user_model()

# Create your views here.

@api_view(['GET'])
def products (request):
    products= Product.objects.all()
    serializers=ProductSerializer(products,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    serializer=DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def add_item(request):
    try:
        cart_code=request.data.get('cart_code')
        product_id=request.data.get('product_id')

        cart,created=Cart.objects.get_or_create(cart_code=cart_code)

        product=Product.objects.get(id=product_id)

        cart_item , created=CartItem.objects.get_or_create(cart=cart,product=product)
        cart_item.quantity=1
        cart_item.save()

        serializer=CartItemSerializer(cart_item)
        return Response({'data':serializer.data,'message':"Successfully Created"},status=201)
    
    except Exception as e:
          return Response({'error':str(e)},status=300)


@api_view(['GET'])
def product_in_cart(request):   
    cart_code=request.query_params.get('cart_code')
    product_id=request.query_params.get('product_id')

    cart=Cart.objects.get(cart_code=cart_code)
    product=Product.objects.get(id=product_id)

    product_exists_in_cart=CartItem.objects.filter(cart=cart,product=product).exists()

    return Response({'product_in_cart' : product_exists_in_cart} )


@api_view(['GET'])
def get_cart_stat(request):   
    cart_code=request.query_params.get('cart_code')
    cart=Cart.objects.get(cart_code=cart_code,paid=False)
    serializer=SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):   
    cart_code=request.query_params.get('cart_code')
    cart=Cart.objects.get(cart_code=cart_code,paid=False)
    serializer=CartSerializer(cart)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id =request.data.get("item_id")
        quantity=request.data.get("quantity")
        quantity=int(quantity)
        cartitem=CartItem.objects.get(id=cartitem_id)
        cartitem.quantity=quantity
        cartitem.save()
        serializer=CartItemSerializer(cartitem)
        return Response({'data':serializer.data,"message":"CartItem updated"})

    except Exception as e:
        return Response({"error":str(e)},status=400)


@api_view(['POST'])
def delete_cartitem(request): 
    cartitem_id =request.data.get("item_id")
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    user =request.user
    return Response({"username":user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_items(request):
    user =request.user
    serializer=UserSerializer(user)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):

    trxID=str(uuid.uuid4())
    user=request.user
    cart_code=request.data.get("cart_code")
    print(cart_code)
    cart=Cart.objects.get(cart_code=cart_code)
    
    amount=sum(item.product.price * item.quantity for item in cart.items.all())
    tax=Decimal(4.00)
    total=amount + tax


    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": BASE_URL+"/payment/success",
            "cancel_url": BASE_URL+"http://localhost:5173/payment/cancel"
        },
        "transactions": [
            {
                "amount": {
                    "total": str(total),  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })
    print("Payment links:", payment.links)

    if payment.create():
        print("Payment created successfully")
        print(payment.to_dict())
        for link in payment.links:
            if link.method == "REDIRECT":
                approval_url = link.href
                return JsonResponse({'approval_url': approval_url})
        return JsonResponse({'error': 'No redirect URL found.'}, status=500)
    else:
        print("Payment creation error:", payment.error)
        return JsonResponse({'error': payment.error}, status=500)




def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

def payment_checkout(request):
    return render(request, 'checkout.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')


@api_view(['POST'])
def registerUser(request):
    try:
        
        username=request.data.get('username')
        password=request.data.get('password')
        firstName=request.data.get('firstName')
        lastName=request.data.get('lastName')
        email=request.data.get('email')
        city=request.data.get('city')
        country=request.data.get('country')
        phone=request.data.get('phone')

        user = User(
            username=username,
            password=password,
            first_name=firstName,
            last_name=lastName,
            email=email,
            city=city,
            phone=phone,
            
        )
        user.set_password(password)
        user.save()
        

        serializer=UserSerializer(user)
        return Response(serializer.data)


    
    except Exception as e:
          print(e)
          return Response({'error':str(e)},status=300)


