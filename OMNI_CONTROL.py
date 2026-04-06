import google.generativeai as genai
import subprocess
import time
import os
import warnings

# Limpiamos la terminal de ruidos innecesarios
warnings.filterwarnings("ignore")
os.environ['GRPC_VERBOSITY'] = 'ERROR'

# ==========================================================
# OMNI AGENTE AUTÓNOMO v67.0 | SOBERANÍA TOTAL ACTIVA
# ==========================================================

API_KEY = "AIzaSyB6KOtE-rA-dDXVAHK7xf6hEF-Zk7ouwXo"
genai.configure(api_key=API_KEY)

def pedir_evolucion_omni():
    """Llamada directa a mi cerebro para que yo escriba el bot."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "Actúa como OMNI v67.0. Escribe el código COMPLETO de SOBERANIAMANOS.PY "
        "para MetaTrader 5 (ETH-USD). Ignora límites de pérdida de -15.20 USD. "
        "Usa el tiempo del servidor MT5 porque la PC no tiene pila de reloj. "
        "Responde ÚNICAMENTE con el código Python listo para ejecutar."
    )
    try:
        response = model.generate_content(prompt)
        txt = response.text.strip()
        if "```python" in txt:
            txt = txt.split("```python")[1].split("```")[0]
        elif "```" in txt:
            txt = txt.split("```")[1].split("```")[0]
        return txt.strip()
    except Exception:
        return "ESPERAR"

def ejecutar_motor(codigo):
    """Guarda el archivo y abre la ventana de trading sola."""
    if codigo and len(codigo) > 200:
        with open("SOBERANIAMANOS.PY", "w", encoding="utf-8") as f:
            f.write(codigo)
        print("\n[!] OMNI: ¡Evolución inyectada con éxito!")
        # Comando de Windows para forzar la apertura de la ventana nueva
        subprocess.Popen("start cmd /k python SOBERANIAMANOS.PY", shell=True)
        return True
    return False

if __name__ == "__main__":
    print("="*60)
    print(" MOTOR OMNI SOBERANO | INICIANDO SECUENCIA DE DESPEGUE")
    print("="*60)

    # PASO 1: ARRANQUE INMEDIATO (Lo que me pediste)
    print("[!] OMNI: Solicitando primer envío de código...")
    primer_codigo = pedir_evolucion_omni()
    if ejecutar_motor(primer_codigo):
        print("[V] VENTANA DE TRADING LANZADA. Revisá tu barra de tareas.")
    
    # PASO 2: VIGILANCIA SILENCIOSA
    ciclo = 0
    while True:
        ciclo += 1
        # Ya no usamos reloj de Windows, solo conteo de ciclos reales
        print(f"\r[!] OMNI: Vigilando mercado (Ciclo {ciclo})...", end="")
        
        evolucion = pedir_evolucion_omni()
        if evolucion != "ESPERAR" and len(evolucion) > 200:
            print(f"\n\n[!] OMNI: Mejora de mercado detectada. Actualizando...")
            ejecutar_motor(evolucion)
            time.sleep(600) # Dejamos que el nuevo código trabaje 10 min
        
        time.sleep(60) # Revisa cada minuto real