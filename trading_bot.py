import yfinance as yf
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

def generar_pronostico():
    # 1. Obtener datos reales de mercado
    ticker = yf.Ticker("EURUSD=X")
    data = ticker.history(period="2d", interval="1h")
    precio_actual = round(data['Close'].iloc[-1], 4)
    
    # 2. Lógica de Análisis (Simulada con tendencia de 2026)
    # Post-Fed: El dólar se debilita.
    accion = "COMPRA (LONG)"
    color_accion = "#26a69a" # Verde TradingView
    tp = 1.1650
    sl = 1.1495
    razon = "Debilidad persistente del USD tras la reunión de la Fed y soporte sólido en 1.1520."

    return {
        "par": "EUR/USD",
        "accion": accion,
        "color": color_accion,
        "precio": precio_actual,
        "tp": tp,
        "sl": sl,
        "razon": razon,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def enviar_correo(p):
    # Leemos los SECRETOS que configuramos en GitHub
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    if not sender_email or not sender_password:
        print("⚠️ No se enviará correo: Faltan las variables de entorno SENDER_EMAIL o SENDER_PASSWORD.")
        return

    destinatario = sender_email # Te lo envías a ti mismo
    asunto = f"🚀 SEÑAL {p['par']}: {p['accion']}"
    cuerpo = f"""
    Hola Trader,
    
    El bot ha detectado una oportunidad:
    - Acción: {p['accion']}
    - Precio Entrada: {p['precio']}
    - Take Profit: {p['tp']}
    - Stop Loss: {p['sl']}
    
    Motivo: {p['razon']}
    Actualizado a las {p['fecha']} UTC.
    """

    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = sender_email
    msg['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, destinatario, msg.as_string())
        print("✅ Correo enviado con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")

def actualizar_index_html(p):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Forex Intelligence Hub</title>
        <style>
            body {{ background-color: #131722; color: #d1d4dc; font-family: sans-serif; margin: 0; padding: 20px; }}
            .layout-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 20px; max-width: 1400px; margin: 0 auto; }}
            .card {{ background: #1e222d; border: 1px solid #434651; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.3); }}
            .signal-badge {{ background-color: {p['color']}; color: white; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 1.1rem; margin-bottom: 15px; text-transform: uppercase; }}
            .price {{ font-size: 3rem; color: #ffffff; font-family: monospace; margin: 10px 0; }}
            .chart-container {{ height: 500px; background: #1e222d; border: 1px solid #434651; border-radius: 12px; overflow: hidden; }}
            .btn-update {{ background: #2962ff; color: white; border: none; padding: 15px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 20px; }}
            .label {{ color: #787b86; font-size: 0.85rem; text-transform: uppercase; }}
            .value {{ font-weight: bold; font-size: 1.4rem; display: block; margin-top: 5px; }}
            @media (max-width: 900px) {{ .layout-grid {{ grid-template-columns: 1fr; }} }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center; margin-bottom:30px;">Forex Intelligence Hub 2026</h1>
        <div class="layout-grid">
            <div class="card">
                <div class="signal-badge">{p['accion']}</div>
                <h2 style="margin:0;">{p['par']}</h2>
                <div class="label" style="margin-top:10px;">Entrada</div>
                <div class="price">{p['precio']}</div>
                <div style="display: flex; justify-content: space-around; margin-top: 20px; border-top: 1px solid #434651; padding-top: 20px;">
                    <div><span class="label">TP</span><span class="value" style="color:#26a69a">{p['tp']}</span></div>
                    <div><span class="label">SL</span><span class="value" style="color:#ef5350">{p['sl']}</span></div>
                </div>
                <div style="text-align:left; background:#2a2e39; padding:15px; border-radius:8px; margin-top:20px; font-size:0.9rem;">
                    <strong>Análisis:</strong> {p['razon']}
                </div>
                <button id="updateBtn" class="btn-update" onclick="pedirToken()">🔄 ACTUALIZAR AHORA</button>
            </div>
            <div class="chart-container">
                <div id="tv_chart" style="height:100%;"></div>
                <script src="https://s3.tradingview.com/tv.js"></script>
                <script>
                    new TradingView.widget({{"autosize": true, "symbol": "FX:EURUSD", "interval": "60", "theme": "dark", "style": "1", "locale": "es", "container_id": "tv_chart"}});
                    async function pedirToken() {{
                        const token = prompt("Introduce tu Token de GitHub:");
                        if(!token) return;
                        const res = await fetch('https://api.github.com/repos/TU_USUARIO/TU_REPO/actions/workflows/main.yml/dispatches', {{
                            method: 'POST',
                            headers: {{ 'Authorization': `Bearer ${{token}}`, 'Accept': 'application/vnd.github.v3+json' }},
                            body: JSON.stringify({{ ref: 'main' }})
                        }});
                        if(res.ok) alert("🚀 ¡Bot despertado! Refresca en 1 minuto.");
                        else alert("❌ Error. Token inválido o configuración incorrecta.");
                    }}
                </script>
            </div>
        </div>
        <p style="text-align:center; font-size:0.7rem; color:#787b86; margin-top:20px;">Última actualización: {p['fecha']} UTC</p>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    datos = generar_pronostico()
    actualizar_index_html(datos)
    enviar_correo(datos)
