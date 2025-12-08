// Scripts para Parisina
// Polyfills para compatibilidad con navegadores antiguos

// Polyfill para NodeList.forEach (IE11)
if (window.NodeList && !NodeList.prototype.forEach) {
    NodeList.prototype.forEach = function (callback, thisArg) {
        thisArg = thisArg || window;
        for (var i = 0; i < this.length; i++) {
            callback.call(thisArg, this[i], i, this);
        }
    };
}

// Polyfill para Element.closest (IE11)
if (!Element.prototype.closest) {
    Element.prototype.closest = function(s) {
        var el = this;
        if (!document.documentElement.contains(el)) return null;
        do {
            if (el.matches(s)) return el;
            el = el.parentElement || el.parentNode;
        } while (el !== null && el.nodeType === 1);
        return null;
    };
}

// Polyfill para Element.matches (IE11)
if (!Element.prototype.matches) {
    Element.prototype.matches = 
        Element.prototype.matchesSelector || 
        Element.prototype.mozMatchesSelector ||
        Element.prototype.msMatchesSelector || 
        Element.prototype.oMatchesSelector || 
        Element.prototype.webkitMatchesSelector ||
        function(s) {
            var matches = (this.document || this.ownerDocument).querySelectorAll(s),
                i = matches.length;
            while (--i >= 0 && matches.item(i) !== this) {}
            return i > -1;            
        };
}

// Función de inicialización segura para todos los navegadores
function initializeParisina() {
    // Tu código JavaScript principal aquí
    // Mover todo el contenido del DOMContentLoaded aquí
    
    console.log('Parisina initialized - Browser:', navigator.userAgent);
}

// Inicialización segura para todos los navegadores
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeParisina);
} else {
    initializeParisina();
}

document.addEventListener('DOMContentLoaded', function() {
    // Modal para agregar al carrito
const modal = document.getElementById('modal-carrito');
const closeModalBtns = document.querySelectorAll('.close-modal');
const agregarCarritoBtns = document.querySelectorAll('.agregar-carrito-btn');
const modalForm = document.getElementById('modal-cantidad-form');
const modalProductInfo = document.getElementById('modal-product-info');
const modalCantidad = document.getElementById('modal-cantidad');
const modalStockInfo = document.getElementById('modal-stock-info');

// Verificar si el usuario está autenticado (función helper)
function usuarioEstaAutenticado() {
    return document.body.classList.contains('user-authenticated');
}

function usuarioEsAdministrador() {
    return document.body.classList.contains('user-staff');
}

// Abrir modal
agregarCarritoBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        // Si el usuario no está autenticado, redirigir a login
        if (!usuarioEstaAutenticado()) {
            const tipo = this.getAttribute('data-tipo');
            const productoId = this.getAttribute('data-producto-id');
            const cantidad = 1; // Cantidad por defecto
            
            // Guardar producto pendiente en localStorage
            localStorage.setItem('producto_pendiente', JSON.stringify({
                tipo: tipo,
                producto_id: productoId,
                cantidad: cantidad
            }));
            
            // Redirigir a login
            window.location.href = '/login/';
            return;
        }
        
        // Si es administrador, no permitir
        if (usuarioEsAdministrador()) {
            alert('Los administradores no pueden agregar productos al carrito.');
            return;
        }
        
        // Usuario autenticado y no administrador - mostrar modal
        const tipo = this.getAttribute('data-tipo');
        const productoId = this.getAttribute('data-producto-id');
        const productoNombre = this.getAttribute('data-producto-nombre');
        const productoPrecio = this.getAttribute('data-producto-precio');
        const productoStock = this.getAttribute('data-producto-stock');
        const productoUnidad = this.getAttribute('data-producto-unidad');

        // Llenar información del producto en el modal
        modalProductInfo.innerHTML = `
            <h4>${productoNombre}</h4>
            <p>Precio: $${productoPrecio} / ${productoUnidad}</p>
            <p>Stock disponible: ${productoStock} ${productoUnidad}</p>
        `;

        // Llenar campos ocultos del formulario
        document.getElementById('modal-tipo').value = tipo;
        document.getElementById('modal-producto-id').value = productoId;

        // Configurar cantidad máxima
        modalCantidad.setAttribute('max', productoStock);
        modalCantidad.value = 1; // Resetear a 1
        modalStockInfo.textContent = `Máximo: ${productoStock} ${productoUnidad}`;

        // Mostrar modal
        modal.style.display = 'block';
    });
});

// Cerrar modal
closeModalBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
});

// Cerrar modal al hacer clic fuera
window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Enviar formulario del modal
modalForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const tipo = document.getElementById('modal-tipo').value;
    const productoId = document.getElementById('modal-producto-id').value;
    const cantidad = document.getElementById('modal-cantidad').value;

    // Crear formulario dinámico para enviar
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    formData.append('cantidad', cantidad);

    fetch(`/carrito/agregar-con-cantidad/${tipo}/${productoId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Cerrar modal y mostrar mensaje
            modal.style.display = 'none';
            showMessage(data.message, 'success');
            // Recargar la página para actualizar contador del carrito
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error al agregar al carrito', 'error');
    });
});

    // Sistema de métodos de pago en checkout
const metodoPagoSelect = document.getElementById('metodo_pago');
const metodosPagoForms = document.querySelectorAll('.metodo-pago-form');

if (metodoPagoSelect) {
    metodoPagoSelect.addEventListener('change', function() {
        // Ocultar todos los formularios primero
        metodosPagoForms.forEach(form => {
            form.style.display = 'none';
            // Limpiar campos y quitar required
            const inputs = form.querySelectorAll('input');
            inputs.forEach(input => {
                input.removeAttribute('required');
                input.value = ''; // Limpiar valores
            });
        });

        // Mostrar el formulario correspondiente
        const metodoSeleccionado = this.value;
        if (metodoSeleccionado) {
            const formId = `form-${metodoSeleccionado}`;
            const formToShow = document.getElementById(formId);
            if (formToShow) {
                formToShow.style.display = 'block';
                // Hacer requeridos los campos del formulario mostrado
                const inputs = formToShow.querySelectorAll('input');
                inputs.forEach(input => input.setAttribute('required', 'required'));
            }
        }
    });

    // Disparar el evento change al cargar la página si ya hay un método seleccionado
    if (metodoPagoSelect.value) {
        metodoPagoSelect.dispatchEvent(new Event('change'));
    }
}

    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = 'red';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!valid) {
                e.preventDefault();
                showMessage('Por favor completa todos los campos requeridos.', 'error');
            }
        });
    });

    // Formateo de números de tarjeta
    const numeroTarjetaInput = document.getElementById('numero_tarjeta');
    if (numeroTarjetaInput) {
        numeroTarjetaInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let matches = value.match(/\d{4,16}/g);
            let match = matches && matches[0] || '';
            let parts = [];
            
            for (let i=0, len=match.length; i<len; i+=4) {
                parts.push(match.substring(i, i+4));
            }
            
            if (parts.length) {
                e.target.value = parts.join(' ');
            } else {
                e.target.value = value;
            }
        });
    }

    // Formateo de fecha de vencimiento
    const fechaVencimientoInput = document.getElementById('fecha_vencimiento');
    if (fechaVencimientoInput) {
        fechaVencimientoInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value;
        });
    }

    // Función para mostrar mensajes
    function showMessage(message, type) {
        // Crear elemento de mensaje
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type}`;
        messageDiv.textContent = message;
        
        // Insertar en el contenedor de mensajes
        const messagesContainer = document.querySelector('.messages-container .container');
        if (messagesContainer) {
            messagesContainer.appendChild(messageDiv);
            
            // Remover después de 5 segundos
            setTimeout(() => {
                messageDiv.remove();
            }, 5000);
        } else {
            // Si no hay contenedor, usar alert nativo
            alert(message);
        }
    }

    // Efectos de navegación
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Animación de mensajes existentes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Efectos en tarjetas de productos
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Confirmación para eliminaciones
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        if (button.closest('form')) return;
        
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });
});

// Función para mostrar/ocultar elementos
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

// Función para formatear precios
function formatPrice(price) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(price);
}