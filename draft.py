import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Purealign - Portal de Consulta y Cotización",
    page_icon="🦷",
    layout="wide"
)

# --- ESTILOS CSS (DISEÑO LIMPIO Y TARJETAS FIJAS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f7fc;
    }
    h1, h2, h3 {
        color: #3CE2E2 !important;
        font-weight: 700;
    }
    p, li, label, .streamlit-expanderHeader {
        color: #4A3E93 !important;
    }
    
    .card-box {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 12px;
        border: 2px solid #e3e0f5;
        box-shadow: 0 4px 12px rgba(108, 91, 194, 0.05);
        margin-bottom: 20px;
        min-height: 580px;
        height: 580px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .card-content {
        flex-grow: 1;
        overflow-y: auto;
    }
    
    div.row-widget.stRadio div[role="radiogroup"] label p {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #4A3E93 !important;
    }
    
    div.row-widget.stRadio > label {
        font-size: 19px !important;
        font-weight: 700 !important;
    }
    
    .stRadio > div {
        gap: 12px;
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .desglose-box {
        background-color: #f1effa;
        border-left: 5px solid #6C5BC2;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .total-destacado {
        color: #6C5BC2;
        font-size: 26px;
        font-weight: bold;
    }
    
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dcd7f2;
        padding: 15px;
        border-radius: 10px;
    }

    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .logo-img {
        width: 75px;
        height: 75px;
        border-radius: 10px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS ---
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def conectar_google_sheets():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_credenciales = os.path.join(directorio_actual, "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_credenciales, SCOPE)
    client = gspread.authorize(creds)
    return client.open("Purealign_DB_Trabajo")

try:
    db = conectar_google_sheets()
    sheet_tratamientos = db.worksheet("Tratamientos")
    sheet_creditos = db.worksheet("Creditos")
    sheet_adicionales = db.worksheet("Adicionales")
    sheet_pacientes = db.worksheet("Pacientes")

    df_tratamientos = pd.DataFrame(sheet_tratamientos.get_all_records())
    df_creditos = pd.DataFrame(sheet_creditos.get_all_records())
    df_adicionales = pd.DataFrame(sheet_adicionales.get_all_records())
    df_pacientes = pd.DataFrame(sheet_pacientes.get_all_records())
except Exception as e:
    # Valores por defecto si no hay conexión activa para pruebas locales
    df_adicionales = pd.DataFrame([
        {"Producto": "Botella de Limpieza para Alineadores", "Precio": 250},
        {"Producto": "Contenedor / Caja para Alineadores", "Precio": 180},
        {"Producto": "Kit de Retenedores Post-Tratamiento", "Precio": 1200}
    ])
    df_pacientes = pd.DataFrame()

# --- ENCABEZADO CON LOGOTIPO NÍTIDO ---
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "WhatsApp Image 2026-10-26 at 12.04.44 PM.jpeg")

if os.path.exists(logo_path):
    import base64
    with open(logo_path, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
        <div class="header-container">
            <img src="data:image/jpeg;base64,{encoded_img}" class="logo-img">
            <div>
                <h1 style="margin: 0; padding: 0; line-height: 1.1;">Purealign - Portal de Consulta y Cotización</h1>
                <p style="margin: 5px 0 0 0; color: #4A3E93; font-weight: 500;">Sistema inteligente de cálculo de paquetes y control de órdenes (HD Ortodoncia).</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("Purealign - Portal de Consulta y Cotización")
    st.markdown("Sistema inteligente de cálculo de paquetes y control de órdenes (HD Ortodoncia).")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN SUPERIOR: REGISTRO (IZQ) Y CALCULADORA INTELIGENTE (DER)
# ==============================================================================
col_sec1, col_sec2 = st.columns([3, 2])

with col_sec1:
    st.markdown('<hr style="border: 2px solid #3CE2E2; margin-top: 10px; margin-bottom: 10px;">', unsafe_allow_html=True)
    
    st.subheader("👤 Registro de Paciente y Selección de Paquete")
    
    nombre_paciente = st.text_input("Nombre Completo del Paciente")
    
    opciones_paquete = [
        "10 Alineadores (Precio Normal)",
        "15 Alineadores (Precio Normal)",
        "1 a 20 Alineadores (Plan Pure Basic + Seguro)",
        "21 a 40 Alineadores (Plan Pure Extended + Seguro)"
    ]
    
    paquete_seleccionado = st.radio("Selecciona la modalidad requerida:", opciones_paquete)

    if "10 Alineadores" in paquete_seleccionado:
        cant_alineadores_num = 10
    elif "15 Alineadores" in paquete_seleccionado:
        cant_alineadores_num = 15
    elif "Pure Basic" in paquete_seleccionado:
        cant_alineadores_num = st.number_input("Cantidad exacta de alineadores (1 a 20):", min_value=1, max_value=20, value=20, step=1)
        if cant_alineadores_num == 20:
            st.info("💡 ¿Requieres más de 20 alineadores? Te recomendamos seleccionar el **Plan Pure Extended**.")
    else:
        cant_alineadores_num = st.number_input("Cantidad exacta de alineadores (21 a 40):", min_value=21, max_value=40, value=21, step=1)

    # --- LÓGICA FINANCIERA Y DE TOKENS ---
    precio_final = 0.0
    rango_paquete = ""
    contenido_paquete = ""
    tokens_consumidos = 0

    if "10 Alineadores" in paquete_seleccionado:
        precio_final = 5200.0
        rango_paquete = "10 Alineadores Individuales ($520 c/u)"
        contenido_paquete = "⚠️ **Esquema Individual:** Cobro por unidad ($520 MXN). Sin sets de refinamiento extra ni planeaciones."
        tokens_consumidos = 10  # 1 token por alineador, sin tokens de seguro/planeación
    elif "15 Alineadores" in paquete_seleccionado:
        precio_final = 7800.0
        rango_paquete = "15 Alineadores Individuales ($520 c/u)"
        contenido_paquete = "⚠️ **Esquema Individual:** Cobro por unidad ($520 MXN). Sin sets de refinamiento extra ni planeaciones."
        tokens_consumidos = 15  # 1 token por alineador, sin tokens de seguro/planeación
    elif "Pure Basic" in paquete_seleccionado:
        costo_linea = cant_alineadores_num * 670.0
        seguro_basic = 2560.0
        precio_final = costo_linea + seguro_basic
        rango_paquete = f"{cant_alineadores_num} Alineadores (Plan Pure Basic)"
        # linea_costo = f"💲 **Costo Alineadores ({cant_alineadores_num} x $670):** ${costo_linea:,.2f} MXN<br><br>"
        linea_seguro = f"🛡️ **Seguro Pure Basic:** $2,560.00 MXN<br><br>"
        linea_sets = "✔️ **12 Sets de refinamiento extra** incluidos<br><br>"
        linea_planeacion = "✔️ **1 Planeación digital** incluida"
        
        contenido_paquete = linea_sets + linea_planeacion
        tokens_consumidos = cant_alineadores_num + 5  # Alineadores + 5 tokens fijos por seguro/planeación
    elif "Pure Extended" in paquete_seleccionado:
        costo_linea = cant_alineadores_num * 640.0
        seguro_extended = 4250.0
        precio_final = costo_linea + seguro_extended
        rango_paquete = f"{cant_alineadores_num} Alineadores (Plan Pure Extended)"
        # linea_costo = f"💲 **Costo Alineadores ({cant_alineadores_num} x $640):** ${costo_linea:,.2f} MXN<br><br>"
        linea_seguro = f"🛡️ **Seguro Pure Extended:** $4,250.00 MXN<br><br>"
        linea_sets = "✔️ **25 Sets de refinamiento extra** incluidos<br><br>"
        linea_planeacion = "✔️ **1 Planeación digital** incluida"
        
        contenido_paquete = linea_seguro + linea_sets + linea_planeacion
        tokens_consumidos = cant_alineadores_num + 5  # Alineadores + 5 tokens fijos por seguro/planeación

    st.markdown('</div></div>', unsafe_allow_html=True)

with col_sec2:
    st.markdown('<hr style="border: 2px solid #3CE2E2; margin-top: 10px; margin-bottom: 10px;">', unsafe_allow_html=True)
    
    st.subheader("📊 Resumen y Desglose Inteligente")
    
    st.markdown(f"""
    * **Paciente:** {nombre_paciente if nombre_paciente else '*Pendiente de ingresar*'}
    * **Modalidad:** `{paquete_seleccionado}`
    * **Cantidad de alineadores:** {cant_alineadores_num}
    """)
    
    st.markdown(f"""
    <div class="desglose-box">
        <h4 style="color: #6C5BC2; margin-top:0;">📦 Cobertura del Paquete</h4>
        <p><b>Rango:</b> {rango_paquete}</p>
        {contenido_paquete}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**SUBTOTAL PACIENTE:** <span class='total-destacado'>${precio_final:,.0f} MXN</span>", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN MEDIA: TOKENS Y PRODUCTOS ADICIONALES (CON CONTADOR)
# ==============================================================================
col_mid1, col_mid2 = st.columns([2, 3])

with col_mid1:
    st.markdown('<hr style="border: 2px solid #3CE2E2; margin-top: 10px; margin-bottom: 10px;">', unsafe_allow_html=True)
   
    st.subheader("📦 Tokens Disponibles")
    
    # Bolsa inicial de 100 tokens de consulta
    tokens_totales_iniciales = 100
    tokens_restantes = tokens_totales_iniciales - tokens_consumidos
    
    st.metric(label="Bolsa de Tokens", value=f"{tokens_restantes} / {tokens_totales_iniciales}", delta=f"-{tokens_consumidos} para esta orden", delta_color="inverse")
    st.markdown(f"<p style='font-size: 14px; margin-top: 10px;'>ℹ️ Cada alineador equivale a 1 token. Los planes con seguro e inclusión de planeación consumen 5 tokens adicionales.</p>", unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

with col_mid2:
    st.markdown('<hr style="border: 2px solid #3CE2E2; margin-top: 10px; margin-bottom: 10px;">', unsafe_allow_html=True)
    
    st.subheader("🛍️ Productos Adicionales (Conteo y Precios)")
    
    total_adicionales = 0.0
    if not df_adicionales.empty:
        for idx, row in df_adicionales.iterrows():
            prod_nombre = row["Producto"]
            prod_precio = float(row["Precio"])
            
            # Fila interactiva con contador numérico de cantidad por producto
            col_prod1, col_prod2 = st.columns([2, 1])
            with col_prod1:
                st.markdown(f"<p style='margin-top: 8px; font-weight: 500;'>{prod_nombre} (${prod_precio:,.0f} c/u)</p>", unsafe_allow_html=True)
            with col_prod2:
                cantidad_prod = st.number_input(f"Cant_{idx}", min_value=0, max_value=20, value=0, step=1, label_visibility="collapsed", key=f"qty_{idx}")
            
            total_adicionales += (prod_precio * cantidad_prod)
    else:
        st.warning("No hay productos adicionales configurados.")
        
    total_general = precio_final + total_adicionales
    
    st.markdown("---")
    st.markdown(f"**Subtotal Adicionales:** ${total_adicionales:,.0f} MXN")
    st.markdown(f"### 💳 Total a Consultar: <span class='total-destacado'>${total_general:,.0f} MXN</span>", unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN INFERIOR: TABLA HISTÓRICA DE PACIENTES (SOLO CONSULTA)
# ==============================================================================
st.markdown('<hr style="border: 2px solid #3CE2E2; margin-top: 10px; margin-bottom: 10px;">', unsafe_allow_html=True)
st.subheader("📋 Historial de Pacientes y Cotizaciones Registradas")
st.markdown("Consulta en tiempo real sincronizada con Google Sheets.")

if not df_pacientes.empty:
    st.dataframe(df_pacientes, use_container_width=True, hide_index=True)
else:
    st.info("No hay órdenes registradas aún en Google Sheets.")