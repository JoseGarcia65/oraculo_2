import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de correo (Usa variables de entorno por seguridad)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "tu-correo.gmail.com"
SENDER_PASSWORD = "tu-contraseña-de-aplicacion" # No es tu clave normal, es una 'App Password'

def generar_pronostico():
    # Aquí iría la lógica de conexión a la API de Forex
    # Por ahora, simulamos el análisis técnico de mañana
    datos = {
        "par": "EUR/USD",
        "accion": "VENTA (SHORT)",
        "entrada": "1.1470",
        "tp": "1.1390",
        "sl": "1.1520",
        "razon": "Divergencia Fed/BCE y aversión al riesgo por tensiones en Oriente Medio."
    }
    return datos

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