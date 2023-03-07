from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from .serializers import OrderSerializer, ProductSerializer, UserSerializer, VendorSerializer, ProductHolderList
from .models import Order, Product, User, Vendor, Product_holders_List
from rest_framework import generics
from rest_framework.decorators import api_view
import threading as thread
import stripe
from django.core.mail import EmailMultiAlternatives


def vendors(request):
    queryset = Vendor.objects.all()
    serializer = VendorSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


def products(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


def vendorProductList(request):
    queryset = Product_holders_List.objects.all()
    serializer = ProductHolderList(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


def user(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def searching(request):
    a = []
    products = Product.objects.filter(product_name=request.data.get('search')).values()
    a = [products.get('id') for products in products]
    search = Product_holders_List.objects.filter(product=a[0])
    serializer = ProductHolderList(search, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def order(request):
    data = request.data.get('pv_id')
    arr = []
    pay_price=0
    indiv_price=[]
    for i in range(0, len(request.data.get('pv_id'))):
        orders = Product_holders_List.objects.filter(pk=data[i].get('pid')).values()
        price = [orders.get('price') for orders in orders]
        user = User.objects.get(pk=request.data.get('uid'))
        product = Product.objects.filter(pk=data[i].get('pid'))
        product1 = Product.objects.filter(pk=orders[0].get('product_id')).values()
        arr.append([{"product": [product1.get('product_name') for product1 in product1], "price": price,
                     "quantity": int(data[i].get('quantity'))}])
        instance = Order.objects.create(user=user, quantity=data[i].get('quantity'),
                                        total_price=(int(data[i].get('quantity')) * price[0]))
        instance.product.set(product)
        instance.save()
        individual_price = (int(data[i].get('quantity')) * price[0])
        pay_price+=individual_price
        indiv_price.append(individual_price)

        pill = data[i].get('quantity')
        Product_holders_List.objects.filter(pk__in=[data[i].get('pid')]).update(stock=F('stock') - pill)

    stripe.api_key = 'sk_test_51MBfbdDjBgI52bwWj73IhtqddWHqR5Bv2rxXRtZWm1uiglA6CD3mrq1MLYcQfckir7BXRrqh9HDFtGKzfBl7ECiK00weAtshHv'
    stripe.Charge.create(
        amount=pay_price,
        currency="USD",
        # type="card",
        card={
            "number": request.data.get('card_no'),
            "exp_month": request.data.get('exp_month'),
            "exp_year": request.data.get('exp_year'),
            "cvc": request.data.get('cvc'),
        },
        metadata={'order_id': instance.id}
    )


    subject = 'Purchase receipt'
    # message = f'Dear User \n Thank you for purchasing medicine from us \n Your Purchase List is as follow \n ' +(str(arr))
    email_from = 'f180111@nu.edu.pk'
    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives  # <= EmailMultiAlternatives instead of EmailMessage
    product_mail = []
    product_price = []
    product_quan = []
    for i in range(0, len(arr)):
        product_mail.append([a['product'] for a in arr[i]])
        product_price.append([a['price'] for a in arr[i]])
        product_quan.append([a['quantity'] for a in arr[i]])

    plain_version = '/home/dev/ecommerceApp/ecommercesite/templates/email.html'  # import plain version. No html content
    html_version = '/home/dev/ecommerceApp/ecommercesite/templates/email.html'  # import html version. Has html content
    product_mail2 = []
    product_price2 = []
    product_quan2 = []
    indiv_price2=[]
    for i in range(0,len(product_mail)):
        x = str(product_mail[i])
        y=str(product_quan[i])
        z=str(product_price[i])
        w=str(indiv_price[i])
        x = x.replace("[", "")
        x = x.replace("]", "")
        x = x.replace("'", "")
        y = y.replace("[", "")
        y = y.replace("]", "")
        y = y.replace("'", "")
        z = z.replace("[", "")
        z = z.replace("]", "")
        z = z.replace("'", "")
        w = w.replace("[", "")
        w = w.replace("]", "")
        w = w.replace("'", "")
        product_mail2.append(x)
        product_price2.append(z)
        product_quan2.append(y)
        indiv_price2.append(w)

    print(product_mail2[1])

    html_message = render_to_string(html_version, {'context': product_mail2,'context1':product_price2,'context2':indiv_price2,'context3':product_quan2,'context4':pay_price})

    message = EmailMultiAlternatives(subject, html_message, email_from, to=["email@host.com"])
    message.attach_alternative(html_message, "text/html")  # attach html version
    message.send()
    return JsonResponse("Payment Made Successfully", safe=False)
