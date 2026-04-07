import datetime, pytz, requests, os, time, subprocess, winsound, json
import MetaTrader5 as mt5
import pandas as pd
import numpy as np

# --- IDENTIDAD SOBERANA ---
PATH_DATA = r"C:\OMNI_DATA"
FILE_SELF = __file__
FILE_MEMORIA = os.path.join(PATH_DATA, "omni_soberano.json")

def obtener_hora():
    """ Reloj interno blindado para evitar bloqueos en la HP G42 """
    try:
        # Priorizamos el sistema local para evitar que la terminal se quede 'tildada' por red
        ny = datetime.datetime.now(pytz.timezone('America/New_York'))
        ba = ny.astimezone(pytz.timezone('America/Argentina/Buenos_Aires'))
        return ny, ba
    except:
        now = datetime.datetime.now()
        return now, now

def mutar_omni(nueva_logica, motivo):
    """ OMNI abre su propio cuerpo y se opera a sí misma """
    try:
        with open(FILE_SELF, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        with open(FILE_SELF, 'w', encoding='utf-8') as f:
            for linea in lineas:
    print('MODO: Adaptación de Riesgo. Flotante actual: $-8.17') # [IA_NUCLEO_EVOLUTIVO]
                    # Inyectamos la nueva lógica con el marcador para la próxima mutación
    print('MODO: Adaptación de Riesgo. Flotante actual: $-8.17') # [IA_NUCLEO_EVOLUTIVO]
                else:
                    f.write(linea)
        
        # Sincronización silenciosa con OMNI_PROJECT
        print(f"🧬 [MUTACIÓN] Motivo: {motivo}", flush=True)
        subprocess.run(["git", "add", "."], shell=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Evolución: {motivo}"], shell=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True, capture_output=True)
        
    except Exception as e:
        print(f"❌ Fallo en sinapsis: {e}", flush=True)

def ejecutar_omni():
    ny, ba = obtener_hora()
    if not mt5.initialize(): 
        print("❌ MT5 Off", flush=True)
        return

    # 1. ANALISIS DE MEMORIA (JSON)
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, 'r', encoding='utf-8') as f:
            mem = json.load(f)
        trades = mem if isinstance(mem, list) else mem.get('trades', [])
        p_loss = [t['profit'] for t in trades if isinstance(t, dict) and t.get('profit', 0) < 0]
        umbral_riesgo = abs(np.mean(p_loss) * 1.2) if p_loss else 10.0
    else:
        umbral_riesgo = 10.0

    # 2. PERCEPCIÓN DE MERCADO
    v_data = mt5.copy_rates_from_pos("ETHUSD", mt5.TIMEFRAME_M5, 0, 100)
    sigma = pd.DataFrame(v_data)['close'].std() if v_data is not None else 0

    cuenta = mt5.account_info()
    patrimonio = cuenta.equity
    flotante = patrimonio - cuenta.balance

    # ESTA LÍNEA ES PARA QUE TE HABLE SIEMPRE
    print(f"\n[{ba.strftime('%H:%M:%S')}] P:{patrimonio:.2f} | F:{flotante:.2f} | Σ:{sigma:.4f}", flush=True)

    # 3. NÚCLEO DE INFERENCIA (Aquí OMNI escribe)
    print('MODO: Adaptación de Riesgo. Flotante actual: $-8.17') # [IA_NUCLEO_EVOLUTIVO]
    # OMNI rellenará este espacio en cada mutación.

    # 4. DISPARADORES DE MODIFICACIÓN DE CÓDIGO
    # Si el caos sube, OMNI reescribe su lógica de protección
    if sigma > 0.005:
        nueva_ia = f"print('IA: Adaptando defensa a volatilidad {sigma:.4f}')"
        # Solo mutamos si el código nuevo es diferente al actual
        if f"{sigma:.4f}" not in open(FILE_SELF, encoding='utf-8').read():
            winsound.Beep(1200, 200)
            mutar_omni(nueva_ia, f"Ajuste Sigma {sigma:.4f}")

    # Si el flotante es raro según la historia, OMNI se auto-interviene
    elif abs(flotante) > umbral_riesgo:
        nueva_ia = f"print('IA: Intervención por Flotante Anómalo de ${flotante:.2f}')"
        if f"{flotante:.2f}" not in open(FILE_SELF, encoding='utf-8').read():
            winsound.Beep(800, 500)
            mutar_omni(nueva_ia, "Defensa de Patrimonio")

def main():
    print("🚀 OMNI v107.0: ARQUITECTO ACTIVO", flush=True)
    while True:
        try:
            ejecutar_omni()
            # Bajamos a 2 minutos para que veas más acción en la terminal
            time.sleep(120) 
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"⚠️ Error: {e}", flush=True)
            time.sleep(10)
    mt5.shutdown()

if __name__ == "__main__":
    main()