from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# ======================================================
# 1. CLIENTE (Login)
# ======================================================
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(max_length=50, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# ======================================================
# 2. PROVEEDOR
# ======================================================
class Proveedor(models.Model):
    empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='proveedores/', blank=True, null=True)

    def __str__(self):
        return self.empresa

# ======================================================
# 3. PRODUCTOS (Telas, Decoración, Mercería/Manualidades, Hogar)
# ======================================================
class Telas(models.Model):
    UNIDADES = [
        ('metro', 'Metro'),
        ('par', 'Par'),
        ('paquete', 'Paquete'),
        ('unidad', 'Unidad'),
        ('kit', 'Kit'),
        ('litro', 'Litro'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo_tela = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, choices=UNIDADES, default='unidad')
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='telas/')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos_telas')

    def __str__(self):
        return self.nombre

class Decoracion(models.Model):
    UNIDADES = [
        ('metro', 'Metro'),
        ('par', 'Par'),
        ('paquete', 'Paquete'),
        ('unidad', 'Unidad'),
        ('kit', 'Kit'),
        ('litro', 'Litro'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, choices=UNIDADES, default='unidad')
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='decoracion/')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos_decoracion')

    def __str__(self):
        return self.nombre

class MerceriaManualidad(models.Model):
    UNIDADES = [
        ('metro', 'Metro'),
        ('par', 'Par'),
        ('paquete', 'Paquete'),
        ('unidad', 'Unidad'),
        ('kit', 'Kit'),
        ('litro', 'Litro'),
    ]
    
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, choices=UNIDADES, default='unidad')
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='merceria/')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos_merceria')

    def __str__(self):
        return self.nombre

class Hogar(models.Model):
    UNIDADES = [
        ('metro', 'Metro'),
        ('par', 'Par'),
        ('paquete', 'Paquete'),
        ('unidad', 'Unidad'),
        ('kit', 'Kit'),
        ('litro', 'Litro'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo_articulo = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, choices=UNIDADES, default='unidad')
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='hogar/')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos_hogar')

    def __str__(self):
        return self.nombre

# ======================================================
# 4. PEDIDO  (Carrito y compras)
# ======================================================
class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente (Carrito)'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.user.username}"

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.items.all())
        self.save()
        return self.total

# ======================================================
# 5. PEDIDO ITEM (Detalle del carrito/pedido)
# ======================================================
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"