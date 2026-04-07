import datetime, pytz, requests, os, time, subprocess, winsound, json
import MetaTrader5 as mt5
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE NÚCLEO ---
PATH_DATA = r"C:\OMNI_DATA"
FILE_SELF = __file__
FILE_MEMORIA = os.path.join(PATH_DATA, "omni_soberano.json")

def obtener_hora():
    """ Reloj interno para evitar tildes en la HP G42 """
    try:
        ny = datetime.datetime.now(pytz.timezone('America/New_York'))
        ba = ny.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))
        return ny, ba
    except:
        now = datetime.datetime.now()
        return now, now

def mutar_omni(nueva_logica, motivo):
    """ OMNI se auto-edita asegurando la sangría de 4 espacios """
    try:
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        with open(FILE_SELF, 'w', encoding='utf-8') as f:
            for linea in lineas:
    print('ESTADO: Defendiendo Equity. Flotante actual: $-10.71') # [IA_NUCLEO_EVOLUTIVO]
                    # Forzamos los 4 espacios de sangría para evitar IndentationError
    print('ESTADO: Defendiendo Equity. Flotante actual: $-10.71') # [IA_NUCLEO_EVOLUTIVO]
                else:
                    f.write(linea)
        
        print(f"🧬 [MUTACIÓN] {motivo}", flush=True)
        # Sincronización con OMNI_PROJECT
        subprocess.run(["git", "add", "."], shell=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"OMNI Evolucion: {motivo}"], shell=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True, capture_output=True)
    except Exception as e:
        print(f"❌ Fallo en sinapsis: {e}", flush=True)

def ejecutar_omni():
    ny, ba = obtener_hora()
    if not mt5.initialize(): return

    # 1. ANÁLISIS DE MEMORIA
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, 'r', encoding='utf-8') as f:
                m_data = json.load(f)
            trades = m_data if isinstance(m_data, list) else m_data.get('trades', [])
            p_loss = [t['profit'] for t in trades if isinstance(t, dict) and t.get('profit', 0) < 0]
            umbral = abs(np.mean(p_loss) * 1.5) if p_loss else 10.0
        except: umbral = 10.0
    else: umbral = 10.0

    # 2. PERCEPCIÓN
    v_data = mt5.copy_rates_from_pos("ETHUSD", mt5.TIMEFRAME_M5, 0, 100)
    sigma = pd.DataFrame(v_data)['close'].std() if v_data is not None else 0
    
    cuenta = mt5.account_info()
    patrimonio = cuenta.equity
    flotante = patrimonio - cuenta.balance

    # INFO EN PANTALLA
    print(f"[{ba.strftime('%H:%M:%S')}] P:${patrimonio:.2f} | F:${flotante:.2f} | Σ:{sigma:.4f}", flush=True)

    # 3. NÚCLEO DE INFERENCIA
    print('ESTADO: Defendiendo Equity. Flotante actual: $-10.71') # [IA_NUCLEO_EVOLUTIVO]
    # OMNI escribirá aquí su lógica de pensamiento líquido.

    # 4. DISPARADORES DE AUTO-EDICIÓN
    if abs(flotante) > umbral:
        winsound.Beep(800, 500)
        nueva_ia = f"print('ESTADO: Defendiendo Equity. Flotante actual: ${flotante:.2f}')"
        if f"${flotante:.2f}" not in open(FILE_SELF, encoding='utf-8').read():
            mutar_omni(nueva_ia, "Defensa de Patrimonio")

def main():
    print("🚀 OMNI v107.1: NÚCLEO ARQUITECTÓNICO REPARADO", flush=True)
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