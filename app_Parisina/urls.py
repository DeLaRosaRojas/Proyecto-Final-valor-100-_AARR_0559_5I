from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    
    # CRUD Productos
    path('telas/', views.lista_telas, name='lista_telas'),
    path('telas/agregar/', views.agregar_tela, name='agregar_tela'),
    path('telas/editar/<int:id>/', views.editar_tela, name='editar_tela'),
    path('telas/eliminar/<int:id>/', views.eliminar_tela, name='eliminar_tela'),
    
    path('decoracion/', views.lista_decoracion, name='lista_decoracion'),
    path('decoracion/agregar/', views.agregar_decoracion, name='agregar_decoracion'),
    path('decoracion/editar/<int:id>/', views.editar_decoracion, name='editar_decoracion'),
    path('decoracion/eliminar/<int:id>/', views.eliminar_decoracion, name='eliminar_decoracion'),
    
    path('merceria/', views.lista_merceria, name='lista_merceria'),
    path('merceria/agregar/', views.agregar_merceria, name='agregar_merceria'),
    path('merceria/editar/<int:id>/', views.editar_merceria, name='editar_merceria'),
    path('merceria/eliminar/<int:id>/', views.eliminar_merceria, name='eliminar_merceria'),
    
    path('hogar/', views.lista_hogar, name='lista_hogar'),
    path('hogar/agregar/', views.agregar_hogar, name='agregar_hogar'),
    path('hogar/editar/<int:id>/', views.editar_hogar, name='editar_hogar'),
    path('hogar/eliminar/<int:id>/', views.eliminar_hogar, name='eliminar_hogar'),
    
    # Proveedores
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Pedidos
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/detalle/<int:id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/eliminar/<int:id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('pedidos/cambiar_estado/<int:id>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<str:tipo>/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/agregar-con-cantidad/<str:tipo>/<int:producto_id>/', views.agregar_al_carrito_con_cantidad, name='agregar_al_carrito_con_cantidad'),
    path('carrito/agregar-redirect/<str:tipo>/<int:producto_id>/<int:cantidad>/', views.agregar_al_carrito_con_cantidad_redirect, name='agregar_al_carrito_con_cantidad_redirect'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/procesar/', views.procesar_pago, name='procesar_pago'),
    path('pedido/completado/', views.pedido_completado, name='pedido_completado'),
    
    # Mis Pedidos
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    # Procesar Productos Pendientes
    path('procesar-producto-pendiente/', views.procesar_producto_pendiente, name='procesar_producto_pendiente'),
]