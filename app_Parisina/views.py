from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from decimal import Decimal
import json
from .models import *
from .forms import *

def es_administrador(user):
    return user.is_staff

def inicio(request):
    telas = Telas.objects.all()[:4]
    decoracion = Decoracion.objects.all()[:4]
    merceria = MerceriaManualidad.objects.all()[:4]
    hogar = Hogar.objects.all()[:4]
    
    context = {
        'telas': telas,
        'decoracion': decoracion,
        'merceria': merceria,
        'hogar': hogar,
    }
    return render(request, 'inicio.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crear perfil de cliente con todos los datos
            Cliente.objects.create(
                user=user,
                telefono=form.cleaned_data.get('telefono'),
                direccion=form.cleaned_data.get('direccion'),
                correo=form.cleaned_data.get('correo'),
                codigo_postal=form.cleaned_data.get('codigo_postal')
            )
            
            # Autenticar y loguear al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                
                # Verificar si hay producto pendiente en la sesión
                producto_pendiente = request.session.get('producto_pendiente')
                if producto_pendiente:
                    tipo = producto_pendiente['tipo']
                    producto_id = producto_pendiente['producto_id']
                    cantidad = producto_pendiente['cantidad']
                    
                    # Limpiar la sesión
                    del request.session['producto_pendiente']
                    
                    # Redirigir para agregar el producto al carrito
                    return redirect('agregar_al_carrito_con_cantidad_redirect', tipo=tipo, producto_id=producto_id, cantidad=cantidad)
                
                messages.success(request, '¡Registro exitoso! Bienvenido a Parisina.')
                return redirect('inicio')
            
    else:
        form = RegistroForm()
    
    return render(request, 'auth/registro.html', {'form': form})

# ======================================================
# VISTAS PARA TELAS
# ======================================================
def lista_telas(request):
    telas = Telas.objects.all()
    return render(request, 'productos/telas/lista.html', {'telas': telas})

@user_passes_test(es_administrador)
def agregar_tela(request):
    if request.method == 'POST':
        form = TelaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tela agregada correctamente.')
            return redirect('lista_telas')
    else:
        form = TelaForm()
    return render(request, 'productos/telas/form.html', {'form': form, 'titulo': 'Agregar Tela'})

@user_passes_test(es_administrador)
def editar_tela(request, id):
    tela = get_object_or_404(Telas, id=id)
    if request.method == 'POST':
        form = TelaForm(request.POST, request.FILES, instance=tela)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tela actualizada correctamente.')
            return redirect('lista_telas')
    else:
        form = TelaForm(instance=tela)
    return render(request, 'productos/telas/form.html', {'form': form, 'titulo': 'Editar Tela'})

@user_passes_test(es_administrador)
def eliminar_tela(request, id):
    tela = get_object_or_404(Telas, id=id)
    if request.method == 'POST':
        tela.delete()
        messages.success(request, 'Tela eliminada correctamente.')
        return redirect('lista_telas')
    return render(request, 'productos/telas/eliminar.html', {'tela': tela})

# ======================================================
# VISTAS PARA DECORACIÓN
# ======================================================
def lista_decoracion(request):
    productos = Decoracion.objects.all()
    return render(request, 'productos/decoracion/lista.html', {'productos': productos})

@user_passes_test(es_administrador)
def agregar_decoracion(request):
    if request.method == 'POST':
        form = DecoracionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto de decoración agregado correctamente.')
            return redirect('lista_decoracion')
    else:
        form = DecoracionForm()
    return render(request, 'productos/decoracion/form.html', {'form': form, 'titulo': 'Agregar Decoración'})

@user_passes_test(es_administrador)
def editar_decoracion(request, id):
    producto = get_object_or_404(Decoracion, id=id)
    if request.method == 'POST':
        form = DecoracionForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_decoracion')
    else:
        form = DecoracionForm(instance=producto)
    return render(request, 'productos/decoracion/form.html', {'form': form, 'titulo': 'Editar Decoración'})

@user_passes_test(es_administrador)
def eliminar_decoracion(request, id):
    producto = get_object_or_404(Decoracion, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('lista_decoracion')
    return render(request, 'productos/decoracion/eliminar.html', {'producto': producto})

# ======================================================
# VISTAS PARA MERCERÍA
# ======================================================
def lista_merceria(request):
    productos = MerceriaManualidad.objects.all()
    return render(request, 'productos/merceria/lista.html', {'productos': productos})

@user_passes_test(es_administrador)
def agregar_merceria(request):
    if request.method == 'POST':
        form = MerceriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto de mercería agregado correctamente.')
            return redirect('lista_merceria')
    else:
        form = MerceriaForm()
    return render(request, 'productos/merceria/form.html', {'form': form, 'titulo': 'Agregar Mercería'})

@user_passes_test(es_administrador)
def editar_merceria(request, id):
    producto = get_object_or_404(MerceriaManualidad, id=id)
    if request.method == 'POST':
        form = MerceriaForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_merceria')
    else:
        form = MerceriaForm(instance=producto)
    return render(request, 'productos/merceria/form.html', {'form': form, 'titulo': 'Editar Mercería'})

@user_passes_test(es_administrador)
def eliminar_merceria(request, id):
    producto = get_object_or_404(MerceriaManualidad, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('lista_merceria')
    return render(request, 'productos/merceria/eliminar.html', {'producto': producto})

# ======================================================
# VISTAS PARA HOGAR
# ======================================================
def lista_hogar(request):
    productos = Hogar.objects.all()
    return render(request, 'productos/hogar/lista.html', {'productos': productos})

@user_passes_test(es_administrador)
def agregar_hogar(request):
    if request.method == 'POST':
        form = HogarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto para hogar agregado correctamente.')
            return redirect('lista_hogar')
    else:
        form = HogarForm()
    return render(request, 'productos/hogar/form.html', {'form': form, 'titulo': 'Agregar Producto Hogar'})

@user_passes_test(es_administrador)
def editar_hogar(request, id):
    producto = get_object_or_404(Hogar, id=id)
    if request.method == 'POST':
        form = HogarForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_hogar')
    else:
        form = HogarForm(instance=producto)
    return render(request, 'productos/hogar/form.html', {'form': form, 'titulo': 'Editar Producto Hogar'})

@user_passes_test(es_administrador)
def eliminar_hogar(request, id):
    producto = get_object_or_404(Hogar, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('lista_hogar')
    return render(request, 'productos/hogar/eliminar.html', {'producto': producto})

# ======================================================
# VISTAS PARA PROVEEDORES
# ======================================================
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})

@user_passes_test(es_administrador)
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor agregado correctamente.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/form.html', {'form': form, 'titulo': 'Agregar Proveedor'})

@user_passes_test(es_administrador)
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/form.html', {'form': form, 'titulo': 'Editar Proveedor'})

@user_passes_test(es_administrador)
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado correctamente.')
        return redirect('lista_proveedores')
    return render(request, 'proveedores/eliminar.html', {'proveedor': proveedor})

# ======================================================
# CRUD CLIENTES
# ======================================================
@user_passes_test(es_administrador)
def lista_clientes(request):
    clientes = Cliente.objects.all().select_related('user')
    return render(request, 'clientes/lista.html', {'clientes': clientes})

@user_passes_test(es_administrador)
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.correo = request.POST.get('correo')
        cliente.codigo_postal = request.POST.get('codigo_postal')
        cliente.save()
        messages.success(request, 'Cliente actualizado correctamente.')
        return redirect('lista_clientes')
    
    return render(request, 'clientes/form.html', {'cliente': cliente})

@user_passes_test(es_administrador)
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        usuario = cliente.user
        cliente.delete()
        usuario.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('lista_clientes')
    return render(request, 'clientes/eliminar.html', {'cliente': cliente})

# ======================================================
# CRUD PEDIDOS
# ======================================================
@user_passes_test(es_administrador)
def lista_pedidos(request):
    pedidos = Pedido.objects.all().select_related('cliente__user')
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})

@user_passes_test(es_administrador)
def detalle_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    items = pedido.items.all()
    
    context = {
        'pedido': pedido,
        'items': items,
    }
    return render(request, 'pedidos/detalle.html', context)

@user_passes_test(es_administrador)
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        pedido.direccion_envio = request.POST.get('direccion_envio')
        pedido.estado = request.POST.get('estado')
        pedido.save()
        messages.success(request, 'Pedido actualizado correctamente.')
        return redirect('lista_pedidos')
    
    return render(request, 'pedidos/form.html', {'pedido': pedido})

@user_passes_test(es_administrador)
def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado correctamente.')
        return redirect('lista_pedidos')
    return render(request, 'pedidos/eliminar.html', {'pedido': pedido})

@user_passes_test(es_administrador)
def cambiar_estado_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADOS):
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f'Estado del pedido cambiado a {nuevo_estado}.')
        return redirect('detalle_pedido', id=pedido.id)
    return redirect('lista_pedidos')

# ======================================================
# CARRITO DE COMPRAS Y PRODUCTOS PENDIENTES
# ======================================================
def agregar_al_carrito(request, tipo, producto_id):
    # Si el usuario no está autenticado, guardar en sesión y redirigir a login
    if not request.user.is_authenticated:
        request.session['producto_pendiente'] = {
            'tipo': tipo,
            'producto_id': producto_id,
            'cantidad': 1
        }
        request.session.modified = True
        messages.info(request, 'Por favor inicia sesión para agregar productos al carrito.')
        return redirect('login')
    
    # Si es administrador, no permitir
    if request.user.is_staff:
        messages.error(request, 'Los administradores no pueden agregar productos al carrito.')
        return redirect('inicio')
    
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = Cliente.objects.create(
            user=request.user,
            correo=request.user.email
        )
    
    return agregar_producto_al_carrito(request, cliente, tipo, producto_id, 1)

@login_required
def agregar_al_carrito_con_cantidad(request, tipo, producto_id):
    if request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Los administradores no pueden agregar productos al carrito.'})
    
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = Cliente.objects.create(
            user=request.user,
            correo=request.user.email
        )
    
    cantidad = int(request.POST.get('cantidad', 1))
    
    # Llamar a la función helper para AJAX
    return agregar_producto_al_carrito_ajax(request, cliente, tipo, producto_id, cantidad)

def agregar_al_carrito_con_cantidad_redirect(request, tipo, producto_id, cantidad):
    """Vista para redirección después del login/registro"""
    if request.user.is_staff:
        messages.error(request, 'Los administradores no pueden agregar productos al carrito.')
        return redirect('inicio')
    
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = Cliente.objects.create(
            user=request.user,
            correo=request.user.email
        )
    
    cantidad = int(cantidad)
    return agregar_producto_al_carrito(request, cliente, tipo, producto_id, cantidad)

def agregar_producto_al_carrito(request, cliente, tipo, producto_id, cantidad):
    """Función helper para agregar productos al carrito (redirección normal)"""
    pedido, created = Pedido.objects.get_or_create(cliente=cliente, estado='pendiente')
    
    modelos = {
        'telas': Telas,
        'decoracion': Decoracion,
        'merceria': MerceriaManualidad,
        'hogar': Hogar,
    }
    
    if tipo not in modelos:
        messages.error(request, 'Tipo de producto no válido.')
        return redirect('inicio')
    
    Modelo = modelos[tipo]
    producto = get_object_or_404(Modelo, id=producto_id)
    
    # Verificar stock
    if cantidad > producto.stock:
        messages.error(request, f'No hay suficiente stock. Stock disponible: {producto.stock}')
        return redirect(request.META.get('HTTP_REFERER', 'inicio'))
    
    content_type = ContentType.objects.get_for_model(Modelo)
    item_existente = PedidoItem.objects.filter(
        pedido=pedido,
        content_type=content_type,
        object_id=producto.id
    ).first()
    
    if item_existente:
        item_existente.cantidad += cantidad
        item_existente.save()
    else:
        PedidoItem.objects.create(
            pedido=pedido,
            content_type=content_type,
            object_id=producto.id,
            precio_unitario=producto.precio,
            cantidad=cantidad
        )
    
    messages.success(request, f'{cantidad} x {producto.nombre} agregado al carrito.')
    return redirect('ver_carrito')

def agregar_producto_al_carrito_ajax(request, cliente, tipo, producto_id, cantidad):
    """Función helper para agregar productos al carrito (respuesta AJAX)"""
    pedido, created = Pedido.objects.get_or_create(cliente=cliente, estado='pendiente')
    
    modelos = {
        'telas': Telas,
        'decoracion': Decoracion,
        'merceria': MerceriaManualidad,
        'hogar': Hogar,
    }
    
    if tipo not in modelos:
        return JsonResponse({'success': False, 'message': 'Tipo de producto no válido.'})
    
    Modelo = modelos[tipo]
    producto = get_object_or_404(Modelo, id=producto_id)
    
    # Verificar stock
    if cantidad > producto.stock:
        return JsonResponse({'success': False, 'message': f'No hay suficiente stock. Stock disponible: {producto.stock}'})
    
    content_type = ContentType.objects.get_for_model(Modelo)
    item_existente = PedidoItem.objects.filter(
        pedido=pedido,
        content_type=content_type,
        object_id=producto.id
    ).first()
    
    if item_existente:
        item_existente.cantidad += cantidad
        item_existente.save()
    else:
        PedidoItem.objects.create(
            pedido=pedido,
            content_type=content_type,
            object_id=producto.id,
            precio_unitario=producto.precio,
            cantidad=cantidad
        )
    
    return JsonResponse({'success': True, 'message': f'{cantidad} x {producto.nombre} agregado al carrito.'})

@login_required
def ver_carrito(request):
    if request.user.is_staff:
        messages.error(request, 'Los administradores no pueden acceder al carrito.')
        return redirect('inicio')
    
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = Cliente.objects.create(
            user=request.user,
            correo=request.user.email
        )
        messages.info(request, 'Se ha creado tu perfil de cliente automáticamente.')
    
    pedido, created = Pedido.objects.get_or_create(cliente=cliente, estado='pendiente')
    
    subtotal = sum(item.subtotal for item in pedido.items.all())
    impuestos = subtotal * Decimal('0.16')
    total = subtotal + impuestos
    
    context = {
        'pedido': pedido,
        'subtotal': subtotal,
        'impuestos': impuestos,
        'total': total,
    }
    return render(request, 'carrito/ver.html', context)

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(PedidoItem, id=item_id)
    if item.pedido.cliente.user != request.user:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('ver_carrito')
    
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('ver_carrito')

@login_required
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(PedidoItem, id=item_id)
    if item.pedido.cliente.user != request.user:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('ver_carrito')
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            # Verificar stock
            producto = item.producto
            if cantidad > producto.stock:
                messages.error(request, f'No hay suficiente stock. Stock disponible: {producto.stock}')
            else:
                item.cantidad = cantidad
                item.save()
                messages.success(request, 'Cantidad actualizada.')
        else:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito.')
    
    return redirect('ver_carrito')

# ======================================================
# CHECKOUT Y PAGO
# ======================================================
@login_required
def checkout(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    pedido = get_object_or_404(Pedido, cliente=cliente, estado='pendiente')
    
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        metodo_pago = request.POST.get('metodo_pago')
        
        if direccion and metodo_pago:
            # Validar información según el método de pago
            if metodo_pago in ['tarjeta_credito', 'tarjeta_debito']:
                numero_tarjeta = request.POST.get('numero_tarjeta', '').replace(' ', '')
                fecha_vencimiento = request.POST.get('fecha_vencimiento')
                cvv = request.POST.get('cvv')
                nombre_tarjeta = request.POST.get('nombre_tarjeta')
                
                # Validaciones del servidor (adicionales al JavaScript)
                if not all([numero_tarjeta, fecha_vencimiento, cvv, nombre_tarjeta]):
                    messages.error(request, 'Por favor completa toda la información de la tarjeta.')
                    return redirect('checkout')
                
                # Validar fecha de vencimiento en el servidor también
                try:
                    mes, año = fecha_vencimiento.split('/')
                    mes = int(mes)
                    año = int(año) + 2000  # Convertir a año completo
                    
                    from datetime import datetime
                    ahora = datetime.now()
                    fecha_vencimiento_obj = datetime(año, mes, 1)
                    
                    if fecha_vencimiento_obj < ahora:
                        messages.error(request, 'La tarjeta está vencida. Por favor usa una tarjeta válida.')
                        return redirect('checkout')
                        
                except (ValueError, IndexError):
                    messages.error(request, 'Fecha de vencimiento inválida.')
                    return redirect('checkout')
            
            elif metodo_pago == 'paypal':
                email_paypal = request.POST.get('email_paypal')
                if not email_paypal or 'usuario_paypal_autenticado' not in email_paypal:
                    messages.error(request, 'Por favor inicia sesión en PayPal correctamente.')
                    return redirect('checkout')
            
            elif metodo_pago == 'transferencia':
                comprobante = request.POST.get('comprobante_transferencia')
                fecha_transferencia = request.POST.get('fecha_transferencia')
                
                if not comprobante or not fecha_transferencia:
                    messages.error(request, 'Por favor completa la información de la transferencia.')
                    return redirect('checkout')
            
            # PROCESAR EL PEDIDO (si pasó todas las validaciones)
            pedido.direccion_envio = direccion
            pedido.estado = 'pagado'
            pedido.calcular_total()
            pedido.save()
            
            # Reducir stock de productos
            stock_suficiente = True
            productos_sin_stock = []
            
            for item in pedido.items.all():
                producto = item.producto
                if producto.stock >= item.cantidad:
                    producto.stock -= item.cantidad
                    producto.save()
                else:
                    stock_suficiente = False
                    productos_sin_stock.append(producto.nombre)
            
            if stock_suficiente:
                messages.success(request, f'¡Pedido #{pedido.id} realizado con éxito! Método de pago: {metodo_pago.replace("_", " ").title()}')
                return redirect('pedido_completado')
            else:
                # Revertir el estado si no hay stock
                pedido.estado = 'pendiente'
                pedido.save()
                messages.error(request, f'No hay suficiente stock de: {", ".join(productos_sin_stock)}')
                return redirect('ver_carrito')
                
        else:
            messages.error(request, 'Por favor completa la dirección y selecciona un método de pago.')
            return redirect('checkout')
    
    # Calcular totales (para GET request)
    subtotal = sum(item.subtotal for item in pedido.items.all())
    impuestos = subtotal * Decimal('0.16')
    total = subtotal + impuestos
    
    context = {
        'pedido': pedido,
        'subtotal': subtotal,
        'impuestos': impuestos,
        'total': total,
        'cliente': cliente,
    }
    return render(request, 'carrito/checkout.html', context)

@login_required
def procesar_pago(request):
    if request.user.is_staff:
        messages.error(request, 'Los administradores no pueden realizar compras.')
        return redirect('inicio')
    
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = Cliente.objects.create(
            user=request.user,
            correo=request.user.email
        )
    
    pedido = get_object_or_404(Pedido, cliente=cliente, estado='pendiente')
    
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        direccion = request.POST.get('direccion')
        
        if not direccion:
            messages.error(request, 'Por favor proporciona una dirección de envío.')
            return redirect('checkout')
        
        # Procesar información de pago según el método
        if metodo_pago == 'tarjeta_credito':
            numero_tarjeta = request.POST.get('numero_tarjeta')
            fecha_vencimiento = request.POST.get('fecha_vencimiento')
            cvv = request.POST.get('cvv')
            nombre_titular = request.POST.get('nombre_titular')
            
            if not all([numero_tarjeta, fecha_vencimiento, cvv, nombre_titular]):
                messages.error(request, 'Por favor completa todos los campos de la tarjeta.')
                return redirect('checkout')
        
        elif metodo_pago == 'tarjeta_debito':
            numero_tarjeta = request.POST.get('numero_tarjeta')
            fecha_vencimiento = request.POST.get('fecha_vencimiento')
            cvv = request.POST.get('cvv')
            nombre_titular = request.POST.get('nombre_titular')
            
            if not all([numero_tarjeta, fecha_vencimiento, cvv, nombre_titular]):
                messages.error(request, 'Por favor completa todos los campos de la tarjeta.')
                return redirect('checkout')
        
        elif metodo_pago == 'paypal':
            email_paypal = request.POST.get('email_paypal')
            if not email_paypal:
                messages.error(request, 'Por favor proporciona tu email de PayPal.')
                return redirect('checkout')
        
        elif metodo_pago == 'transferencia':
            clabe = request.POST.get('clabe')
            banco = request.POST.get('banco')
            if not all([clabe, banco]):
                messages.error(request, 'Por favor completa todos los campos de transferencia.')
                return redirect('checkout')
        
        # Actualizar pedido
        pedido.direccion_envio = direccion
        pedido.estado = 'pagado'
        pedido.calcular_total()
        pedido.save()
        
        # Actualizar dirección del cliente si se proporciona
        if direccion and not cliente.direccion:
            cliente.direccion = direccion
            cliente.save()
        
        # Reducir stock de productos
        for item in pedido.items.all():
            producto = item.producto
            producto.stock -= item.cantidad
            producto.save()
        
        messages.success(request, '¡Pago procesado exitosamente! Tu pedido ha sido confirmado.')
        return redirect('pedido_completado')
    
    return redirect('checkout')

@login_required
def pedido_completado(request):
    return render(request, 'carrito/pedido_completado.html')

# ======================================================
# PEDIDOS DEL CLIENTE
# ======================================================
# En views.py - Versión simple
@login_required
def mis_pedidos(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    pedidos = Pedido.objects.filter(cliente=cliente).exclude(estado='pendiente').order_by('fecha_pedido')
    
    pedidos_con_totales = []
    for i, pedido in enumerate(pedidos, start=1):  # ¡Aquí está la magia!
        subtotal = sum(item.subtotal for item in pedido.items.all())
        impuestos = subtotal * Decimal('0.16')
        total = subtotal + impuestos
        
        pedidos_con_totales.append({
            'pedido': pedido,
            'subtotal': subtotal,
            'impuestos': impuestos,
            'total': total,
            'cantidad_items': pedido.items.count(),
            'numero_orden': i  # i empieza en 1
        })
    
    context = {'pedidos_con_totales': pedidos_con_totales}
    return render(request, 'carrito/mis_pedidos.html', context)

# ======================================================
# PROCESAR PRODUCTOS PENDIENTES
# ======================================================
@login_required
def procesar_producto_pendiente(request):
    """Procesar producto pendiente después del login/registro"""
    if request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Los administradores no pueden agregar productos al carrito.'})
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))
        
        if tipo and producto_id:
            try:
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                cliente = Cliente.objects.create(
                    user=request.user,
                    correo=request.user.email
                )
            
            return agregar_producto_al_carrito_ajax(request, cliente, tipo, producto_id, cantidad)
    
    return JsonResponse({'success': False, 'message': 'Datos inválidos.'})