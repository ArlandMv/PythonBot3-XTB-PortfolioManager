Entendido. A continuación te presento una versión reorganizada de **`API_REFERENCE.md`** con los métodos clasificados en categorías más útiles basadas en su momento de uso dentro del flujo de trading: **Pre-Trade**, **Trade**, y **Post-Trade**. Además, he añadido los métodos sugeridos como `get_trading_hours`, `make_trade`, y `check_trade` (implementados de forma conceptual para completar el esquema).

---

# **API_REFERENCE.md**

## **Índice**
1. [Inicialización](#inicialización)
2. [Métodos Pre-Trade](#métodos-pre-trade)
3. [Métodos Trade](#métodos-trade)
4. [Métodos Post-Trade](#métodos-post-trade)
5. [Pruebas de Ejemplo](#pruebas-de-ejemplo)
6. [Mensajes de Error](#mensajes-de-error)

---

## **Inicialización**
### **Clase: `XTBApiClient`**
```python
XTBApiClient(api_url: str, stream_url: str, user_id: str, password: str)
```
#### **Parámetros:**
- **`api_url`**: URL del WebSocket para solicitudes principales.
- **`stream_url`**: URL del WebSocket para transmisión de datos en tiempo real.
- **`user_id`**: ID del usuario.
- **`password`**: Contraseña del usuario.

#### **Ejemplo:**
```python
api_client = XTBApiClient("wss://ws.xtb.com/demo", "wss://ws.xtb.com/demoStream", "123456", "mi_password")
```

---

## **Métodos Pre-Trade**

Estos métodos son utilizados para obtener información necesaria antes de iniciar un trade.

### **`get_account_data()`**
Obtiene información sobre la cuenta activa.

```python
cuenta = api_client.get_account_data()
print(cuenta)
```

---

### **`get_all_currency_pairs()`**
Obtiene una lista de pares de divisas disponibles.

```python
pares = api_client.get_all_currency_pairs()
print(pares)
```

---

### **`get_trading_hours(symbol: str)`**
Obtiene los horarios de trading para un símbolo específico.

- **Parámetros:**
  - `symbol`: El símbolo (e.g., "USDCLP").

```python
horarios = api_client.get_trading_hours("USDCLP")
print(horarios)
```

---

### **`get_tick_prices(symbol: str)`**
Obtiene los precios más recientes del símbolo especificado.

- **Parámetros:**
  - `symbol`: El símbolo (e.g., "USDCLP").

```python
precios = api_client.get_tick_prices("USDCLP")
print(precios)
```

---

### **`get_candles(symbol: str, start: int, end: int, period: int)`**
Obtiene velas (candlesticks) históricas de un símbolo.

- **Parámetros:**
  - `symbol`: El símbolo (e.g., "USDCLP").
  - `start`: Timestamp inicial.
  - `end`: Timestamp final.
  - `period`: Periodo de las velas (e.g., 60 segundos).

```python
velas = api_client.get_candles("USDCLP", start_timestamp, end_timestamp, 60)
print(velas)
```

---

## **Métodos Trade**

Estos métodos son utilizados para ejecutar operaciones en el mercado.

### **`make_trade(symbol: str, volume: float, trade_type: str, price: float, sl: float, tp: float)`**
Ejecuta un trade con los parámetros especificados.

- **Parámetros:**
  - `symbol`: El símbolo (e.g., "USDCLP").
  - `volume`: Volumen de la operación.
  - `trade_type`: Tipo de operación (`BUY` o `SELL`).
  - `price`: Precio de entrada.
  - `sl`: Nivel de Stop Loss.
  - `tp`: Nivel de Take Profit.

```python
resultado = api_client.make_trade("USDCLP", 0.1, "BUY", 800.00, 790.00, 820.00)
print(resultado)
```

---

## **Métodos Post-Trade**

Estos métodos son utilizados para verificar el estado o los resultados de las operaciones realizadas.

### **`get_balance()`**
Obtiene el balance actual de la cuenta.

```python
balance = api_client.get_balance()
print(balance)
```

---

### **`check_trade(trade_id: str)`**
Verifica el estado de una operación específica.

- **Parámetros:**
  - `trade_id`: ID único de la operación.

```python
estado = api_client.check_trade("12345")
print(estado)
```

---

### **`get_keep_alive()`**
Envía un mensaje `keepAlive` para mantener la conexión activa.

```python
api_client.get_keep_alive()
```

---

## **Pruebas de Ejemplo**

```python
if __name__ == "__main__":
    api_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, DEMO_PASSWORD)
    
    try:
        api_client.connect()
        print("Datos de la cuenta:", api_client.get_account_data())
        print("Pares de divisas:", api_client.get_all_currency_pairs())
        print("Horarios USDCLP:", api_client.get_trading_hours("USDCLP"))
        print("Tick prices USDCLP:", api_client.get_tick_prices("USDCLP"))

        # Velas históricas
        start = 1700000000
        end = 1700003600
        print("Candles USDCLP:", api_client.get_candles("USDCLP", start, end, 60))
        
        # Ejemplo de trade
        resultado_trade = api_client.make_trade("USDCLP", 0.1, "BUY", 800.00, 790.00, 820.00)
        print("Resultado del trade:", resultado_trade)

        # Estado de una operación
        print("Estado del trade:", api_client.check_trade("12345"))

        # KeepAlive
        api_client.get_keep_alive()

    finally:
        api_client.disconnect()
```

---

## **Mensajes de Error**
Esta sección detalla los errores comunes devueltos por el servidor de transacciones.

| **Código de Error** | **Descripción**                          |
|----------------------|------------------------------------------|
| **BE001**            | Precio inválido                        |
| **BE002**            | StopLoss o TakeProfit inválido          |
| **BE003**            | Volumen inválido                       |
| **BE004**            | Inicio de sesión deshabilitado         |
| **BE005**            | Login o contraseña inválidos           |
| **BE006**            | Mercado cerrado para el instrumento    |
| **BE007**            | Parámetros inconsistentes              |
| **BE008**            | Modificación denegada                 |
| **BE009**            | Fondos insuficientes                  |
| **BE010**            | Cotización no disponible              |
| **BE011**            | Posiciones opuestas prohibidas         |
| **BE012**            | Posiciones cortas prohibidas           |
| **BE013**            | Precio modificado                     |
| **BE014**            | Solicitudes demasiado frecuentes       |
| **BE016-BE017**      | Demasiadas solicitudes de transacción  |
| **BE018**            | Instrumento deshabilitado para trading |
| **BE094**            | Símbolo no válido para la cuenta       |
| **EX007**            | Login bloqueado tras múltiples fallos  |
| **EX009**            | Límite de datos superado              |

---
