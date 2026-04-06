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
        r = requests.get("http://worldtimeapi.org/api/timezone/America/New_York", timeout=5)
        ny = datetime.datetime.fromisoformat(r.json()['datetime'])
    except:
        ny = datetime.datetime.now(pytz.timezone('America/New_York'))
    ba = ny.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))
    return ny, ba

def mutar_omni(nueva_logica, motivo):
    """ OMNI reescribe su propio código con codificación reforzada """
    try:
        # Forzamos encoding='utf-8' para evitar el error de 'charmap'
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        with open(FILE_SELF, 'w', encoding='utf-8') as f:
            for linea in lineas:
    print('IA: Defensa activa por Sigma 17.489743') # [IA_LOGICA_SOBERANA]
    print('IA: Defensa activa por Sigma 17.489743') # [IA_LOGICA_SOBERANA]
                else:
                    f.write(linea)
        
        subprocess.run(["git", "add", "."], shell=True)
        subprocess.run(["git", "commit", "-m", f"OMNI SOBERANO: {motivo}"], shell=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True)
        print(f"🧬 [SISTEMA] Mutación completada: {motivo}")
    except Exception as e:
        print(f"❌ Error en mutación: {e}")

def ejecutar_omni():
    ny, ba = obtener_hora()
    if not mt5.initialize(): return

    # 1. ANÁLISIS DE MEMORIA DINÁMICO
    umbral_dinamico = -5.0
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, 'r', encoding='utf-8') as f:
                data = json.load(f)
            trades = data.get('trades', [])
            drawdowns = [t['profit'] for t in trades if t.get('profit', 0) < 0]
            if drawdowns: umbral_dinamico = np.mean(drawdowns) * 2
        except: pass

    # 2. PERCEPCIÓN DE VOLATILIDAD
    v_data = mt5.copy_rates_from_pos("ETHUSD", mt5.TIMEFRAME_M5, 0, 100)
    sigma = pd.DataFrame(v_data)['close'].std() if v_data is not None else 0

    cuenta = mt5.account_info()
    patrimonio = cuenta.equity
    balance = cuenta.balance
    flotante_actual = patrimonio - balance

    print(f"\n" + "—"*65)
    print(f"🤖 OMNI v106.1 | Σ: {sigma:.6f} | Umbral de Dolor: {umbral_dinamico:.2f}")
    print(f"[ESTADO] Equity: ${patrimonio:.2f} | Flotante: ${flotante_actual:.2f}")

    # 3. NÚCLEO DE AUTOPROGRAMACIÓN
    print('IA: Defensa activa por Sigma 17.489743') # [IA_LOGICA_SOBERANA]
    # OMNI insertará aquí su razonamiento puro.

    # 4. MOTOR DE INFERENCIA
    if flotante_actual < umbral_dinamico:
        winsound.Beep(1000, 500)
        # Verificamos el contenido actual con utf-8 para decidir si mutamos
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            if f"{sigma:.6f}" not in f.read():
                mutar_omni(f"print('IA: Defensa activa por Sigma {sigma:.6f}')", "Ajuste Estadístico")

def main():
    print("🚀 OMNI v106.1: AUTONOMÍA PROBABILÍSTICA (ENCODING FIX)")
    while True:
        try:
            ejecutar_omni()
            time.sleep(300)
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(10)
    mt5.shutdown()

if __name__ == "__main__":
    main()