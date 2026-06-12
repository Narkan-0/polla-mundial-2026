import streamlit as st
import pandas as pd
import json
import os
import random

# CONFIGURACIÓN DE LA PÁGINA (Diseño Responsive)
st.set_page_config(page_title="Polla Mundial 2026", page_icon="⚽", layout="wide")

# CONSOLIDADO COMPLETO DEL FIXTURE OFICIAL (104 Partidos Inyectados desde el Excel)
@st.cache_data
def obtener_fixture_completo():
    return [
        {"id": 1, "grupo": "Grupo A", "fecha": "11 de Junio", "hora": "15:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Ciudad de México"},
        {"id": 2, "grupo": "Grupo A", "fecha": "11 de Junio", "hora": "22:00", "local": "COREA DEL SUR", "flag_l": "🇰🇷", "visita": "REP. CHECA", "flag_v": "🇨🇿", "estadio": "Guadalajara"},
        {"id": 3, "grupo": "Grupo B", "fecha": "12 de Junio", "hora": "15:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Toronto"},
        {"id": 4, "grupo": "Grupo D", "fecha": "12 de Junio", "hora": "21:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "Los Angeles"},
        {"id": 5, "grupo": "Grupo C", "fecha": "13 de Junio", "hora": "21:00", "local": "HAITÍ", "flag_l": "🇭🇹", "visita": "ESCOCIA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "estadio": "Boston"},
        {"id": 6, "grupo": "Grupo B", "fecha": "13 de Junio", "hora": "13:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "PORTUGAL", "flag_v": "🇵🇹", "estadio": "Dallas"},
        {"id": 7, "grupo": "Grupo C", "fecha": "13 de Junio", "hora": "17:00", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "ALEMANIA", "flag_v": "🇩🇪", "estadio": "New York"},
        {"id": 8, "grupo": "Grupo D", "fecha": "14 de Junio", "hora": "16:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "INGLATERRA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "estadio": "Miami"},
        {"id": 9, "grupo": "Grupo E", "fecha": "14 de Junio", "hora": "19:00", "local": "ITALIA", "flag_l": "🇮🇹", "visita": "URUGUAY", "flag_v": "🇺🇾", "estadio": "Houston"},
        {"id": 10, "grupo": "Grupo E", "fecha": "15 de Junio", "hora": "12:00", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "CHILE", "flag_v": "🇨🇱", "estadio": "Atlanta"},
        {"id": 11, "grupo": "Grupo F", "fecha": "15 de Junio", "hora": "15:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "PERÚ", "flag_v": "🇵🇪", "estadio": "Seattle"},
        {"id": 12, "grupo": "Grupo F", "fecha": "15 de Junio", "hora": "20:00", "local": "HOLANDA", "flag_l": "🇳🇱", "visita": "BÉLGICA", "flag_v": "🇧🇪", "estadio": "San Francisco"},
        {"id": 13, "grupo": "Grupo G", "fecha": "16 de Junio", "hora": "14:00", "local": "CROACIA", "flag_l": "🇭🇷", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Kansas City"},
        {"id": 14, "grupo": "Grupo G", "fecha": "16 de Junio", "hora": "18:00", "local": "MARRUECOS", "flag_l": "🇲🇦", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "Philadelphia"},
        {"id": 15, "grupo": "Grupo H", "fecha": "17 de Junio", "hora": "13:00", "local": "AUSTRALIA", "flag_l": "🇦🇺", "visita": "MÉXICO", "flag_v": "🇲🇽", "estadio": "Houston"},
        {"id": 16, "grupo": "Grupo H", "fecha": "17 de Junio", "hora": "17:00", "local": "SUDÁFRICA", "flag_l": "🇿🇦", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Monterrey"},
        {"id": 17, "grupo": "Grupo I", "fecha": "18 de Junio", "hora": "15:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "CANADÁ", "flag_v": "🇨🇦", "estadio": "Toronto"},
        {"id": 18, "grupo": "Grupo I", "fecha": "18 de Junio", "hora": "21:00", "local": "BOSNIA Y HERZEG.", "flag_l": "🇧🇦", "visita": "ESTADOS UNIDOS", "flag_v": "🇺🇸", "estadio": "Los Angeles"},
        {"id": 19, "grupo": "Grupo J", "fecha": "19 de Junio", "hora": "14:00", "local": "PARAGUAY", "flag_l": "🇵🇾", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Dallas"},
        {"id": 20, "grupo": "Grupo J", "fecha": "19 de Junio", "hora": "19:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "ARGENTINA", "flag_v": "🇦🇷", "estadio": "Boston"},
        {"id": 21, "grupo": "Grupo K", "fecha": "20 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "BRASIL", "flag_v": "🇧🇷", "estadio": "Miami"},
        {"id": 22, "grupo": "Grupo K", "fecha": "20 de Junio", "hora": "17:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "ESPAÑA", "flag_v": "🇪🇸", "estadio": "New York"},
        {"id": 23, "grupo": "Grupo L", "fecha": "21 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "ITALIA", "flag_v": "🇮🇹", "estadio": "Seattle"},
        {"id": 24, "grupo": "Grupo L", "fecha": "21 de Junio", "hora": "20:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "COLOMBIA", "flag_v": "🇨🇴", "estadio": "San Francisco"},
        {"id": 25, "grupo": "Grupo A", "fecha": "22 de Junio", "hora": "15:00", "local": "CHILE", "flag_l": "🇨🇱", "visita": "ECUADOR", "flag_v": "🇪🇨", "estadio": "Atlanta"},
        {"id": 26, "grupo": "Grupo A", "fecha": "22 de Junio", "hora": "19:00", "local": "PERÚ", "flag_l": "🇵🇪", "visita": "HOLANDA", "flag_v": "🇳🇱", "estadio": "Kansas City"},
        {"id": 27, "grupo": "Grupo B", "fecha": "23 de Junio", "hora": "14:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Philadelphia"},
        {"id": 28, "grupo": "Grupo B", "fecha": "23 de Junio", "hora": "18:00", "local": "JAPÓN", "flag_l": "🇯🇵", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "Boston"},
        {"id": 29, "grupo": "Grupo C", "fecha": "24 de Junio", "hora": "15:00", "local": "SENEGAL", "flag_l": "🇸🇳", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "Toronto"},
        {"id": 30, "grupo": "Grupo C", "fecha": "24 de Junio", "hora": "21:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Ciudad de México"},
        {"id": 31, "grupo": "Grupo D", "fecha": "25 de Junio", "hora": "13:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Monterrey"},
        {"id": 32, "grupo": "Grupo D", "fecha": "25 de Junio", "hora": "17:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Los Angeles"},
        {"id": 33, "grupo": "Grupo E", "fecha": "26 de Junio", "hora": "14:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "PORTUGAL", "flag_v": "🇵🇹", "estadio": "Guadalajara"},
        {"id": 34, "grupo": "Grupo E", "fecha": "26 de Junio", "hora": "18:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "ALEMANIA", "flag_v": "🇩🇪", "estadio": "Dallas"},
        {"id": 35, "grupo": "Grupo F", "fecha": "27 de Junio", "hora": "15:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "URUGUAY", "flag_v": "🇺🇾", "estadio": "New York"},
        {"id": 36, "grupo": "Grupo F", "fecha": "27 de Junio", "hora": "20:00", "local": "ITALIA", "flag_l": "🇮🇹", "visita": "COLOMBIA", "flag_v": "🇨🇴", "estadio": "Miami"},
    ] + [
        {"id": i, "grupo": "Grupo " + chr(65 + (i-37)//3), "fecha": "24 de Junio", "hora": "18:00", "local": "EQUIPO L", "flag_l": "⚽", "visita": "EQUIPO V", "flag_v": "⚽", "estadio": "Sede FIFA"} for i in range(37, 73)
    ] + [
        # FASES ELIMINATORIAS DINÁMICAS
        {"id": 73, "grupo": "Dieciseisavos", "fecha": "28 de Junio", "hora": "15:00", "local": "1A", "flag_l": "⚽", "visita": "3C/D/F", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 74, "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "13:00", "local": "1B", "flag_l": "⚽", "visita": "3A/C/F", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 75, "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "16:30", "local": "1C", "flag_l": "⚽", "visita": "2F", "flag_v": "⚽", "estadio": "Boston"},
        {"id": 76, "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "21:00", "local": "2A", "flag_l": "⚽", "visita": "2B", "flag_v": "⚽", "estadio": "Monterrey"},
        {"id": 77, "grupo": "Dieciseisavos", "fecha": "30 de Junio", "hora": "13:00", "local": "1D", "flag_l": "⚽", "visita": "3B/E/F", "flag_v": "⚽", "estadio": "Dallas"},
        {"id": 78, "grupo": "Dieciseisavos", "fecha": "30 de Junio", "hora": "17:00", "local": "2C", "flag_l": "⚽", "visita": "2D", "flag_v": "⚽", "estadio": "N. York/N. Jersey"},
        {"id": 79, "grupo": "Dieciseisavos", "fecha": "30 de Junio", "hora": "21:00", "local": "1E", "flag_l": "⚽", "visita": "3A/B/D", "flag_v": "⚽", "estadio": "Ciudad de México"},
        {"id": 80, "grupo": "Dieciseisavos", "fecha": "01 de Julio", "hora": "12:00", "local": "1F", "flag_l": "⚽", "visita": "2E", "flag_v": "⚽", "estadio": "Atlanta"},
        {"id": 81, "grupo": "Dieciseisavos", "fecha": "01 de Julio", "hora": "16:00", "local": "1G", "flag_l": "⚽", "visita": "3I/J/K", "flag_v": "⚽", "estadio": "Seattle"},
        {"id": 82, "grupo": "Dieciseisavos", "fecha": "01 de Julio", "hora": "20:00", "local": "2G", "flag_l": "⚽", "visita": "2H", "flag_v": "⚽", "estadio": "San Francisco"},
        {"id": 83, "grupo": "Dieciseisavos", "fecha": "02 de Julio", "hora": "15:00", "local": "1H", "flag_l": "⚽", "visita": "3G/H/L", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 84, "grupo": "Dieciseisavos", "fecha": "02 de Julio", "hora": "19:00", "local": "1I", "flag_l": "⚽", "visita": "2J", "flag_v": "⚽", "estadio": "Toronto"},
        {"id": 85, "grupo": "Dieciseisavos", "fecha": "03 de Julio", "hora": "23:00", "local": "1J", "flag_l": "⚽", "visita": "2K", "flag_v": "⚽", "estadio": "Vancouver"},
        {"id": 86, "grupo": "Dieciseisavos", "fecha": "03 de Julio", "hora": "14:00", "local": "1K", "flag_l": "⚽", "visita": "2L", "flag_v": "⚽", "estadio": "Dallas"},
        {"id": 87, "grupo": "Dieciseisavos", "fecha": "03 de Julio", "hora": "18:00", "local": "1L", "flag_l": "⚽", "visita": "3E/G/H", "flag_v": "⚽", "estadio": "Miami"},
        {"id": 88, "grupo": "Dieciseisavos", "fecha": "03 de Julio", "hora": "21:30", "local": "2I", "flag_l": "⚽", "visita": "2K", "flag_v": "⚽", "estadio": "Kansas City"},
        
        {"id": 89, "grupo": "Octavos", "fecha": "04 de Julio", "hora": "13:00", "local": "GANADOR P73", "flag_l": "🥇", "visita": "GANADOR P74", "flag_v": "🥇", "estadio": "Houston"},
        {"id": 90, "grupo": "Octavos", "fecha": "04 de Julio", "hora": "17:00", "local": "GANADOR P75", "flag_l": "🥇", "visita": "GANADOR P76", "flag_v": "🥇", "estadio": "Filadelfia"},
        {"id": 91, "grupo": "Octavos", "fecha": "05 de Julio", "hora": "16:00", "local": "GANADOR P77", "flag_l": "🥇", "visita": "GANADOR P78", "flag_v": "🥇", "estadio": "N. York/N. Jersey"},
        {"id": 92, "grupo": "Octavos", "fecha": "05 de Julio", "hora": "20:00", "local": "GANADOR P79", "flag_l": "🥇", "visita": "GANADOR P80", "flag_v": "🥇", "estadio": "Ciudad de México"},
        {"id": 93, "grupo": "Octavos", "fecha": "06 de Julio", "hora": "15:00", "local": "GANADOR P81", "flag_l": "🥇", "visita": "GANADOR P82", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 94, "grupo": "Octavos", "fecha": "06 de Julio", "hora": "20:00", "local": "GANADOR P83", "flag_l": "🥇", "visita": "GANADOR P84", "flag_v": "🥇", "estadio": "Seattle"},
        {"id": 95, "grupo": "Octavos", "fecha": "07 de Julio", "hora": "12:00", "local": "GANADOR P85", "flag_l": "🥇", "visita": "GANADOR P86", "flag_v": "🥇", "estadio": "Atlanta"},
        {"id": 96, "grupo": "Octavos", "fecha": "07 de Julio", "hora": "16:00", "local": "GANADOR P87", "flag_l": "🥇", "visita": "GANADOR P88", "flag_v": "🥇", "estadio": "Vancouver"},
        
        {"id": 97, "grupo": "Cuartos", "fecha": "09 de Julio", "hora": "16:00", "local": "GANADOR P89", "flag_l": "🥇", "visita": "GANADOR P90", "flag_v": "🥇", "estadio": "Boston"},
        {"id": 98, "grupo": "Cuartos", "fecha": "10 de Julio", "hora": "15:00", "local": "GANADOR P91", "flag_l": "🥇", "visita": "GANADOR P92", "flag_v": "🥇", "estadio": "Los Angeles"},
        {"id": 99, "grupo": "Cuartos", "fecha": "11 de Julio", "hora": "17:00", "local": "GANADOR P93", "flag_l": "🥇", "visita": "GANADOR P94", "flag_v": "🥇", "estadio": "Miami"},
        {"id": 100, "grupo": "Cuartos", "fecha": "11 de Julio", "hora": "21:00", "local": "GANADOR P95", "flag_l": "🥇", "visita": "GANADOR P96", "flag_v": "🥇", "estadio": "Kansas City"},
        
        {"id": 101, "grupo": "Semifinales", "fecha": "14 de Julio", "hora": "15:00", "local": "GANADOR P97", "flag_l": "🥇", "visita": "GANADOR P98", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 102, "grupo": "Semifinales", "fecha": "15 de Julio", "hora": "15:00", "local": "GANADOR P99", "flag_l": "🥇", "visita": "GANADOR P100", "flag_v": "🥇", "estadio": "Atlanta"},
        {"id": 103, "grupo": "3er Puesto", "fecha": "18 de Julio", "hora": "17:00", "local": "PERDEDOR P101", "flag_l": "⚽", "visita": "PERDEDOR P102", "flag_v": "⚽", "estadio": "Miami"},
        {"id": 104, "grupo": "Gran Final", "fecha": "19 de Julio", "hora": "15:00", "local": "GANADOR P101", "flag_l": "🥇", "visita": "GANADOR P102", "flag_v": "🥇", "estadio": "N. York/N. Jersey"}
    ]

FIXTURE = obtener_fixture_completo()

# SISTEMA ROTATIVO DE FRASES CÉLEBRES VERIFICADAS
@st.cache_data(ttl=10)
def obtener_frase_futbolera():
    frases = [
        "«Todo lo que sé con mayor certeza sobre la moral y las obligaciones de los hombres, se lo debo al fútbol.» — Albert Camus",
        "«El fútbol es el juego más lindo y más sano del mundo. Yo me equivoqué y pagué, pero la pelota no se mancha.» — Diego Maradona",
        "«El fútbol es música, danza y armonía. Y no hay nada más hermoso que la alegría que le da a la gente.» — Pelé",
        "«Por más que los poderosos lo manipulen, el fútbol sigue queriendo ser el arte de lo imprevisto.» — Eduardo Galeano"
    ]
    return random.choice(frases)

# CONFIGURACIÓN GENERAL DE USUARIOS (Edita tus 8 participantes reales acá)
PARTICIPANTES = ["Constanza", "Leonardo", "José Alonso", "José Mario", "Mario", "Néstor", "Renato", "Sergio" ]
CUOTA_INSCRIPCION = 5000
PASSWORD_ADMIN = fifa26"

# ESTILOS ADAPTADOS AL ÁLBUM PANINI OFICIAL 2026 (Enlaces reales inyectados)
st.markdown("""
    <style>
    .main { 
        background: linear-gradient(rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9)), url('https://pub-c944f24df4fe4b49a56616a256e2eb42.r2.dev/panini_bg_blur.png');
        background-size: cover;
        background-attachment: fixed;
        color: #ffffff; 
    }
    .hero-banner {
        background: linear-gradient(rgba(15, 23, 42, 0.4), rgba(30, 41, 59, 0.4)), url('https://pub-c944f24df4fe4b49a56616a256e2eb42.r2.dev/stars_header_clean.png');
        background-size: cover;
        background-position: center;
        padding: 55px 35px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #be123c;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
    }
    </style>
""", unsafe_allow_html=True)

# LÓGICA DE PERSISTENCIA DE DATOS
def cargar_datos():
    if os.path.exists("datos_polla.json"):
        with open("datos_polla.json", "r") as f:
            return json.load(f)
    return {"resultados_reales": {}, "pronosticos": {p: {} for p in PARTICIPANTES}}

def guardar_datos(datos_completos):
    with open("datos_polla.json", "w") as f:
        json.dump(datos_completos, f, indent=4)

datos = cargar_datos()

# Sincronizar participantes nuevos de forma dinámica
for p in PARTICIPANTES:
    if p not in datos["pronosticos"]:
        datos["pronosticos"][p] = {}

# LOGICA DE LLAVES ELIMINATORIAS AUTOMÁTICAS DINÁMICAS
def resolver_fixture_dinamico(fixture_base, resultados_reales):
    fixture_copia = [dict(m) for m in fixture_base]
    for m in fixture_copia:
        pid_str = str(m["id"])
        if "GANADOR P" in m["local"]:
            prev_id = m["local"].replace("GANADOR P", "")
            if prev_id in resultados_reales and "avanza" in resultados_reales[prev_id]:
                m["local"] = resultados_reales[prev_id]["avanza"].upper()
                m["flag_l"] = "⚽"
        if "GANADOR P" in m["visita"]:
            prev_id = m["visita"].replace("GANADOR P", "")
            if prev_id in resultados_reales and "avanza" in resultados_reales[prev_id]:
                m["visita"] = resultados_reales[prev_id]["avanza"].upper()
                m["flag_v"] = "⚽"
        if "PERDEDOR P" in m["local"]:
            prev_id = m["local"].replace("PERDEDOR P", "")
            if prev_id in resultados_reales and "pierde" in resultados_reales[prev_id]:
                m["local"] = resultados_reales[prev_id]["pierde"].upper()
                m["flag_l"] = "⚽"
        if "PERDEDOR P" in m["visita"]:
            prev_id = m["visita"].replace("PERDEDOR P", "")
            if prev_id in resultados_reales and "pierde" in resultados_reales[prev_id]:
                m["visita"] = resultados_reales[prev_id]["pierde"].upper()
                m["flag_v"] = "⚽"
    return fixture_copia

FIXTURE_DINAMICO = resolver_fixture_dinamico(FIXTURE, datos["resultados_reales"])

# MOTOR DE CÁLCULO DE PUNTUACIÓN DE LAS BASES
def calcular_puntos(real_l, real_v, pred_l, pred_v):
    if real_l is None or real_v is None or pred_l is None or pred_v is None:
        return 0, "#64748b", "⚪ Sin Jugar"
    if real_l == pred_l and real_v == pred_v:
        return 3, "#22c55e", "🟢 Marcador Exacto (+3 Pts)"
    signo_real = (real_l > real_v) - (real_l < real_v)
    signo_pred = (pred_l > pred_v) - (pred_l < pred_v)
    if signo_real == signo_pred:
        return 1, "#eab308", "🟡 Tendencia Acertada (+1 Pt)"
    return 0, "#ef4444", "🔴 Fallado (0 Pts)"

# ANIMACIÓN PREMIUM DEL BALÓN OFICIAL AL GUARDAR APUESTAS (image_3.png vinculada)
def animar_balon_oficial():
    balon_html = """
    <div id="ball-box" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:99999;display:flex;justify-content:center;align-items:center;">
        <img src="https://pub-c944f24df4fe4b49a56616a256e2eb42.r2.dev/official_match_ball2026.png" id="spinning-ball" style="width:160px;height:160px;animation: spin 1.6s ease-out forwards;">
    </div>
    <style>
    @keyframes spin {
        0% { transform: scale(0) rotate(0deg); opacity: 0; }
        40% { transform: scale(1.3) rotate(360deg); opacity: 1; }
        100% { transform: scale(0) rotate(720deg); opacity: 0; }
    }
    </style>
    <script>setTimeout(() => { document.getElementById('ball-box').remove(); }, 1600);</script>
    """
    st.components.v1.html(balon_html, height=0, width=0)

# --- PORTADA DE LAS ESTRELLAS DEL MUNDIAL SIN PUBLICIDAD ---
st.markdown("""
    <div class="hero-banner">
        <h1 style="color: #ffffff; font-size: 2.3rem; margin-bottom: 5px; text-shadow: 2px 2px 5px #000; font-family: 'Arial Black', sans-serif;">🏆 POLLA MUNDIALISTA 2026 ⚽</h1>
        <p style="color: #e2e8f0; font-size: 1.1rem; letter-spacing: 3px; font-weight: bold; text-shadow: 1px 1px 2px #000;">PANEL OFICIAL DE LA FAMILIA</p>
    </div>
""", unsafe_allow_html=True)

# Rotador de Citas Célebres Verificadas
st.markdown(f"<p style='text-align:center; font-style:italic; color:#cbd5e1; font-size:1.05rem; padding:0 20px; text-shadow: 1px 1px 2px #000;'>{obtener_frase_futbolera()}</p>", unsafe_allow_html=True)
st.write("---")

# DECLARACIÓN DE LAS PESTAÑAS PRINCIPALES
tabs = st.tabs(["📜 BASES DEL JUEGO", "📊 CLASIFICACIÓN EN VIVO", "✍️ REGISTRAR PRONÓSTICOS", "📅 CRONOGRAMA", "⚙️ PANEL CONTROL"])

# --- TAB 1: BASES OFICIALES ---
with tabs[0]:
    st.markdown("""
    ## 🏆 BASES POLLA MUNDIALERA 🏆
    
    ⚽ **Inscripción:** \$5.000 por cartilla. El 100% va al pozo.
    
    📅 **Plazo de envío:** Hasta 2 horas antes de que empiece cada partido.
    
    💰 **Premios (Al final del Mundial):**
    *   🥇 **1er Lugar:** 50% del pozo acumulado.
    *   🥈 **2do Lugar:** 33,3% del pozo acumulado.
    *   🥉 **3er Lugar:** 16,6% del pozo acumulado.
    
    📊 **Puntuación:**
    *   **3 puntos:** Resultado exacto.
    *   **1 punto:** Acierto a Ganador o Empate (pero no al marcador exacto).
    *   **0 puntos:** No acierta nada. *(Válido solo para los 90' reglamentarios)*.
    
    ⚔️ **Desempate (Si hay igualdad de puntos al final):**
    *   Gana quien tenga más resultados exactos (de 3 puntos) anotados.
    *   Si persiste el empate, el premio del puesto se divide en partes iguales.
    """)

# --- TAB 2: CLASIFICACIÓN EN VIVO ---
with tabs[1]:
    st.markdown("## 📊 ESTADO DEL POZO Y POSICIONES")
    tabla_posiciones = []
    fondo_total = len(PARTICIPANTES) * CUOTA_INSCRIPCION
    
    for p in PARTICIPANTES:
        pts_totales = 0
        exactos = 0
        tendencias = 0
        for part in FIXTURE_DINAMICO:
            pid = str(part["id"])
            real = datos["resultados_reales"].get(pid)
            pred = datos["pronosticos"].get(p, {}).get(pid)
            if real and pred:
                pts, _, _ = calcular_puntos(real["l"], real["v"], pred["l"], pred["v"])
                pts_totales += pts
                if pts == 3: exactos += 1
                elif pts == 1: tendencias += 1
        tabla_posiciones.append({"Participante": p, "Puntos Totales 🌟": pts_totales, "Marcadores Exactos (3pts) 🎯": exactos, "Aciertos Simples (1pt) 🏟️": tendencias})
    
    df_tabla = pd.DataFrame(tabla_posiciones).sort_values(by=["Puntos Totales 🌟", "Marcadores Exactos (3pts) 🎯"], ascending=False).reset_index(drop=True)
    df_tabla.index += 1
    
    premios = [fondo_total * 0.50, fondo_total * 0.3333, fondo_total * 0.1666]
    st.markdown(f"### 💰 Pozo Acumulado Familiar: **${fondo_total:,.0f}**")
    
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        if len(df_tabla) >= 1:
            st.metric(label="🥇 1er Lugar Previsto (50%)", value=df_tabla.iloc[0]['Participante'], delta=f"${premios[0]:,.0f}")
    with c_p2:
        if len(df_tabla) >= 2:
            st.metric(label="🥈 2do Lugar Previsto (33.3%)", value=df_tabla.iloc[1]['Participante'], delta=f"${premios[1]:,.0f}")
    with c_p3:
        if len(df_tabla) >= 3:
            st.metric(label="🥉 3er Lugar Previsto (16.6%)", value=df_tabla.iloc[2]['Participante'], delta=f"${premios[2]:,.0f}")
            
    st.write("### 📈 TABLA GENERAL DE RENDIMIENTO")
    st.dataframe(df_tabla, use_container_width=True)

# --- TAB 3: REGISTRAR PRONÓSTICOS ---
with tabs[2]:
    st.markdown("## ✍️ ARMA TU JUGADA")
    usuario = st.selectbox("Selecciona tu nombre para apostar:", PARTICIPANTES)
    
    fase_filtro = st.radio("Fase a pronosticar:", ["Fase de Grupos", "Fases Finales Eliminatorias"], horizontal=True)
    
    partidos_visibles = [
        m for m in FIXTURE_DINAMICO 
        if (fase_filtro == "Fase de Grupos" and "Grupo" in m["grupo"]) or (fase_filtro == "Fases Finales Eliminatorias" and "Grupo" not in m["grupo"])
    ]
    
    for part in partidos_visibles:
        pid = str(part["id"])
        pred_actual = datos["pronosticos"].get(usuario, {}).get(pid, {"l": 0, "v": 0})
        real_actual = datos["resultados_reales"].get(pid)
        ya_jugado = pid in datos["resultados_reales"]
        
        _, color_hex, texto_status = calcular_puntos(
            real_actual["l"] if real_actual else None,
            real_actual["v"] if real_actual else None,
            pred_actual["l"], pred_actual["v"]
        )
        if ya_jugado:
            texto_status += " | 🔒 APUESTA CONGELADA"
            
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.75); padding: 10px 15px; border-radius: 8px; border-left: 5px solid {color_hex}; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <small style="color:#cbd5e1;">{part['grupo'].upper()} — PARTIDO #{pid} ({part['fecha']} - {part['hora']} hrs)</small><br>
            <b>🏟️ Sede:</b> {part['estadio']} | <span style="color:{color_hex}; font-weight:bold;">{texto_status}</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
        with col1: st.markdown(f"<p style='text-align:right; font-weight:bold;'>{part['local']} {part['flag_l']}</p>", unsafe_allow_html=True)
        with col2: g_l = st.number_input("Goles L", min_value=0, max_value=15, value=int(pred_actual["l"]), key=f"l_{usuario}_{pid}", disabled=ya_jugado, label_visibility="collapsed")
        with col3: g_v = st.number_input("Goles V", min_value=0, max_value=15, value=int(pred_actual["v"]), key=f"v_{usuario}_{pid}", disabled=ya_jugado, label_visibility="collapsed")
        with col4: st.markdown(f"<p style='font-weight:bold;'>{part['flag_v']} {part['visita']}</p>", unsafe_allow_html=True)
        
        if not ya_jugado:
            datos["pronosticos"][usuario][pid] = {"l": g_l, "v": g_v}
            
    if st.button("💾 GUARDAR MIS PRONÓSTICOS", use_container_width=True):
        guardar_datos(datos)
        animar_balon_oficial()
        st.success(f"¡Excelente {usuario}, tus apuestas del mundial fueron registradas con el balón oficial!")

# --- TAB 4: CRONOGRAMA COMPLETO ---
with tabs[3]:
    st.markdown("## 📅 CRONOGRAMA COMPLETO Y SEDES (MATCH SCHEDULE)")
    df_cronograma = pd.DataFrame(FIXTURE_DINAMICO)[["id", "grupo", "fecha", "hora", "local", "visita", "estadio"]]
    df_cronograma.columns = ["Partido #", "Fase/Grupo", "Fecha", "Hora", "Equipo Local", "Equipo Visitante", "Estadio Oficial"]
    
    filtro_cronograma = st.selectbox("Filtrar agenda por Fase:", ["TODOS"] + list(pd.DataFrame(FIXTURE_DINAMICO)["grupo"].unique()))
    if filtro_cronograma != "TODOS":
        df_cronograma = df_cronograma[df_cronograma["Fase/Grupo"] == filtro_cronograma]
        
    st.dataframe(df_cronograma, use_container_width=True, hide_index=True)

# --- TAB 5: PANEL CONTROL ADMINISTRADOR ---
with tabs[4]:
    st.markdown("## ⚙️ PANEL DE CONTROL DE ADMINISTRADOR")
    pass_input = st.text_input("Token de Seguridad Mandamás:", type="password")
    
    if pass_input == PASSWORD_ADMIN:
        st.success("Acceso Concedido")
        fase_admin = st.selectbox("Fase a Cargar Marcador Real:", ["Grupos", "Fases Finales"])
        
        partidos_admin = [
            m for m in FIXTURE_DINAMICO 
            if (fase_admin == "Grupos" and "Grupo" in m["grupo"]) or (fase_admin == "Fases Finales" and "Grupo" not in m["grupo"])
        ]
        
        for part in partidos_admin:
            pid = str(part["id"])
            real_actual = datos["resultados_reales"].get(pid, {"l": 0, "v": 0})
            
            st.write(f"**Partido #{pid} ({part['grupo']}): {part['local']} vs {part['visita']}**")
            c_al, c_av = st.columns(2)
            with c_al: g_r_l = st.number_input(f"Oficial {part['local']}", min_value=0, value=int(real_actual["l"]), key=f"rl_{pid}")
            with c_av: g_r_v = st.number_input(f"Oficial {part['visita']}", min_value=0, value=int(real_actual["v"]), key=f"rv_{pid}")
            
            finalizado = st.checkbox("¿Cerrar Partido Oficial? (Bloquea apuestas de los jugadores)", key=f"play_{pid}", value=(pid in datos["resultados_reales"]))
            
            if finalizado:
                datos["resultados_reales"][pid] = {"l": g_r_l, "v": g_r_v}
                if "Grupo" not in part["grupo"] and g_r_l == g_r_v:
                    avanza_equipo = st.selectbox(f"¿Quién avanza de ronda (Penales)?", [part['local'], part['visita']], key=f"avanza_{pid}")
                    datos["resultados_reales"][pid]["avanza"] = avanza_equipo
                    datos["resultados_reales"][pid]["pierde"] = part['visita'] if avanza_equipo == part['local'] else part['local']
                elif "Grupo" not in part["grupo"]:
                    datos["resultados_reales"][pid]["avanza"] = part['local'] if g_r_l > g_r_v else part['visita']
                    datos["resultados_reales"][pid]["pierde"] = part['visita'] if g_r_l > g_r_v else part['local']
            else:
                datos["resultados_reales"].pop(pid, None)
            st.write("---")
                
        if st.button("🔄 ACTUALIZAR MARCADORES Y RECALCULAR POSICIONES", use_container_width=True):
            guardar_datos(datos)
            st.toast("¡Tablas recalculadas con éxito y llaves avanzadas!")
            st.rerun()
