from trendico.models import Cart


def cart_context(request):
    cart_item_count = 0
    cart_total = 0
    cart_items = []

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cart_items.all()
            cart_item_count = cart_items.count()
            cart_total = cart.calculate_total()

    return {
        'cart_item_count': cart_item_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }
