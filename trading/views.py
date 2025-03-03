from django.shortcuts import render, redirect, get_object_or_404
from .serializers import OrderSerializer, TransactionSerializer
from rest_framework import viewsets
from products.models import Product
from django.contrib import messages
from .models import Order, Transaction, TradeRequest
from users.permissions import IsAdmin
from users.models import User
from django.contrib.auth.decorators import login_required


@login_required
def create_trade_request(request, product_id):
    requested_product = get_object_or_404(Product, id=product_id)

    if request.user == requested_product.representative:
        messages.error(request, "You cannot trade your own product.")
        return redirect('product_list')

    if request.method == "POST":
        offered_product_id = request.POST.get("offered_product")
        offered_product = get_object_or_404(Product, id=offered_product_id)

        if offered_product.representative != request.user:
            messages.error(request, "You can only offer products you own.")
            return redirect('product_list')

        trade_request = TradeRequest.objects.create(
            customer=request.user,
            trader=requested_product.representative,
            offered_product=offered_product,
            requested_product=requested_product
        )
        messages.success(request, "Trade request sent successfully.")
        return redirect('product_list')

    user_products = Product.objects.filter(representative=request.user)
    return render(request, 'trading/create_trade.html', {
        'requested_product': requested_product,
        'user_products': user_products
    })
    

@login_required
def confirm_trade(request, trade_id):
    trade = get_object_or_404(TradeRequest, id=trade_id, status="accepted", trader=request.user)

    if request.method == "POST":
        # Swap product owners
        trade.offered_product.representative, trade.requested_product.representative = (
            trade.requested_product.representative,
            trade.offered_product.representative,
        )
        trade.offered_product.save()
        trade.requested_product.save()

        # Create Order & Transaction
        order = Order.objects.create(
            user=trade.customer, 
            product=trade.requested_product, 
            quantity=1, 
            status='completed'
        )

        transaction = Transaction.objects.create(
            order=order,
            status='success',
            payment_method='trade',
            amount=0,
            transaction_id=f"trade_{trade.id}"
        )

        trade.delete()  # Remove trade request after completion
        messages.success(request, "Trade successfully completed!")
        return redirect('profile', username=request.user.username)

    return render(request, 'trading/confirm_trade.html', {'trade': trade})


def accept_trade(request, trade_id):
    trade = get_object_or_404(TradeRequest, id=trade_id, trader=request.user, status='pending')
    
    # Mark trade as accepted before redirecting
    trade.status = "accepted"
    trade.save()
    
    return redirect("confirm_trade", trade_id=trade.id)


def decline_trade(request, trade_id):
    trade = get_object_or_404(TradeRequest, id=trade_id, trader=request.user, status='pending')
    trade.status = "declined"
    trade.save()
    messages.info(request, "Trade request declined.")
    return redirect("product_list")


class OrderAPI(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdmin]
    
    
class TransactionAPI(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAdmin]
