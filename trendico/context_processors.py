from trendico.models import Cart, Wishlist


def cart_context(request):
    cart_item_count = 0
    cart_items = []
    cart_total=0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cart_items.all()
            cart_item_count = cart_items.count()
            cart_total=cart.cart_total

    return {
        'cart_item_count': cart_item_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }


def wishlist_context(request):
    wishlist_item_count = 0
    wishlist_items = []

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()

        if wishlist:
            wishlist_items = wishlist.items.all()
            wishlist_item_count = wishlist_items.count()

    return {
        'wishlist_item_count': wishlist_item_count,
        'wishlist_items': wishlist_items,
    }
