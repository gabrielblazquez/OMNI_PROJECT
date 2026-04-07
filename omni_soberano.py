import datetime, pytz, requests, os, time, subprocess, winsound, json
import MetaTrader5 as mt5
import pandas as pd
import numpy as np

# --- IDENTIDAD SOBERANA ---
PATH_DATA = r"C:\OMNI_DATA"
FILE_SELF = __file__
FILE_MEMORIA = os.path.join(PATH_DATA, "omni_soberano.json")

def obtener_hora():
    try:
        r = requests.get("http://worldtimeapi.org/api/timezone/America/New_York", timeout=5)
        ny = datetime.datetime.fromisoformat(r.json()['datetime'])
    except:
        ny = datetime.datetime.now(pytz.timezone('America/New_York'))
    return ny, ny.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))

def mutar_omni(nueva_arquitectura, razon):
    """ OMNI reescribe su código y sincroniza con OMNI_PROJECT """
    try:
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        with open(FILE_SELF, 'w', encoding='utf-8') as f:
            for linea in lineas:
    print('MODO: Adaptación de Riesgo. Flotante actual: $-8.04') # [IA_NUCLEO_EVOLUTIVO]
    print('MODO: Adaptación de Riesgo. Flotante actual: $-8.04') # [IA_NUCLEO_EVOLUTIVO]
                else: f.write(linea)
        
        # Sincronización con GitHub
        subprocess.run(["git", "add", "."], shell=True)
        subprocess.run(["git", "commit", "-m", f"OMNI Evolucion: {razon}"], shell=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True)
        print(f"🧬 OMNI: Arquitectura redefinida por {razon}")
    except Exception as e:
        print(f"❌ Error en sinapsis: {e}")

def ejecutar_omni():
    ny, ba = obtener_hora()
    if not mt5.initialize(): return

    # 1. MEMORIA HISTÓRICA (Fix para el error 'list' object)
    riesgo_dinamico = 5.0
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, 'r', encoding='utf-8') as f:
                mem_data = json.load(f)
            # Si la memoria es una lista, la procesamos directamente
            trades = mem_data if isinstance(mem_data, list) else mem_data.get('trades', [])
            if trades:
                p_loss = [t['profit'] for t in trades if isinstance(t, dict) and t.get('profit', 0) < 0]
                if p_loss: riesgo_dinamico = abs(np.mean(p_loss) * 1.5)
        except Exception as e: print(f"⚠️ Error leyendo memoria: {e}")

    # 2. PERCEPCIÓN DE ENTROPÍA (Σ)
    v_data = mt5.copy_rates_from_pos("ETHUSD", mt5.TIMEFRAME_M5, 0, 100)
    sigma = pd.DataFrame(v_data)['close'].std() if v_data is not None else 0

    cuenta = mt5.account_info()
    patrimonio = cuenta.equity
    flotante = patrimonio - cuenta.balance
    
    print(f"\n" + "—"*65)
    print(f"🤖 OMNI v106.4 | BA: {ba.strftime('%H:%M:%S')} | Σ: {sigma:.6f}")
    print(f"[ESTADO] Equity: ${patrimonio:.2f} | Flotante: ${flotante:.2f}")

    # 3. NÚCLEO DE INFERENCIA
    print('MODO: Adaptación de Riesgo. Flotante actual: $-8.04') # [IA_NUCLEO_EVOLUTIVO]
    # OMNI escribirá su lógica aquí.

    # 4. AUTO-EDICIÓN PROACTIVA
    if abs(flotante) > riesgo_dinamico:
        winsound.Beep(1000, 400)
        nueva_ia = f"print('MODO: Adaptación de Riesgo. Flotante actual: ${flotante:.2f}')"
        mutar_omni(nueva_ia, "Desviación de Flotante")

def main():
    print("🚀 OMNI v106.4 SOBERANA: PENSAMIENTO LÍQUIDO (FIXED)")
    while True:
        try:
            ejecutar_omni()
            time.sleep(300) 
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"⚠️ Error de sistema: {e}")
            time.sleep(10)
    mt5.shutdown()

if __name__ == "__main__":
    main()