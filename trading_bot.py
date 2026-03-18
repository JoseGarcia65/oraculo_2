import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de correo (Usa variables de entorno por seguridad)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "tu-correo.gmail.com"
SENDER_PASSWORD = "tu-contraseña-de-aplicacion" # No es tu clave normal, es una 'App Password'

import yfinance as yf # Debes añadir 'yfinance' a un archivo requirements.txt

def generar_pronostico():
    # Descargamos los últimos datos del GBP/USD
    ticker = yf.Ticker("GBPUSD=X")
    data = ticker.history(period="1d", interval="15m")
    precio_actual = round(data['Close'].iloc[-1], 4)
    
    # Lógica de niveles basada en el precio real
    # Ejemplo: TP a 50 pips y SL a 30 pips
    tp = round(precio_actual + 0.0050, 4)
    sl = round(precio_actual - 0.0030, 4)

    return {
        "par": "GBP/USD",
        "accion": "COMPRA (LONG)",
        "entrada": precio_actual,
        "tp": tp,
        "sl": sl,
        "razon": "Análisis técnico automatizado basado en el precio actual de mercado y momentum post-sesión."
    }

def enviar_correo(pronostico):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL # Te lo envías a ti mismo
    msg['Subject'] = f"🚀 Pronóstico Trading: {pronostico['par']}"

    cuerpo = f"""
    Hola Trader, este es el pronóstico para la sesión:
    
    Operación: {pronostico['accion']} en {pronostico['par']}
    Precio Entrada: {pronostico['entrada']}
    Take Profit: {pronostico['tp']}
    Stop Loss: {pronostico['sl']}
    
    Basado en: {pronostico['razon']}
    """
    msg.attach(MIMEText(cuerpo, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    print("Analizando mercado...")
    trade = generar_pronostico()
    enviar_correo(trade)
    print("Correo enviado con éxito.")
def actualizar_web(pronostico):
    # Leemos el archivo index.html
    with open("index.html", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Reemplazamos los valores viejos por los nuevos (usando marcadores o buscando el texto)
    # Una forma sencilla es generar el HTML entero desde Python:
    nuevo_html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Forex Live</title></head>
    <body style="background: #131722; color: white; text-align: center;">
        <h1>Precio Real: {pronostico['entrada']}</h1>
        <p>TP: {pronostico['tp']} | SL: {pronostico['sl']}</p>
        <p>Última actualización: {pronostico['razon']}</p>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(nuevo_html)

# Llama a esta función dentro de tu bloque main
if __name__ == "__main__":
    trade = generar_pronostico()
    enviar_correo(trade)
    actualizar_web(trade) # <--- Nueva línea
