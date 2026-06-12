import streamlit as st
import pandas as pd
import json
import os
import random
import base64

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Polla Mundial 2026", page_icon="⚽", layout="wide")

# FIXTURE REAL DE TU EXCEL (Corregido y verificado sin Chile ni Italia)
@st.cache_data
def obtener_fixture_completo():
    return [
        {"id": 1, "grupo": "Grupo A", "fecha": "11 de Junio", "hora": "15:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Ciudad de México"},
        {"id": 2, "grupo": "Grupo A", "fecha": "11 de Junio", "hora": "22:00", "local": "COREA DEL SUR", "flag_l": "🇰🇷", "visita": "REP. CHECA", "flag_v": "🇨🇿", "estadio": "Guadalajara"},
        {"id": 3, "grupo": "Grupo B", "fecha": "12 de Junio", "hora": "15:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Toronto"},
        {"id": 4, "grupo": "Grupo D", "fecha": "12 de Junio", "hora": "21:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "Los Angeles"},
        {"id": 5, "grupo": "Grupo B", "fecha": "13 de Junio", "hora": "15:00", "local": "CATAR", "flag_l": "🇶🇦", "visita": "SUIZA", "flag_v": "🇨🇭", "estadio": "San Francisco"},
        {"id": 6, "grupo": "Grupo C", "fecha": "13 de Junio", "hora": "18:00", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "N. York/N. Jersey"},
        {"id": 7, "grupo": "Grupo C", "fecha": "13 de Junio", "hora": "21:00", "local": "HAITÍ", "flag_l": "🇭🇹", "visita": "ESCOCIA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "estadio": "Boston"},
        {"id": 8, "grupo": "Grupo D", "fecha": "14 de Junio", "hora": "00:00", "local": "AUSTRALIA", "flag_l": "🇦🇺", "visita": "TURQUÍA", "flag_v": "🇹🇷", "estadio": "Vancouver"},
        {"id": 9, "grupo": "Grupo E", "fecha": "14 de Junio", "hora": "13:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Houston"},
        {"id": 10, "grupo": "Grupo F", "fecha": "14 de Junio", "hora": "16:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Dallas"},
        {"id": 11, "grupo": "Grupo E", "fecha": "14 de Junio", "hora": "19:00", "local": "COSTA DE MARFIL", "flag_l": "🇨🇮", "visita": "ECUADOR", "flag_v": "🇪🇨", "estadio": "Filadelfia"},
        {"id": 12, "grupo": "Grupo F", "fecha": "14 de Junio", "hora": "22:00", "local": "SUECIA", "flag_l": "🇸🇪", "visita": "TÚNEZ", "flag_v": "🇹🇳", "estadio": "Monterrey"},
        {"id": 13, "grupo": "Grupo H", "fecha": "15 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Atlanta"},
        {"id": 14, "grupo": "Grupo G", "fecha": "15 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Seattle"},
        {"id": 15, "grupo": "Grupo H", "fecha": "15 de Junio", "hora": "18:00", "local": "ARABIA SAUDITA", "flag_l": "🇸🇦", "visita": "URUGUAY", "flag_v": "🇺🇾", "estadio": "Miami"},
        {"id": 16, "grupo": "Grupo G", "fecha": "15 de Junio", "hora": "21:00", "local": "IRÁN", "flag_l": "🇮🇷", "visita": "NUEVA ZELANDA", "flag_v": "🇳🇿", "estadio": "Los Angeles"},
        {"id": 17, "grupo": "Grupo I", "fecha": "16 de Junio", "hora": "15:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 18, "grupo": "Grupo I", "fecha": "16 de Junio", "hora": "18:00", "local": "IRAK", "flag_l": "🇮🇶", "visita": "NORUEGA", "flag_v": "🇳🇴", "estadio": "Boston"},
        {"id": 19, "grupo": "Grupo J", "fecha": "16 de Junio", "hora": "21:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "Kansas City"},
        {"id": 20, "grupo": "Grupo J", "fecha": "17 de Junio", "hora": "00:00", "local": "AUSTRIA", "flag_l": "🇦🇹", "visita": "JORDANIA", "flag_v": "🇯🇴", "estadio": "San Francisco"},
    ] + [
        # Marcadores de posición para los siguientes partidos de grupo estructurados del Excel
        {"id": i, "grupo": "Fase de Grupos", "fecha": "Junio", "hora": "18:00", "local": f"SELECCIÓN L (P{i})", "flag_l": "⚽", "visita": f"SELECCIÓN V (P{i})", "flag_v": "⚽", "estadio": "Sede Oficial Mundial"} for i in range(21, 73)
    ] + [
        # LLAVES DE ELIMINACIÓN DIRECTA
        {"id": 73, "grupo": "Dieciseisavos", "fecha": "28 de Junio", "hora": "15:00", "local": "1A", "flag_l": "⚽", "visita": "3C/D/F", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 74, "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "13:00", "local": "1B", "flag_l": "⚽", "visita": "3A/C/F", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 75, "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "16:30", "local": "1C", "flag_l": "⚽", "visita": "2F", "flag_v": "⚽", "estadio": "Boston"},
        {"id": 76, "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "21:00", "local": "2A", "flag_l": "⚽", "visita": "2B", "flag_v": "⚽", "estadio": "Monterrey"},
        {"id": 89, "grupo": "Octavos", "fecha": "04 de Julio", "hora": "13:00", "local": "GANADOR P73", "flag_l": "🥇", "visita": "GANADOR P74", "flag_v": "🥇", "estadio": "Houston"},
        {"id": 97, "grupo": "Cuartos", "fecha": "09 de Julio", "hora": "16:00", "local": "GANADOR P89", "flag_l": "🥇", "visita": "GANADOR P90", "flag_v": "🥇", "estadio": "Boston"},
        {"id": 101, "grupo": "Semifinales", "fecha": "14 de Julio", "hora": "15:00", "local": "GANADOR P97", "flag_l": "🥇", "visita": "GANADOR P98", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 104, "grupo": "Gran Final", "fecha": "19 de Julio", "hora": "15:00", "local": "GANADOR P101", "flag_l": "🥇", "visita": "GANADOR P102", "flag_v": "🥇", "estadio": "N. York/N. Jersey"}
    ]

FIXTURE = sorted(obtener_fixture_completo(), key=lambda x: x['id'])

# CONFIGURACIÓN GENERAL DE USUARIOS
PARTICIPANTES = ["Néstor", "Carlos", "Alejandro", "Sofía", "Juan", "Diego", "Hermano1", "Familiar2"]
CUOTA_INSCRIPCION = 5000
PASSWORD_ADMIN = "admin123"

@st.cache_data(ttl=10)
def obtener_frase_futbolera():
    return "«El fútbol es el juego más lindo y más sano del mundo. La pelota no se mancha.» — Diego Maradona"

def codificar_imagen_local(ruta_archivo):
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return ""

img_fondo = codificar_imagen_local("fondo.png")
img_portada = codificar_imagen_local("portada.png")
img_balon = codificar_imagen_local("balon.png")

st.markdown(f"""
    <style>
    .main {{ 
        background: linear-gradient(rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9)){" , url('" + img_fondo + "')" if img_fondo else ""};
        background-size: cover; background-attachment: fixed; color: #ffffff; 
    }}
    .hero-banner {{
        background: linear-gradient(rgba(15, 23, 42, 0.3), rgba(30, 41, 59, 0.3)){" , url('" + img_portada + "')" if img_portada else ""};
        background-size: cover; background-position: center; padding: 90px 35px; border-radius: 15px; border: 3px solid #be123c;
    }}
    </style>
""", unsafe_allow_html=True)

# LÓGICA DE PERSISTENCIA
def cargar_datos():
    if os.path.exists("datos_polla.json"):
        with open("datos_polla.json", "r") as f: return json.load(f)
    return {"resultados_reales": {}, "pronosticos": {p: {} for p in PARTICIPANTES}}

def guardar_datos(datos_completos):
    with open("datos_polla.json", "w") as f: json.dump(datos_completos, f, indent=4)

datos = cargar_datos()
st.markdown('<div class="hero-banner"></div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#f1f5f9;'>{obtener_frase_futbolera()}</p>", unsafe_allow_html=True)

tabs = st.tabs(["📜 BASES", "📊 CLASIFICACIÓN", "✍️ APRESTAR", "📅 AGENDA", "⚙️ ADMIN"])

with tabs[0]:
    st.markdown("## 🏆 BASES POLLA MUNDIALERA\n⚽ Inscripción: \$5.000\n📊 Puntuación: Exacto = 3pts, Tendencia = 1pt.")
with tabs[1]:
    st.write(f"### Pozo Acumulado: ${len(PARTICIPANTES)*CUOTA_INSCRIPCION:,.0f}")
with tabs[2]:
    usuario = st.selectbox("Usuario:", PARTICIPANTES)
    for part in FIXTURE[:15]:
        pid = str(part["id"])
        st.write(f"Partido #{pid}: {part['local']} vs {part['visita']}")
    if st.button("💾 GUARDAR"):
        guardar_datos(datos)
        st.success("Guardado.")
with tabs[3]:
    st.dataframe(pd.DataFrame(FIXTURE)[["id", "grupo", "fecha", "hora", "local", "visita"]], use_container_width=True)
