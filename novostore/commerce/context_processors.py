from models import CartElement
from views import get_cart

def cart_context(context):
    cart = get_cart(context)
    cart_elements = CartElement.objects.filter(cart = cart).select_related()
    return { 'cart' : cart, 'cart_elements' : cart_elements, 'len_cart_elements' : len(cart_elements) }
