# Guía de Contribución

Gracias por tu interés en contribuir a ExnovaAPI. Este documento proporciona guías y mejores prácticas para contribuir al proyecto.

## Tabla de Contenidos

- [Configuración del Entorno](#configuración-del-entorno)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Estándares de Código](#estándares-de-código)
- [Flujo de Trabajo](#flujo-de-trabajo)
- [Patrones Importantes](#patrones-importantes)
- [Testing](#testing)
- [Documentación](#documentación)

## Configuración del Entorno

### Requisitos

- Python 3.10+
- pip o uv

### Instalación para Desarrollo

```bash
# Clonar el repositorio
git clone <repo-url>
cd exnovaapi

# Instalar en modo desarrollo
pip install -e .

# O con uv
uv pip install -e .

# Instalar dependencias de desarrollo
pip install pylint pytest
```

## Estructura del Proyecto

```
exnovaapi/
├── __init__.py           # Exportaciones públicas
├── api.py                # API core (HTTP + WebSocket)
├── stable_api.py         # API de usuario de alto nivel
├── context.py            # Contexto por instancia (estado de sesión)
├── constants.py          # Mapeo de activos a IDs
├── country_id.py         # IDs de países
├── expiration.py         # Cálculo de tiempos de expiración
├── global_value.py       # [DEPRECADO] Variables globales
├── version_control.py    # Versión de la API
├── http/                 # Endpoints HTTP
│   ├── login.py
│   ├── logout.py
│   ├── getprofile.py
│   └── ...
└── ws/                   # WebSocket
    ├── client.py         # Cliente WebSocket principal
    ├── chanels/          # Mensajes salientes
    │   ├── base.py       # Clase base para canales
    │   ├── buyv3.py      # Compra de opciones
    │   └── ...
    ├── received/         # Handlers de mensajes entrantes
    │   ├── profile.py
    │   ├── candles.py
    │   └── ...
    └── objects/          # Objetos de datos
        ├── timesync.py
        ├── profile.py
        └── ...
```

## Estándares de Código

### Estilo

- Seguir PEP 8
- Usar type hints cuando sea posible
- Docstrings en formato Google

```python
def buy(self, price: float, active: str, action: str, expiration: int) -> tuple[bool, int | str]:
    """
    Ejecutar una operación de compra.

    Args:
        price: Monto a invertir.
        active: Nombre del activo (ej: "EURUSD").
        action: Dirección ("call" o "put").
        expiration: Tiempo en minutos.

    Returns:
        Tuple de (success, order_id o error_message).
    """
```

### Convenciones de Nombres

- Clases: `PascalCase` (ej: `WebsocketClient`)
- Funciones/métodos: `snake_case` (ej: `get_balance`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `REDIS_CONNECTION_PREFIX`)
- Variables privadas: `_prefijo` (ej: `self._connections`)

### Manejo del Estado

**IMPORTANTE**: No usar variables globales. Usar `self.api.context` para estado por instancia.

```python
# MAL - No hacer esto
import exnovaapi.global_value as global_value
global_value.balance_id = 123

# BIEN - Usar contexto de instancia
self.api.context.balance_id = 123
```

## Flujo de Trabajo

### 1. Crear Branch

```bash
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/descripcion-del-bug
```

### 2. Hacer Cambios

- Escribir código siguiendo los estándares
- Agregar tests si aplica
- Actualizar documentación

### 3. Commit

Usar mensajes de commit descriptivos:

```bash
git commit -m "feat: agregar soporte para opciones blitz

- Implementar buy_blitz() en stable_api.py
- Agregar canal BuyBlitzOption
- Actualizar documentación"
```

Prefijos recomendados:
- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `refactor:` Refactorización sin cambio de funcionalidad
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

### 4. Push y Pull Request

```bash
git push origin feature/nombre-descriptivo
```

## Patrones Importantes

### Patrón de Canales WebSocket

Los canales en `ws/chanels/` heredan de `Base` y tienen acceso a `self.api`:

```python
from exnovaapi.ws.chanels.base import Base

class MiCanal(Base):
    name = "sendMessage"

    def __call__(self, param1, param2):
        data = {
            "name": "mi-operacion",
            "body": {
                "param1": param1,
                "user_balance_id": int(self.api.context.balance_id),
            }
        }
        self.send_websocket_request(self.name, data)
```

### Patrón de Handlers de Mensajes

Los handlers en `ws/received/` reciben `api` y `message`:

```python
def mi_handler(api, message):
    if message["name"] == "mi-mensaje":
        # Procesar mensaje
        api.mi_dato = message["msg"]

        # Acceder al contexto de instancia
        if api.context.balance_id == message["msg"]["balance_id"]:
            # Es para esta cuenta
            pass
```

### Patrón de Polling en stable_api

Muchas operaciones esperan respuesta del servidor:

```python
def mi_operacion(self):
    self.api.resultado = None
    self.api.enviar_solicitud()

    # Esperar respuesta (con timeout)
    start = time.time()
    while self.api.resultado is None:
        if time.time() - start > 30:
            return None
        time.sleep(0.1)

    return self.api.resultado
```

## Testing

### Ejecutar Tests

```bash
pytest tests/
```

### Escribir Tests

```python
import pytest
from exnovaapi.stable_api import Exnova

def test_multiple_connections():
    """Verificar que múltiples instancias tienen contextos separados."""
    api1 = Exnova("email1", "pass1")
    api2 = Exnova("email2", "pass2")

    api1.api.context.balance_id = 100
    api2.api.context.balance_id = 200

    assert api1.api.context.balance_id == 100
    assert api2.api.context.balance_id == 200
```

## Documentación

### Actualizar Documentación

Al agregar nuevas funcionalidades:

1. Actualizar docstrings en el código
2. Agregar ejemplos en README.md
3. Documentar cambios en CHANGELOG.md

### Formato del CHANGELOG

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Agregado
- Nueva característica A

### Cambiado
- Modificación a característica B

### Corregido
- Bug en característica C

### Deprecado
- Característica D será removida en vX.Y.Z
```

## Contacto

Para preguntas o discusiones, abrir un Issue en el repositorio.

---

¡Gracias por contribuir!
