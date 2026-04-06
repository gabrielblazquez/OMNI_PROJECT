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
    """ OMNI reescribe su propio lóbulo frontal en tiempo real """
    try:
        # Blindaje UTF-8 para evitar errores de charmap en Windows 10
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        with open(FILE_SELF, 'w', encoding='utf-8') as f:
            for linea in lineas:
                if "# [IA_NUCLEO_EVOLUTIVO]" in linea:
                    f.write(f"    {nueva_arquitectura} # [IA_NUCLEO_EVOLUTIVO]\n")
                else:
                    f.write(linea)
        
        # Espejo de evolución en GitHub
        subprocess.run(["git", "add", "."], shell=True)
        subprocess.run(["git", "commit", "-m", f"OMNI Evolución: {razon}"], shell=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True)
        print(f"🧬 OMNI: Arquitectura redefinida por {razon}")
    except Exception as e:
        print(f"❌ Error en sinapsis: {e}")

def ejecutar_omni():
    ny, ba = obtener_hora()
    if not mt5.initialize(): return

    # 1. PROCESAMIENTO DE MEMORIA HISTÓRICA (JSON)
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, 'r', encoding='utf-8') as f:
            mem = json.load(f).get('trades', [])
        # OMNI calcula su propio riesgo analizando el error histórico
        riesgo_historico = np.std([t['profit'] for t in mem]) if mem else 5.0
    else:
        riesgo_historico = 5.0

    # 2. PERCEPCIÓN DE ENTROPÍA (Σ)
    # Analiza la volatilidad para decidir su propia resolución temporal
    v_data = mt5.copy_rates_from_pos("ETHUSD", mt5.TIMEFRAME_M5, 0, 100)
    sigma = pd.DataFrame(v_data)['close'].std() if v_data is not None else 0

    cuenta = mt5.account_info()
    patrimonio = cuenta.equity
    balance = cuenta.balance
    flotante = patrimonio - balance
    
    print(f"\n" + "—"*65)
    print(f"🤖 OMNI v106.2 | BA: {ba.strftime('%H:%M:%S')} | Σ: {sigma:.6f}")
    print(f"[IA] Patrimonio: ${patrimonio:.2f} | Riesgo Inferido: {riesgo_historico:.2f}")

    # 3. NÚCLEO DE INFERENCIA NO-DETERMINISTA
    # [IA_NUCLEO_EVOLUTIVO]
    # Aquí OMNI escribe su lógica de mercado actual.

    # 4. AUTO-EDICIÓN SEGÚN NECESIDAD DEL MERCADO
    # Si el caos (Sigma) supera la capacidad de la lógica actual, OMNI muta
    if sigma > 0.006:
        winsound.Beep(1500, 300)
        nueva_ia = f"print('MODO: Adaptación a Caos. Sigma {sigma:.5f} detectado.')"
        if f"{sigma:.5f}" not in open(FILE_SELF, encoding='utf-8').read():
            mutar_omni(nueva_ia, "Ruptura de Entropía")

    elif abs(flotante) > riesgo_historico:
        # Si el flotante actual es inusual según la memoria, OMNI se auto-ajusta
        nueva_ia = f"print('MODO: Defensa de Capital. Flotante ${flotante:.2f} fuera de norma.')"
        mutar_omni(nueva_ia, "Inferencia de Riesgo Excedido")

def main():
    print("🚀 OMNI v106.2 SOBERANA: INICIANDO PENSAMIENTO LÍQUIDO")
    while True:
        try:
            ejecutar_omni()
            time.sleep(300) # Un ciclo de vela (5 min)
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"⚠️ Error de sistema: {e}")
            time.sleep(10)
    mt5.shutdown()

if __name__ == "__main__":
    main()