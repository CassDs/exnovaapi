# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.2.0] - 2026-02-01

### Agregado

- **Soporte para múltiples conexiones simultáneas**: Ahora es posible conectar múltiples cuentas de Exnova al mismo tiempo sin que interfieran entre sí.
- `context.py`: Nueva clase `ExnovaContext` que mantiene el estado por instancia (SSID, balance_id, flags de conexión).
- Documentación completa: README.md, CONTRIBUTING.md, CHANGELOG.md.

### Cambiado

- **api.py**:
  - Ahora inicializa `self.context = ExnovaContext()` en lugar de usar variables globales.
  - Todas las referencias a `global_value.X` cambiadas a `self.context.X`.

- **ws/client.py**:
  - `on_message`, `on_error`, `on_open`, `on_close` ahora usan `self.api.context` en lugar de `global_value`.
  - `on_error` y `on_open` ya no son `@staticmethod` para poder acceder al contexto de instancia.

- **stable_api.py**:
  - Todas las referencias a `global_value.balance_id` cambiadas a `self.api.context.balance_id`.
  - Referencias a `global_value.check_websocket_if_connect` cambiadas a `self.api.context.check_websocket_if_connect`.

- **ws/chanels/*.py** (8 archivos):
  - `buyv2.py`: Usa `self.api.context.balance_id`.
  - `buyv3.py`: Usa `self.api.context.balance_id`.
  - `digital_option.py`: Usa `self.api.context.balance_id`.
  - `get_deferred_orders.py`: Usa `self.api.context.balance_id`.
  - `api_game_getoptions.py`: Usa `self.api.context.balance_id`.
  - `get_positions.py`: Usa `self.api.context.balance_id`.
  - `buy_place_order_temp.py`: Usa `self.api.context.balance_id`.
  - `buy_blitz_option.py`: Usa `self.api.context.balance_id`.

- **ws/received/profile.py**:
  - Usa `api.context.balance_id` en lugar de `global_value.balance_id`.

- **ws/received/candle_generated.py**:
  - Removido import no utilizado de `global_value`.

### Deprecado

- `global_value.py`: Este módulo ya no se usa activamente. Se mantiene por compatibilidad pero todas las funcionalidades han sido movidas a `ExnovaContext`.

### Corregido

- **Bug crítico**: Cuando se conectaban múltiples cuentas, todas las operaciones se ejecutaban en la última cuenta conectada porque `SSID` y `balance_id` eran variables globales compartidas.

## [0.1.0] - 2026-01-21

### Agregado

- Fork inicial de la librería exnovaapi.
- Soporte para opciones binarias, digitales y blitz.
- Soporte para CFD, forex y crypto.
- Streaming de datos en tiempo real.
- Autenticación con 2FA por SMS.

---

## Guía de Migración

### De 0.1.x a 0.2.0

No se requieren cambios en el código del usuario. La API pública permanece igual.

**Antes (0.1.x)** - Solo una cuenta a la vez:
```python
api = Exnova("email", "password")
api.connect()
# Conectar otra cuenta sobrescribía la primera
```

**Después (0.2.0)** - Múltiples cuentas simultáneas:
```python
api1 = Exnova("email1", "password1")
api2 = Exnova("email2", "password2")
api1.connect()
api2.connect()
# Ambas cuentas funcionan independientemente
```
