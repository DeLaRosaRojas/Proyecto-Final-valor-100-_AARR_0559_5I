from .models import Pedido, Cliente

def carrito_context(request):
    context = {}
    # Solo mostrar contador del carrito para clientes (NO administradores)
    if request.user.is_authenticated and not request.user.is_staff:
        try:
            cliente = Cliente.objects.get(user=request.user)
            pedido = Pedido.objects.filter(cliente=cliente, estado='pendiente').first()
            if pedido:
                context['items_carrito'] = pedido.items.count()
            else:
                context['items_carrito'] = 0
        except Cliente.DoesNotExist:
            context['items_carrito'] = 0
    else:
        context['items_carrito'] = 0
    
    return context