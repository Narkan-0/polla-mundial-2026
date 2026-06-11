import streamlit as st
import pandas as pd
import json
import os

# CONFIGURACIÓN DE LA PÁGINA (Diseño Ultra Moderno)
st.set_page_config(page_title="Polla Mundial 2026", page_icon="⚽", layout="wide")

# ESTILOS CSS AVANZADOS PARA DISEÑO VISTOSO
st.markdown("""
    <style>
    .main { 
        background: linear-gradient(135px, #0f172a 0%, #1e1b4b 100%);
        color: #ffffff; 
    }
    .hero-banner {
        background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(15,23,42,0.4)), url('https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #be123c;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    h1, h2, h3 {
        font-family: 'Arial Black', Gadget, sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .card-partino { 
        background: rgba(30, 41, 59, 0.7);
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        border: 1px solid #334155;
    }
    .podio-box {
        background: linear-gradient(185px, #1e293b 0%, #0f172a 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border-top: 5px solid #eab308;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 1. CONFIGURACIÓN GENERAL
PARTICIPANTES = ["Néstor", "Constanza", "Leonardo", "Renato", "Sergio", "José Mario", "José Alonso", "Mario" ]
CUOTA_INSCRIPCION = 5000
PASSWORD_ADMIN = "admin123"

@st.cache_data
def obtener_fixture():
    return [
        {"id": 1, "grupo": "A", "fecha": "11 Junio", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "SUDÁFRICA", "flag_v": "🇿🇦"},
        {"id": 2, "grupo": "A", "fecha": "11 Junio", "local": "COREA DEL SUR", "flag_l": "🇰🇷", "visita": "REP. CHECA", "flag_v": "🇨🇿"},
        {"id": 3, "grupo": "B", "fecha": "12 Junio", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦"},
    ]

FIXTURE = obtener_fixture()

def cargar_datos():
    if os.path.exists("datos_polla.json"):
        with open("datos_polla.json", "r") as f:
            return json.load(f)
    return {"resultados_reales": {}, "pronosticos": {p: {} for p in PARTICIPANTES}}

def guardar_datos(datos):
    with open("datos_polla.json", "w") as f:
        json.dump(datos, f, indent=4)

datos = cargar_datos()

def calcular_puntos(real_l, real_v, pred_l, pred_v):
    if real_l is None or real_v is None or pred_l is None or pred_v is None:
        return 0, "#64748b", "⚪ Sin Jugar"
    if real_l == pred_l and real_v == pred_v:
        return 3, "#22c55e", "🟢 ¡Marcador Exacto! (+3 Pts)"
    signo_real = (real_l > real_v) - (real_l < real_v)
    signo_pred = (pred_l > pred_v) - (pred_l < pred_v)
    if signo_real == signo_pred:
        return 1, "#eab308", "🟡 Tendencia Acertada (+1 Pt)"
    return 0, "#ef4444", "🔴 Fallado (0 Pts)"

# --- BANNER DE BIENVENIDA VISTOSO ---
st.markdown("""
    <div class="hero-banner">
        <h1 style="color: #ffffff; font-size: 3rem; margin-bottom: 0px; text-shadow: 2px 2px 8px #000;">
            🏆 POLLA MUNDIALISTA 2026 ⚽
        </h1>
        <p style="color: #cbd5e1; font-size: 1.2rem; font-style: italic;">
            La batalla definitiva por el trono del fútbol entre amigos
        </p>
    </div>
""", unsafe_allow_html=True)

col_cr7, col_logo, col_messi = st.columns([2, 2, 2])
with col_cr7: st.image("https://images.unsplash.com/photo-1518063319789-7217e6706b04?auto=format&fit=crop&w=300&q=80", caption="¡Apunta a la gloria!")
with col_logo: st.image("https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=300&q=80", caption="FIFA World Cup 2026")
with col_messi: st.image("https://images.unsplash.com/photo-1544698310-74ea9d1c8258?auto=format&fit=crop&w=300&q=80", caption="¡El arte de predecir!")

st.write("---")

tab1, tab2, tab3 = st.tabs(["📊 CLASIFICACIÓN EN VIVO", "✍️ REGISTRAR PRONÓSTICOS", "⚙️ PANEL CONTROL"])

# --- TABLA DE POSICIONES ---
with tab1:
    st.markdown("## 🏆 ESTADO DEL POZO Y POSICIONES")
    tabla_posiciones = []
    num_jugadores = len(PARTICIPANTES)
    fondo_total = num_jugadores * CUOTA_INSCRIPCION
    
    for p in PARTICIPANTES:
        pts_totales = 0
        exactos = 0
        tendencias = 0
        for part in FIXTURE:
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
    
    if num_jugadores >= 6:
        premios = [fondo_total * 0.50, fondo_total * 0.3333, fondo_total * 0.1666]
        tags = ["🥇 1er Lugar (50%)", "🥈 2do Lugar (33.3%)", "🥉 3er Lugar (16.6%)"]
    else:
        premios = [fondo_total * 0.70, fondo_total * 0.30, 0]
        tags = ["🥇 1er Lugar (70%)", "🥈 2do Lugar (30%)", "🥉 Sin premio"]

    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        if len(df_tabla) >= 1:
            st.markdown(f"<div class='podio-box'><h3>{tags[0]}</h3><h2 style='color: #eab308;'>{df_tabla.iloc[0]['Participante']}</h2><p style='font-size: 1.5rem;'>${premios[0]:,.0f}</p></div>", unsafe_allow_html=True)
    with c_p2:
        if len(df_tabla) >= 2:
            st.markdown(f"<div class='podio-box'><h3>{tags[1]}</h3><h2 style='color: #cbd5e1;'>{df_tabla.iloc[1]['Participante']}</h2><p style='font-size: 1.5rem;'>${premios[1]:,.0f}</p></div>", unsafe_allow_html=True)
    with c_p3:
        if len(df_tabla) >= 3 and premios[2] > 0:
            st.markdown(f"<div class='podio-box'><h3>{tags[2]}</h3><h2 style='color: #b45309;'>{df_tabla.iloc[2]['Participante']}</h2><p style='font-size: 1.5rem;'>${premios[2]:,.0f}</p></div>", unsafe_allow_html=True)

    st.write("### 📈 CLASIFICACIÓN GENERAL COMPLETA")
    st.dataframe(df_tabla, use_container_width=True)

# --- REGISTRAR PRONÓSTICOS ---
with tab2:
    st.markdown("## ✍️ ARMA TU JUGADA")
    usuario = st.selectbox("Selecciona tu perfil de jugador:", PARTICIPANTES)
    
    for part in FIXTURE:
        pid = str(part["id"])
        pred_actual = datos["pronosticos"].get(usuario, {}).get(pid, {"l": 0, "v": 0})
        real_actual = datos["resultados_reales"].get(pid)
        
        _, color_hex, texto_status = calcular_puntos(
            real_actual["l"] if real_actual else None,
            real_actual["v"] if real_actual else None,
            pred_actual["l"], pred_actual["v"]
        )
        
        st.markdown(f"""
        <div style="background: rgba(30,41,59,0.5); padding: 10px; border-radius: 8px; border-left: 5px solid {color_hex}; margin-top: 10px;">
            <b>Partido #{pid} - Grupo {part['grupo']} ({part['fecha']})</b> | <span style="color: {color_hex};">{texto_status}</span>
        </div>
        """, unsafe_allow_html=True)
        
        col_inputs = st.columns([3, 2, 2, 3])
        with col_inputs[0]: 
            st.write(f"{part['local']} {part['flag_l']}")
        with col_inputs[1]: 
            g_l = st.number_input(f"Goles {part['local']}", min_value=0, max_value=15, value=int(pred_actual["l"]), key=f"l_{usuario}_{pid}")
        with col_inputs[2]: 
            g_v = st.number_input(f"Goles {part['visita']}", min_value=0, max_value=15, value=int(pred_actual["v"]), key=f"v_{usuario}_{pid}")
        with col_inputs[3]: 
            st.write(f"{part['flag_v']} {part['visita']}")
            
        datos["pronosticos"][usuario][pid] = {"l": g_l, "v": g_v}
        
    if st.button("💾 GUARDAR MIS PRONÓSTICOS"):
        guardar_datos(datos)
        st.balloons()
        st.success("¡Tus predicciones fueron guardadas de manera segura!")

# --- PANEL ADMINISTRADOR ---
with tab3:
    st.markdown("## ⚙️ ADMINISTRACIÓN (RESTRINGIDO)")
    password = st.text_input("Ingresa token de seguridad:", type="password")
    
    if password == PASSWORD_ADMIN:
        st.success("Acceso Concedido")
        for part in FIXTURE:
            pid = str(part["id"])
            real_actual = datos["resultados_reales"].get(pid, {"l": 0, "v": 0})
            
            st.write(f"**Partido #{pid}: {part['local']} vs {part['visita']}**")
            col_admin = st.columns(2)
            with col_admin[0]: g_r_l = st.number_input(f"Oficial {part['local']}", min_value=0, value=int(real_actual["l"]), key=f"rl_{pid}")
            with col_admin[1]: g_r_v = st.number_input(f"Oficial {part['visita']}", min_value=0, value=int(real_actual["v"]), key=f"rv_{pid}")
            
            partido_jugado = st.checkbox("¿Finalizado?", key=f"play_{pid}", value=(pid in datos["resultados_reales"]))
            if partido_jugado:
                datos["resultados_reales"][pid] = {"l": g_r_l, "v": g_r_v}
            else:
                datos["resultados_reales"].pop(pid, None)
                
        if st.button("🔄 SUBIR MARCADORES Y RECALCULAR TODO"):
            guardar_datos(datos)
            st.snow()
            st.success("¡Puntajes actualizados!")
