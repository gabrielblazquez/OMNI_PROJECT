import os, sys, time, json, subprocess, pandas as pd
import requests
from datetime import datetime, timedelta, timezone

# --- PROTOCOLO DE INICIALIZACIÓN SOBERANA ---
def inicializar_entorno():
    libs = ["psutil", "MetaTrader5", "pandas", "ntplib", "pytz"]
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            print(f"[SISTEMA] Instalando {lib} para HP G42...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

inicializar_entorno()
import psutil, ntplib, MetaTrader5 as mt5

# --- PARÁMETROS NÚCLEO OMNI ---
MAGIC_NUMBER = 281078
ACTIVOS = ["ETHUSD", "SPX500", "BTCUSD"]
RIESGO_OP = 0.02
META_FINAL = 200.00
HISTORIAL_VELAS = 1490
RUTA_OMNI = "C:/OMNI_DATA/"
FILE_JSON = RUTA_OMNI + "omni_soberano.json"

if not os.path.exists(RUTA_OMNI): os.makedirs(RUTA_OMNI)

# --- MÓDULO DE TIEMPO ATÓMICO (NY) ---
def obtener_hora_ny():
    """Sincroniza con NY ignorando el reloj de la PC."""
    try:
        cliente = ntplib.NTPClient()
        res = cliente.request('pool.ntp.org', version=3, timeout=2)
        utc = datetime.fromtimestamp(res.tx_time, timezone.utc)
        return utc - timedelta(hours=4) # EDT Nueva York
    except:
        try:
            res = requests.get('https://www.google.com', timeout=2)
            gmt = datetime.strptime(res.headers['date'], '%a, %d %b %Y %H:%M:%S %Z')
            return gmt - timedelta(hours=4)
        except: return None

# --- SOBERANÍA DE RED (GITHUB AUTO-PUSH) ---
def respaldo_nube(evento, detalle):
    """Escribe en disco y sube a GitHub automáticamente."""
    memoria = []
    if os.path.exists(FILE_JSON):
        with open(FILE_JSON, 'r') as f:
            try: memoria = json.load(f)
            except: memoria = []
    
    t_ny = obtener_hora_ny()
    acc = mt5.account_info()
    registro = {
        "fecha_ny": str(t_ny) if t_ny else "N/A",
        "evento": evento,
        "detalle": detalle,
        "equity": acc.equity if acc else 0
    }
    memoria.append(registro)
    
    with open(FILE_JSON, 'w') as f:
        json.dump(memoria[-300:], f, indent=4)
    
    # Comando de Auto-Push (Soberanía de Red)
    try:
        os.system('git add omni_soberano.json')
        os.system('git commit -m "OMNI_UPDATE: Registro de operacion"')
        os.system('git push origin main')
    except:
        pass # Si no hay internet, sigue operando en local

# --- CEREBRO ANALÍTICO ---
def analizar_mercado(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, HISTORIAL_VELAS)
    if rates is None or len(rates) < 100: return None
    
    df = pd.DataFrame(rates)
    df['ema_fast'] = df['close'].ewm(span=12).mean()
    df['ema_slow'] = df['close'].ewm(span=26).mean()
    
    precio = df['close'].iloc[-1]
    momentum = df['ema_fast'].iloc[-1] > df['ema_slow'].iloc[-1]
    
    # ATR para SL dinámico
    df['hl'] = df['high'] - df['low']
    atr = df['hl'].rolling(14).mean().iloc[-1]
    
    return {"go": momentum, "precio": precio, "atr": atr}

# --- GATILLO MT5 ---
def disparar_orden(symbol, info):
    tick = mt5.symbol_info_tick(symbol)
    if not tick: return
    
    precio = tick.ask
    sl = precio - (info['atr'] * 2.0)
    tp = precio + (info['atr'] * 14.0) # RR 7.0 (Filosofía ETH)
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_BUY,
        "price": precio,
        "sl": sl, "tp": tp,
        "magic": MAGIC_NUMBER,
        "comment": "OMNI SOBERANO v101",
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    res = mt5.order_send(request)
    respaldo_nube("ORDEN_ENVIADA", {"symbol": symbol, "retcode": res.retcode})
    return res

# --- DASHBOARD DE CONTROL ---
def renderizar(acc, n_pos, status, ram, ny_t):
    os.system('cls' if os.name == 'nt' else 'clear')
    color = "0A" if acc and acc.equity >= acc.balance else "0F"
    os.system(f"color {color}")
    
    print("╔" + "═"*66 + "╗")
    print(f"║ OMNI v101.0 | SOBERANÍA TOTAL | NY: {ny_t.strftime('%H:%M:%S') if ny_t else 'SYNC...'} ║")
    print("╠" + "═"*66 + "╣")
    if acc:
        faltante = META_FINAL - acc.equity
        print(f"║ [CUENTA] Balance: ${acc.balance:.2f} | Equity: ${acc.equity:.2f} ║")
        print(f"║ [PC NUEVA] Faltan ${faltante:.2f} para la meta de $200.00 ║")
    print(f"║ [HARDWARE] RAM: {ram}% | DISCO: C:/OMNI_DATA/ (VINCULADO) ║")
    print(f"║ [LOGS]     GITHUB: Sincronización Automática Activa ║")
    print(f"║ [STATUS]   {status.ljust(52)} ║")
    print(f"║ [MERCADO]  Analizando {HISTORIAL_VELAS} velas | Activos: {len(ACTIVOS)} ║")
    print("╚" + "═"*66 + "╝")

# --- BUCLE DE OPERACIÓN ---
if __name__ == "__main__":
    if not mt5.initialize(): sys.exit()
    
    respaldo_nube("SISTEMA_ON", "OMNI Iniciado con Sincronización GitHub")

    while True:
        try:
            acc = mt5.account_info()
            pos = mt5.positions_get()
            n_pos = len(pos) if pos else 0
            ram_uso = psutil.virtual_memory().percent
            ny_time = obtener_hora_ny()
            
            msg = "Buscando oportunidad de Momentum..."
            
            if n_pos < 2:
                for activo in ACTIVOS:
                    analisis = analizar_mercado(activo)
                    if analisis and analisis['go']:
                        msg = f"EJECUTANDO COMPRA EN {activo}..."
                        disparar_orden(activo, analisis)
                        break
            
            renderizar(acc, n_pos, msg, ram_uso, ny_time)
            time.sleep(3 if ram_uso < 80 else 7)
            
        except Exception as e:
            respaldo_nube("ERROR_CRITICO", str(e))
            time.sleep(10)