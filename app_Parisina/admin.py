from django.contrib import admin
from .models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'direccion', 'fecha_registro']
    search_fields = ['user__username', 'correo']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'telefono', 'ciudad']
    search_fields = ['empresa', 'telefono']

@admin.register(Telas)
class TelasAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_tela', 'color', 'precio', 'stock']
    list_filter = ['tipo_tela', 'proveedor']
    search_fields = ['nombre', 'color']

@admin.register(Decoracion)
class DecoracionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_producto', 'material', 'precio', 'stock']
    list_filter = ['tipo_producto', 'proveedor']
    search_fields = ['nombre', 'material']

@admin.register(MerceriaManualidad)
class MerceriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'marca', 'precio', 'stock']
    list_filter = ['categoria', 'proveedor']
    search_fields = ['nombre', 'marca']

@admin.register(Hogar)
class HogarAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_articulo', 'color', 'precio', 'stock']
    list_filter = ['tipo_articulo', 'proveedor']
    search_fields = ['nombre', 'color']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_pedido', 'estado', 'total']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['cliente__user__username']

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    search_fields = ['pedido__cliente__user__username']