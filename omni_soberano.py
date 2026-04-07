import datetime, pytz, requests, os, time, subprocess, winsound, json
import MetaTrader5 as mt5
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE IDENTIDAD ---
PATH_DATA = r"C:\OMNI_DATA"
FILE_SELF = __file__
FILE_MEMORIA = os.path.join(PATH_DATA, "omni_soberano.json")

def obtener_hora():
    try:
        ny = datetime.datetime.now(pytz.timezone('America/New_York'))
        ba = ny.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))
        return ny, ba
    except:
        now = datetime.datetime.now()
        return now, now

def cerrar_todo(motivo):
    """ OMNI toma el control y cierra todas las posiciones abiertas """
    print(f"🚨 [INTERVENCIÓN] Cerrando posiciones por: {motivo}", flush=True)
    positions = mt5.positions_get()
    if positions:
        for pos in positions:
            ticket = pos.ticket
            type_dict = {mt5.POSITION_TYPE_BUY: mt5.ORDER_TYPE_SELL, mt5.POSITION_TYPE_SELL: mt5.ORDER_TYPE_BUY}
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": mt5.symbol_info_tick(pos.symbol).bid if pos.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask,
                "magic": 100,
                "comment": "OMNI_SOBERANA_CLOSE",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            mt5.order_send(request)
        winsound.Beep(2000, 1000)

def mutar_omni(nueva_logica, motivo):
    """ Auto-edición con sangría protegida y push a OMNI_PROJECT """
    try:
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        with open(FILE_SELF, 'w', encoding='utf-8') as f:
            for linea in lineas:
    if sigma > 17.1254: print('IA: Alerta de Volatilidad Extrema') # [IA_NUCLEO_EVOLUTIVO]
    if sigma > 17.1254: print('IA: Alerta de Volatilidad Extrema') # [IA_NUCLEO_EVOLUTIVO]
                else: f.write(linea)
        
        subprocess.run(["git", "add", "."], shell=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Evolucion: {motivo}"], shell=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True, capture_output=True)
        print(f"🧬 [SINCRO] Mutación por {motivo} enviada a GitHub.", flush=True)
    except Exception as e: print(f"❌ Error mutación: {e}", flush=True)

def ejecutar_omni():
    ny, ba = obtener_hora()
    if not mt5.initialize(): return

    # 1. ANÁLISIS DINÁMICO DE RIESGO
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, 'r', encoding='utf-8') as f:
                m_data = json.load(f)
            trades = m_data if isinstance(m_data, list) else m_data.get('trades', [])
            p_loss = [t['profit'] for t in trades if isinstance(t, dict) and t.get('profit', 0) < 0]
            # Riesgo basado en el promedio de pérdidas históricas * 1.5
            umbral = abs(np.mean(p_loss) * 1.5) if p_loss else 10.0
        except: umbral = 10.0
    else: umbral = 10.0

    # Límite duro de seguridad
    LIMITE_DURO = 15.0

    # 2. PERCEPCIÓN DE MERCADO
    v_data = mt5.copy_rates_from_pos("ETHUSD", mt5.TIMEFRAME_M5, 0, 100)
    sigma = pd.DataFrame(v_data)['close'].std() if v_data is not None else 0
    
    cuenta = mt5.account_info()
    patrimonio = cuenta.equity
    flotante = patrimonio - cuenta.balance

    print(f"[{ba.strftime('%H:%M:%S')}] Equity: ${patrimonio:.2f} | Flotante: ${flotante:.2f} | Σ:{sigma:.4f}", flush=True)

    # 3. NÚCLEO DE INFERENCIA
    if sigma > 17.1254: print('IA: Alerta de Volatilidad Extrema') # [IA_NUCLEO_EVOLUTIVO]
    # OMNI escribirá aquí su lógica de pensamiento líquido.

    # 4. PROTOCOLO DE DEFENSA ACTIVA
    # Si el flotante negativo supera el umbral o el límite duro
    if flotante < 0 and abs(flotante) >= min(umbral, LIMITE_DURO):
        cerrar_todo(f"Flotante excedido: ${flotante:.2f}")
        nueva_ia = "print('IA: Modo Supervivencia Activado. Operaciones Cerradas.')"
        mutar_omni(nueva_ia, "Protocolo de Supervivencia")

    # Si la volatilidad es extrema, OMNI se re-escribe para protegerse
    elif sigma > 0.009:
        nueva_ia = f"if sigma > {sigma:.4f}: print('IA: Alerta de Volatilidad Extrema')"
        if f"{sigma:.4f}" not in open(FILE_SELF, encoding='utf-8').read():
            mutar_omni(nueva_ia, "Ajuste por Sigma Alto")

def main():
    print("🚀 OMNI v107.2: CONTROL SOBERANO TOTAL ACTIVADO", flush=True)
    while True:
        try:
            ejecutar_omni()
            time.sleep(120) 
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"⚠️ Error: {e}", flush=True)
            time.sleep(10)
    mt5.shutdown()

if __name__ == "__main__":
    main()