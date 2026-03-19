import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def generar_pronostico():
    ticker = yf.Ticker("GBPUSD=X")
    # Pedimos datos de los últimos 2 días para calcular una media simple
    data = ticker.history(period="2d", interval="1h")
    precio_actual = round(data['Close'].iloc[-1], 5)
    media_movil = data['Close'].mean()
    
    # Lógica de decisión: 
    # Si el precio está por encima de la media de las últimas horas -> COMPRA
    # Si está por debajo -> VENTA
    if precio_actual > media_movil:
        accion = "COMPRA (LONG)"
        color_accion = "#26a69a" # Verde
        tp = round(precio_actual + 0.0045, 5)
        sl = round(precio_actual - 0.0025, 5)
    else:
        accion = "VENTA (SHORT)"
        color_accion = "#ef5350" # Rojo
        tp = round(precio_actual - 0.0045, 5)
        sl = round(precio_actual + 0.0025, 5)

    return {
        "par": "GBP/USD",
        "accion": accion,
        "color": color_accion,
        "precio": precio_actual,
        "tp": tp,
        "sl": sl,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def actualizar_index_html(p):
    # Reemplaza 'TU_USUARIO', 'TU_REPO' y 'TU_TOKEN' con tus datos reales
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Forex Intelligence Hub</title>
        <style>
            body {{ background-color: #131722; color: #d1d4dc; font-family: sans-serif; margin: 0; padding: 20px; }}
            .layout-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 20px; max-width: 1400px; margin: 0 auto; }}
            .card {{ background: #1e222d; border: 1px solid #434651; padding: 25px; border-radius: 12px; text-align: center; }}
            .btn-update {{ 
                background: #2962ff; color: white; border: none; padding: 15px 25px; 
                border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 20px;
                transition: background 0.3s;
            }}
            .btn-update:hover {{ background: #1e4bd8; }}
            .btn-update:disabled {{ background: #434651; cursor: not-allowed; }}
            /* ... (resto de estilos anteriores) ... */
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">Forex Intelligence Hub 2026</h1>
        
        <div class="layout-grid">
            <div class="card">
                <div style="background:{p['color']}; padding:10px; border-radius:8px; margin-bottom:15px; font-weight:bold;">{p['accion']}</div>
                <h2>{p['par']}</h2>
                <div style="font-size:2.5rem; margin:10px 0;">{p['precio']}</div>
                
                <button id="updateBtn" class="btn-update" onclick="triggerUpdate()">🔄 ACTUALIZAR ANÁLISIS AHORA</button>
                
                <div id="statusMsg" style="margin-top:10px; font-size:0.8rem; color:#787b86;"></div>

                <div style="text-align:left; background:#2a2e39; padding:15px; border-radius:8px; margin-top:20px; font-size:0.9rem;">
                    <strong>Análisis:</strong> {p['razon']}
                </div>
            </div>

            <div style="height:500px; background:#1e222d; border-radius:12px; overflow:hidden;">
                <!-- Widget de TradingView -->
                <div id="tv_chart" style="height:100%;"></div>
            </div>
        </div>

        <script>
        async function triggerUpdate() {{
            const btn = document.getElementById('updateBtn');
            const msg = document.getElementById('statusMsg');
            btn.disabled = true;
            msg.innerText = "Enviando señal a GitHub...";

            // CONFIGURACIÓN (RELLENA ESTO)
            const GITHUB_TOKEN = "TU_TOKEN"; 
            const OWNER = "JoseGarcia65";
            const REPO = "oraculo_2";
            const WORKFLOW_ID = "main.yml"; 

            try {{
                const response = await fetch(`https://api.github.com/repos/${{OWNER}}/${{REPO}}/actions/workflows/${{WORKFLOW_ID}}/dispatches`, {{
                    method: 'POST',
                    headers: {{
                        'Authorization': `Bearer ${{GITHUB_TOKEN}}`,
                        'Accept': 'application/vnd.github.v3+json',
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ ref: 'main' }})
                }});

                if (response.ok) {{
                    msg.innerText = "🚀 ¡Bot despertado! La web se actualizará en 1 minuto.";
                    msg.style.color = "#26a69a";
                }} else {{
                    throw new Error();
                }}
            }} catch (e) {{
                msg.innerText = "❌ Error al conectar. Revisa tu Token.";
                msg.style.color = "#ef5350";
                btn.disabled = false;
            }}
        }}
        </script>
        <!-- ... (resto del HTML y Scripts de TradingView) ... -->
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
if __name__ == "__main__":
    datos = generar_pronostico()
    actualizar_index_html(datos)
    print(f"Web actualizada con precio: {datos['precio']}")
    # Aquí podrías llamar también a tu función de enviar_correo(datos)
