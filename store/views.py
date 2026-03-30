from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, Order, OrderItem
import random

# ------------------ HOME ------------------
def home(request):
    return render(request, 'store/index.html')


# ------------------ ADD PRODUCT ------------------
def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']

        Product.objects.create(
            name=name,
            price=price,
            stock=stock
        )

        return redirect('/products/')

    return render(request, 'store/add_product.html')


# ------------------ VIEW PRODUCTS ------------------
def view_products(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})


# ------------------ ADD TO CART ------------------


# ------------------ VIEW CART ------------------
def view_cart(request):
    user = "user1"

    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    total = sum([i.product.price * i.quantity for i in items])

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })


# ------------------ REMOVE FROM CART ------------------
def remove_from_cart(request, id):
    user = "user1"

    cart, created = Cart.objects.get_or_create(user=user)

    try:
        item = CartItem.objects.get(cart=cart, product_id=id)
        item.delete()
    except:
        pass

    return redirect('/cart/')


# ------------------ PLACE ORDER ------------------
def place_order(request):
    user = "user1"

    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect('/cart/')

    order = Order.objects.create(user=user, status="CREATED")
    total = 0

    try:
        # CHECK STOCK + REDUCE
        for i in items:
            if i.product.stock < i.quantity:
                raise Exception("Stock not enough")

            i.product.stock -= i.quantity
            i.product.save()

            OrderItem.objects.create(
                order=order,
                product=i.product,
                quantity=i.quantity
            )

            total += i.product.price * i.quantity

        # PAYMENT SIMULATION
        if random.choice([True, False]):
            order.status = "PAID"
        else:
            raise Exception("Payment failed")

        order.total = total
        order.save()

        # CLEAR CART
        items.delete()

        return render(request, 'store/success.html', {'order': order})

    except Exception as e:
        # ROLLBACK
        for i in items:
            i.product.stock += i.quantity
            i.product.save()

        order.status = "FAILED"
        order.save()

        return render(request, 'store/error.html', {'msg': str(e)})


# ------------------ VIEW ORDERS ------------------
def view_orders(request):
    orders = Order.objects.all()
    return render(request, 'store/orders.html', {'orders': orders})


# ------------------ CANCEL ORDER ------------------
def cancel_order(request, id):
    order = Order.objects.get(id=id)

    if order.status == "CANCELLED":
        return redirect('/orders/')

    items = OrderItem.objects.filter(order=order)

    # RESTORE STOCK
    for i in items:
        i.product.stock += i.quantity
        i.product.save()

    order.status = "CANCELLED"
    order.save()

    return redirect('/orders/')


# ------------------ RETURN PRODUCT ------------------
def return_product(request, id):
    try:
        order_item = OrderItem.objects.get(id=id)

        order_item.product.stock += order_item.quantity
        order_item.product.save()

        order_item.delete()
    except:
        pass

    return redirect('/orders/')


# ------------------ LOW STOCK ------------------
def low_stock(request):
    products = Product.objects.filter(stock__lt=5)
    return render(request, 'store/low_stock.html', {'products': products})

def add_to_cart(request, id):
    user = "user1"

    product = Product.objects.get(id=id)

    cart, created = Cart.objects.get_or_create(user=user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}   # ✅ FIX HERE
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('/cart/')