import streamlit as st
import pandas as pd
import json
import os
import random
import base64
from datetime import datetime
import pytz

# CONFIGURACIÓN DE LA PÁGINA (Diseño Responsive)
st.set_page_config(page_title="Polla Mundial 2026", page_icon="⚽", layout="wide")

# CONSOLIDADO OFICIAL DE LOS 104 PARTIDOS CON LLAVES ELIMINATORIAS SEGÚN FORMATO FIFA
@st.cache_data
def obtener_fixture_completo():
    return [
        # --- FECHA 1 (Partidos 1 al 24) — ORDENADO CRONOLÓGICAMENTE POR HORARIO CHILE ---
        {"id": 1, "fase_bloque": "Fecha 1", "grupo": "Grupo A", "fecha_ref": "2026-06-11 15:00", "fecha": "11 de Junio", "hora": "15:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Ciudad de México"},
        {"id": 2, "fase_bloque": "Fecha 1", "grupo": "Grupo A", "fecha_ref": "2026-06-11 22:00", "fecha": "11 de Junio", "hora": "22:00", "local": "COREA DEL SUR", "flag_l": "🇰🇷", "visita": "REP. CHECA", "flag_v": "🇨🇿", "estadio": "Guadalajara"},
        {"id": 3, "fase_bloque": "Fecha 1", "grupo": "Grupo B", "fecha_ref": "2026-06-12 15:00", "fecha": "12 de Junio", "hora": "15:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Toronto"},
        {"id": 4, "fase_bloque": "Fecha 1", "grupo": "Grupo D", "fecha_ref": "2026-06-12 21:00", "fecha": "12 de Junio", "hora": "21:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "Los Angeles"},
        {"id": 5, "fase_bloque": "Fecha 1", "grupo": "Grupo B", "fecha_ref": "2026-06-13 15:00", "fecha": "13 de Junio", "hora": "15:00", "local": "CATAR", "flag_l": "🇶🇦", "visita": "SUIZA", "flag_v": "🇨🇭", "estadio": "San Francisco"},
        {"id": 6, "fase_bloque": "Fecha 1", "grupo": "Grupo C", "fecha_ref": "2026-06-13 18:00", "fecha": "13 de Junio", "hora": "18:00", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "N. York/N. Jersey"},
        {"id": 7, "fase_bloque": "Fecha 1", "grupo": "Grupo C", "fecha_ref": "2026-06-13 21:00", "fecha": "13 de Junio", "hora": "21:00", "local": "HAITÍ", "flag_l": "🇭🇹", "visita": "ESCOCIA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "estadio": "Boston"},
        {"id": 8, "fase_bloque": "Fecha 1", "grupo": "Grupo D", "fecha_ref": "2026-06-14 00:00", "fecha": "14 de Junio", "hora": "00:00", "local": "AUSTRALIA", "flag_l": "🇦🇺", "visita": "TURQUÍA", "flag_v": "🇹🇷", "estadio": "Vancouver"},
        {"id": 9, "fase_bloque": "Fecha 1", "grupo": "Grupo E", "fecha_ref": "2026-06-14 13:00", "fecha": "14 de Junio", "hora": "13:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Houston"},
        {"id": 10, "fase_bloque": "Fecha 1", "grupo": "Grupo F", "fecha_ref": "2026-06-14 16:00", "fecha": "14 de Junio", "hora": "16:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Dallas"},
        {"id": 11, "fase_bloque": "Fecha 1", "grupo": "Grupo E", "fecha_ref": "2026-06-14 19:00", "fecha": "14 de Junio", "hora": "19:00", "local": "COSTA DE MARFIL", "flag_l": "🇨🇮", "visita": "ECUADOR", "flag_v": "🇪🇨", "estadio": "Filadelfia"},
        {"id": 12, "fase_bloque": "Fecha 1", "grupo": "Grupo F", "fecha_ref": "2026-06-14 22:00", "fecha": "14 de Junio", "hora": "22:00", "local": "SUECIA", "flag_l": "🇸🇪", "visita": "TÚNEZ", "flag_v": "🇹🇳", "estadio": "Monterrey"},
        {"id": 13, "fase_bloque": "Fecha 1", "grupo": "Grupo H", "fecha_ref": "2026-06-15 12:00", "fecha": "15 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Atlanta"},
        {"id": 14, "fase_bloque": "Fecha 1", "grupo": "Grupo G", "fecha_ref": "2026-06-15 15:00", "fecha": "15 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Seattle"},
        {"id": 15, "fase_bloque": "Fecha 1", "grupo": "Grupo H", "fecha_ref": "2026-06-15 18:00", "fecha": "15 de Junio", "hora": "18:00", "local": "ARABIA SAUDITA", "flag_l": "🇸🇦", "visita": "URUGUAY", "flag_v": "🇺🇾", "estadio": "Miami"},
        {"id": 16, "fase_bloque": "Fecha 1", "grupo": "Grupo G", "fecha_ref": "2026-06-15 21:00", "fecha": "15 de Junio", "hora": "21:00", "local": "IRÁN", "flag_l": "🇮🇷", "visita": "NUEVA ZELANDA", "flag_v": "🇳🇿", "estadio": "Los Angeles"},
        {"id": 17, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha_ref": "2026-06-16 15:00", "fecha": "16 de Junio", "hora": "15:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 18, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha_ref": "2026-06-17 16:00", "fecha": "17 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Dallas"},
        {"id": 19, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha_ref": "2026-06-16 18:00", "fecha": "16 de Junio", "hora": "18:00", "local": "IRAK", "flag_l": "🇮🇶", "visita": "NORUEGA", "flag_v": "🇳🇴", "estadio": "Boston"},
        {"id": 20, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha_ref": "2026-06-16 21:00", "fecha": "16 de Junio", "hora": "21:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "Kansas City"},
        {"id": 21, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha_ref": "2026-06-17 00:00", "fecha": "17 de Junio", "hora": "00:00", "local": "AUSTRIA", "flag_l": "🇦🇹", "visita": "JORDANIA", "flag_v": "🇯🇴", "estadio": "San Francisco"},
        {"id": 22, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha_ref": "2026-06-17 13:00", "fecha": "17 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "REP. DEL CONGO", "flag_v": "🇨🇬", "estadio": "Houston"},
        {"id": 23, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha_ref": "2026-06-17 19:00", "fecha": "17 de Junio", "hora": "19:00", "local": "GHANA", "flag_l": "🇬🇭", "visita": "PANAMÁ", "flag_v": "🇵🇦", "estadio": "Toronto"},
        {"id": 24, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha_ref": "2026-06-17 22:00", "fecha": "17 de Junio", "hora": "22:00", "local": "UZBEKISTÁN", "flag_l": "🇺🇿", "visita": "COLOMBIA", "flag_v": "🇨🇴", "estadio": "Ciudad de México"},

        # --- FECHA 2 (Partidos 25 al 48) ---
        {"id": 25, "fase_bloque": "Fecha 2", "grupo": "Grupo A", "fecha_ref": "2026-06-18 12:00", "fecha": "18 de Junio", "hora": "12:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Atlanta"},
        {"id": 26, "fase_bloque": "Fecha 2", "grupo": "Grupo B", "fecha_ref": "2026-06-18 15:00", "fecha": "18 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Los Angeles"},
        {"id": 27, "fase_bloque": "Fecha 2", "grupo": "Grupo B", "fecha_ref": "2026-06-18 18:00", "fecha": "18 de Junio", "hora": "18:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Vancouver"},
        {"id": 28, "fase_bloque": "Fecha 2", "grupo": "Grupo A", "fecha_ref": "2026-06-18 21:00", "fecha": "18 de Junio", "hora": "21:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Guadalajara"},
        {"id": 29, "fase_bloque": "Fecha 2", "grupo": "Grupo D", "fecha_ref": "2026-06-19 15:00", "fecha": "19 de Junio", "hora": "15:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "Seattle"},
        {"id": 30, "fase_bloque": "Fecha 2", "grupo": "Grupo C", "fecha_ref": "2026-06-19 18:00", "fecha": "19 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "Boston"},
        {"id": 31, "fase_bloque": "Fecha 2", "grupo": "Grupo C", "fecha_ref": "2026-06-19 20:30", "fecha": "19 de Junio", "hora": "20:30", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Filadelfia"},
        {"id": 32, "fase_bloque": "Fecha 2", "grupo": "Grupo D", "fecha_ref": "2026-06-19 23:00", "fecha": "19 de Junio", "hora": "23:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "San Francisco"},
        {"id": 33, "fase_bloque": "Fecha 2", "grupo": "Grupo F", "fecha_ref": "2026-06-20 13:00", "fecha": "20 de Junio", "hora": "13:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Houston"},
        {"id": 34, "fase_bloque": "Fecha 2", "grupo": "Grupo E", "fecha_ref": "2026-06-20 16:00", "fecha": "20 de Junio", "hora": "16:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Toronto"},
        {"id": 35, "fase_bloque": "Fecha 2", "grupo": "Grupo E", "fecha_ref": "2026-06-20 20:00", "fecha": "20 de Junio", "hora": "20:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Kansas City"},
        {"id": 36, "fase_bloque": "Fecha 2", "grupo": "Grupo F", "fecha_ref": "2026-06-21 00:00", "fecha": "21 de Junio", "hora": "00:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Monterrey"},
        {"id": 37, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha_ref": "2026-06-21 12:00", "fecha": "21 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Atlanta"},
        {"id": 38, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha_ref": "2026-06-21 15:00", "fecha": "21 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Los Angeles"},
        {"id": 39, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha_ref": "2026-06-21 18:00", "fecha": "21 de Junio", "hora": "18:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Miami"},
        {"id": 40, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha_ref": "2026-06-21 21:00", "fecha": "21 de Junio", "hora": "21:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Vancouver"},
        {"id": 41, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha_ref": "2026-06-23 13:00", "fecha": "23 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Houston"},
        {"id": 42, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha_ref": "2026-06-22 13:00", "fecha": "22 de Junio", "hora": "13:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Dallas"},
        {"id": 43, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha_ref": "2026-06-23 16:00", "fecha": "23 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Boston"},
        {"id": 44, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha_ref": "2026-06-22 17:00", "fecha": "22 de Junio", "hora": "17:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Filadelfia"},
        {"id": 45, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha_ref": "2026-06-23 19:00", "fecha": "23 de Junio", "hora": "19:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Toronto"},
        {"id": 46, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha_ref": "2026-06-22 20:00", "fecha": "22 de Junio", "hora": "20:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 47, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha_ref": "2026-06-23 22:00", "fecha": "23 de Junio", "hora": "22:00", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "REP. DEL CONGO", "flag_v": "🇨🇬", "estadio": "Guadalajara"},
        {"id": 48, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha_ref": "2026-06-22 23:00", "fecha": "22 de Junio", "hora": "23:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "San Francisco"},

        # --- FECHA 3 (Partidos 49 al 72) ---
        {"id": 49, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha_ref": "2026-06-24 15:00", "fecha": "24 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "CANADÁ", "flag_v": "🇨🇦", "estadio": "Vancouver"},
        {"id": 50, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha_ref": "2026-06-24 15:00", "fecha": "24 de Junio", "hora": "15:00", "local": "BOSNIA Y HERZEG.", "flag_l": "🇧🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Seattle"},
        {"id": 51, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha_ref": "2026-06-24 18:00", "fecha": "24 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "BRASIL", "flag_v": "🇧🇷", "estadio": "Miami"},
        {"id": 52, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha_ref": "2026-06-24 18:00", "fecha": "24 de Junio", "hora": "18:00", "local": "MARRUECOS", "flag_l": "🇲🇦", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Atlanta"},
        {"id": 53, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha_ref": "2026-06-24 21:00", "fecha": "24 de Junio", "hora": "21:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "MÉXICO", "flag_v": "🇲🇽", "estadio": "Ciudad de México"},
        {"id": 54, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha_ref": "2026-06-24 21:00", "fecha": "24 de Junio", "hora": "21:00", "local": "SUDÁFRICA", "flag_l": "🇿🇦", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Monterrey"},
        {"id": 55, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha_ref": "2026-06-26 15:00", "fecha": "26 de Junio", "hora": "15:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "FRANCIA", "flag_v": "🇫🇷", "estadio": "Boston"},
        {"id": 56, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha_ref": "2026-06-26 15:00", "fecha": "26 de Junio", "hora": "15:00", "local": "SENEGAL", "flag_l": "🇸🇳", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Toronto"},
        {"id": 57, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha_ref": "2026-06-25 16:00", "fecha": "25 de Junio", "hora": "16:00", "local": "CURAZAO", "flag_l": "🇨🇼", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Filadelfia"},
        {"id": 58, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha_ref": "2026-06-25 16:00", "fecha": "25 de Junio", "hora": "16:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "ALEMANIA", "flag_v": "🇩🇪", "estadio": "N. York/N. Jersey"},
        {"id": 59, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha_ref": "2026-06-27 17:00", "fecha": "27 de Junio", "hora": "17:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "INGLATERRA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "estadio": "N. York/N. Jersey"},
        {"id": 60, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha_ref": "2026-06-27 17:00", "fecha": "27 de Junio", "hora": "17:00", "local": "CROACIA", "flag_l": "🇭🇷", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Filadelfia"},
        {"id": 61, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha_ref": "2026-06-25 19:00", "fecha": "25 de Junio", "hora": "19:00", "local": "JAPÓN", "flag_l": "🇯🇵", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Dallas"},
        {"id": 62, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha_ref": "2026-06-25 19:00", "fecha": "25 de Junio", "hora": "19:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "PAÍSES BAJOS", "flag_v": "🇳🇱", "estadio": "Kansas City"},
        {"id": 63, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha_ref": "2026-06-27 19:30", "fecha": "27 de Junio", "hora": "19:30", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "PORTUGAL", "flag_v": "🇵🇹", "estadio": "Miami"},
        {"id": 64, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha_ref": "2026-06-27 19:30", "fecha": "27 de Junio", "hora": "19:30", "local": "REP. DEL CONGO", "flag_l": "🇨🇬", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Atlanta"},
        {"id": 65, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha_ref": "2026-06-26 20:00", "fecha": "26 de Junio", "hora": "20:00", "local": "CABO VERDE", "flag_l": "🇨🇻", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Houston"},
        {"id": 66, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha_ref": "2026-06-26 20:00", "fecha": "26 de Junio", "hora": "20:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "ESPAÑA", "flag_v": "🇪🇸", "estadio": "Guadalajara"},
        {"id": 67, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha_ref": "2026-06-25 22:00", "fecha": "25 de Junio", "hora": "22:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "ESTADOS UNIDOS", "flag_v": "🇺🇸", "estadio": "Los Angeles"},
        {"id": 68, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha_ref": "2026-06-25 22:00", "fecha": "25 de Junio", "hora": "22:00", "local": "PARAGUAY", "flag_l": "🇵🇾", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "San Francisco"},
        {"id": 69, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha_ref": "2026-06-27 22:00", "fecha": "27 de Junio", "hora": "22:00", "local": "ARGELIA", "flag_l": "🇩🇿", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Kansas City"},
        {"id": 70, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha_ref": "2026-06-27 22:00", "fecha": "27 de Junio", "hora": "22:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGENTINA", "flag_v": "🇦🇷", "estadio": "Dallas"},
        {"id": 71, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha_ref": "2026-06-26 23:00", "fecha": "26 de Junio", "hora": "23:00", "local": "EGIPTO", "flag_l": "🇪🇬", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Seattle"},
        {"id": 72, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha_ref": "2026-06-26 23:00", "fecha": "26 de Junio", "hora": "23:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "BÉLGICA", "flag_v": "🇧🇪", "estadio": "Vancouver"},

        # --- FASES FINALES ---
        {"id": 73, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-28 16:00", "fecha": "28 de Junio", "hora": "16:00", "local": "2A", "flag_l": "⚽", "visita": "2B", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 74, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 15:00", "fecha": "29 de Junio", "hora": "15:00", "local": "1A", "flag_l": "⚽", "visita": "3C/E/F/I", "flag_v": "⚽", "estadio": "Boston"},
        {"id": 75, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 18:00", "fecha": "29 de Junio", "hora": "18:00", "local": "1B", "flag_l": "⚽", "visita": "3A/C/F/H", "flag_v": "⚽", "estadio": "Atlanta"},
        {"id": 76, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 21:00", "fecha": "29 de Junio", "hora": "21:00", "local": "2C", "flag_l": "⚽", "visita": "2D", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 89, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-04 15:00", "fecha": "04 de Julio", "hora": "15:00", "local": "GANADOR P74", "flag_l": "🥇", "visita": "GANADOR P73", "flag_v": "🥇", "estadio": "Philadelphia"},
        {"id": 97, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-09 16:00", "fecha": "09 de Julio", "hora": "16:00", "local": "GANADOR P89", "flag_l": "🥇", "visita": "GANADOR P90", "flag_v": "🥇", "estadio": "Boston"},
        {"id": 101, "fase_bloque": "Fases Finales", "grupo": "Semifinales", "fecha_ref": "2026-07-14 15:00", "fecha": "14 de Julio", "hora": "15:00", "local": "GANADOR P97", "flag_l": "🥇", "visita": "GANADOR P98", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 104, "fase_bloque": "Fases Finales", "grupo": "Gran Final", "fecha_ref": "2026-07-19 15:00", "fecha": "19 de Julio", "hora": "15:00", "local": "GANADOR P101", "flag_l": "🥇", "visita": "GANADOR P102", "flag_v": "🥇", "estadio": "N. York/N. Jersey"}
    ]

FIXTURE = sorted(obtener_fixture_completo(), key=lambda x: x['id'])

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

# CONFIGURACIÓN GENERAL DE USUARIOS
PARTICIPANTES = ["Constanza", "José Alonso", "José Mario", "Leonardo", "Mario", "Néstor", "Renato", "Sergio"]
CUOTA_INSCRIPCION = 5000
PASSWORD_ADMIN = "admin123"

# FUNCIÓN TÉCNICA PARA PASAR IMÁGENES LOCALES A ENLACES COMPATIBLES
def codificar_imagen_local(ruta_archivo):
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return ""

img_fondo = codificar_imagen_local("fondo.png")
img_portada = codificar_imagen_local("portada.png")
img_balon = codificar_imagen_local("balon.png")

# ESTILOS ADAPTADOS
st.markdown(f"""
    <style>
    .main {{ 
        background: linear-gradient(rgba(15, 23, 42, 0.88), rgba(30, 41, 59, 0.88)){" , url('" + img_fondo + "')" if img_fondo else ""};
        background-size: cover; background-attachment: fixed; color: #ffffff; 
    }}
    .hero-banner {{
        background: linear-gradient(rgba(15, 23, 42, 0.2), rgba(30, 41, 59, 0.2)){" , url('" + img_portada + "')" if img_portada else ""};
        background-size: cover; background-position: center; padding: 90px 35px; border-radius: 15px; border: 3px solid #be123c;
    }}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE PERSISTENCIA DE DATOS EN VIVO ---
def inicializar_base_de_datos():
    base_inicial = {
        "resultados_reales": {},
        "pronosticos": {p: {} for p in PARTICIPANTES}
    }
    
    if os.path.exists("datos_polla.json"):
        with open("datos_polla.json", "r") as f:
            try:
                content = json.load(f)
                if isinstance(content, dict):
                    if "resultados_reales" in content:
                        base_inicial["resultados_reales"] = content["resultados_reales"]
                    if "pronosticos" in content:
                        for p in PARTICIPANTES:
                            base_inicial["pronosticos"][p] = content["pronosticos"].get(p, {})
                    return base_inicial
            except:
                pass
    return base_inicial

if "datos_globales" not in st.session_state:
    st.session_state["datos_globales"] = inicializar_base_de_datos()

datos = st.session_state["datos_globales"]

def guardar_datos(datos_completos):
    st.session_state["datos_globales"] = datos_completos
    try:
        with open("datos_polla.json", "w") as f:
            json.dump(datos_completos, f, indent=4)
    except:
        pass

def resolver_fixture_dinamico(fixture_base, resultados_reales):
    fixture_copia = [dict(m) for m in fixture_base]
    for m in fixture_copia:
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
    return fixture_copia

FIXTURE_DINAMICO = resolver_fixture_dinamico(FIXTURE, datos["resultados_reales"])

def calcular_puntos(real_l, real_v, pred_l, pred_v):
    if real_l is None or real_v is None or pred_l is None or pred_v is None:
        return 0, "#64748b", "⚪ Sin Jugar"
    try:
        rl, rv = int(real_l), int(real_v)
        pl, pv = int(pred_l), int(pred_v)
    except (ValueError, TypeError):
        return 0, "#64748b", "⚪ Sin Jugar"
        
    if rl == pl and rv == pv:
        return 3, "#22c55e", "🟢 Marcador Exacto (+3 Pts)"
    signo_real = (rl > rv) - (rl < rv)
    signo_pred = (pl > pv) - (pl < pv)
    if signo_real == signo_pred:
        return 1, "#eab308", "🟡 Tendencia Acertada (+1 Pt)"
    return 0, "#ef4444", "🔴 Fallado (0 Pts)"

def verificar_partido_empezado(fecha_ref_str):
    tz_chile = pytz.timezone('America/Santiago')
    ahora_chile = datetime.now(tz_chile)
    try:
        hora_partido = datetime.strptime(fecha_ref_str, "%Y-%m-%d %H:%M")
        hora_partido_tz = tz_chile.localize(hora_partido)
        return ahora_chile >= hora_partido_tz
    except:
        return False

# ANIMACIÓN DEL BALÓN
def animar_balon_oficial():
    src_balon = img_balon if img_balon else "⚽"
    if img_balon:
        balon_html = f"""
        <div id="ball-box" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:99999;display:flex;justify-content:center;align-items:center;">
            <img src="{src_balon}" id="spinning-ball" style="width:160px;height:160px;animation: spin 1.5s ease-out forwards;">
        </div>
        <style>
        @keyframes spin {{
            0% {{ transform: scale(0) rotate(0deg); opacity: 0; }}
            40% {{ transform: scale(1.3) rotate(360deg); opacity: 1; }}
            100% {{ transform: scale(0) rotate(720deg); opacity: 0; }}
        }}
        </style>
        <script>setTimeout(() => {{ document.getElementById('ball-box').remove(); }}, 1500);</script>
        """
    else:
        balon_html = """
        <div id="ball-box" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:99999;display:flex;justify-content:center;align-items:center;">
            <div style="font-size:120px; animation: spin 1.4s ease-out forwards;">⚽</div>
        </div>
        <style>
        @keyframes spin { 0% { transform: scale(0) rotate(0deg); } 50% { transform: scale(1.5) rotate(360deg); } 100% { transform: scale(0); } }
        </style>
        <script>setTimeout(() => { document.getElementById('ball-box').remove(); }, 1400);</script>
        """
    st.components.v1.html(balon_html, height=0, width=0)

# --- PORTADA DE LA WEB ---
st.markdown('<div class="hero-banner"></div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-style:italic; color:#f1f5f9; font-size:1.05rem; padding:0 20px;'>{obtener_frase_futbolera()}</p>", unsafe_allow_html=True)
st.write("---")

tabs = st.tabs(["📜 BASES DEL JUEGO", "📊 CLASIFICACIÓN EN VIVO", "✍️ REGISTRAR PRONÓSTICOS", "📅 CRONOGRAMA", "⚙️ PANEL CONTROL"])

# --- TAB 1: BASES OFICIALES ---
with tabs[0]:
    st.markdown("""
    ## 🏆 BASES POLLA MUNDIALERA 🏆
    ...
    """)

# --- TAB 2: CLASIFICACIÓN EN VIVO ---
with tabs[1]:
    st.markdown("## 📊 RENDIMIENTO DE LA FAMILIA")
    tabla_posiciones = []
    fondo_total = len(PARTICIPANTES) * CUOTA_INSCRIPCION
    
    for p in PARTICIPANTES:
        pts_totales = 0
        exactos = 0
        tendencias = 0
        for part in FIXTURE_DINAMICO:
            pid = str(part["id"])
            real = datos["resultados_reales"].get(pid)
            pred = datos["pronosticos"].get(p, {}).get(pid, {"l": 0, "v": 0})
            if real and pred and "l" in real and "v" in real:
                pts, _, _ = calcular_puntos(real["l"], real["v"], pred.get("l", 0), pred.get("v", 0))
                pts_totales += pts
                if pts == 3: exactos += 1
                elif pts == 1: tendencias += 1
        tabla_posiciones.append({"Participante": p, "Puntos Totales 🌟": pts_totales, "Marcadores Exactos (3pts) 🎯": exactos, "Aciertos Simples (1pt) 🏟️": tendencias})
    
    df_tabla = pd.DataFrame(tabla_posiciones).sort_values(by=["Puntos Totales 🌟", "Marcadores Exactos (3pts) 🎯"], ascending=False).reset_index(drop=True)
    df_tabla.index += 1
    
    puntero_1 = df_tabla.iloc[0]["Participante"].upper() if len(df_tabla) > 0 else "POR DEFINIR"
    puntero_2 = df_tabla.iloc[1]["Participante"].upper() if len(df_tabla) > 1 else "POR DEFINIR"
    puntero_3 = df_tabla.iloc[2]["Participante"].upper() if len(df_tabla) > 2 else "POR DEFINIR"
    
    st.markdown(f"### 💰 Pozo Acumulado del Grupo: **${fondo_total:,.0f} CLP**")
    ...
    st.dataframe(df_tabla, use_container_width=True)

# --- TAB 3: REGISTRAR PRONÓSTICOS (CORREGIDO CON FORMULARIO SEGURO) ---
with tabs[2]:
    st.markdown("## ✍️ ARMA TU JUGADA")
    usuario = st.selectbox("Selecciona tu nombre para apostar:", PARTICIPANTES)
    
    bloque_seleccionado = st.radio(
        "Selecciona la fecha que deseas pronosticar para reducir la lista:",
        ["Fecha 1 (Partidos 1-24)", "Fecha 2 (Partidos 25-48)", "Fecha 3 (Partidos 49-72)", "Fases Finales Eliminatorias"],
        horizontal=True
    )
    
    if "Fecha 1" in bloque_seleccionado: filtro_fia = "Fecha 1"
    elif "Fecha 2" in bloque_seleccionado: filtro_fia = "Fecha 2"
    elif "Fecha 3" in bloque_seleccionado: filtro_fia = "Fecha 3"
    else: filtro_fia = "Fases Finales"
    
    partidos_visibles = [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == filtro_fia]
    
    st.write(f"### 🏟️ Mostrando {len(partidos_visibles)} partidos de: **{bloque_seleccionado}**")
    st.write("---")
    
    # Creamos un contenedor de formulario único para procesar todo sin micro-recargas intermedias
    with st.form(key=f"formulario_apuestas_{usuario}_{filtro_fia}"):
        
        # Diccionario temporal interno para capturar los inputs del formulario de forma limpia
        respuestas_temporales = {}
        
        for part in partidos_visibles:
            pid = str(part["id"])
            pred_actual = datos["pronosticos"].get(usuario, {}).get(pid, {"l": 0, "v": 0})
            real_actual = datos["resultados_reales"].get(pid)
            
            ya_empezo = verificar_partido_empezado(part.get("fecha_ref", "2026-06-11 00:00"))
            congelado_por_admin = pid in datos["resultados_reales"]
            bloquear_casilla = ya_empezo or congelado_por_admin
            
            real_l = real_actual.get("l") if real_actual else None
            real_v = real_actual.get("v") if real_actual else None
            
            _, color_hex, texto_status = calcular_puntos(real_l, real_v, pred_actual.get("l", 0), pred_actual.get("v", 0))
            
            if congelado_por_admin:
                texto_status += " | 🔒 APUESTA CERRADA"
            elif ya_empezo:
                texto_status += " | 🔒 CANDADO: PARTIDO EN CURSO"
                color_hex = "#be123c"
            
            st.markdown(f"""
            <div style="background: rgba(30,41,59,0.7); padding: 6px 12px; border-radius: 8px 8px 0 0; border-left: 5px solid {color_hex}; font-size: 0.85rem; margin-top:12px; color:#cbd5e1;">
                <b>{part["grupo"].upper()} — PARTIDO #{pid}</b> ({part["fecha"]} - {part["hora"]} hrs) | {part["estadio"]} | <span style="color:{color_hex}; font-weight:bold;">{texto_status}</span>
            </div>
            """, unsafe_allow_html=True)
            
            col_l, col_inputs, col_v = st.columns([4, 3, 4])
            with col_l:
                st.markdown(f"<div style='text-align:right; font-weight:bold; font-size:1rem; padding-top:6px;'>{part['local']} {part['flag_l']}</div>", unsafe_allow_html=True)
            with col_inputs:
                c_in1, c_in2 = st.columns(2)
                with c_in1:
                    g_l = st.number_input("GL", min_value=0, max_value=15, value=int(pred_actual.get("l", 0)), key=f"l_{usuario}_{pid}", disabled=bloquear_casilla, label_visibility="collapsed")
                with c_in2:
                    g_v = st.number_input("GV", min_value=0, max_value=15, value=int(pred_actual.get("v", 0)), key=f"v_{usuario}_{pid}", disabled=bloquear_casilla, label_visibility="collapsed")
            with col_v:
                st.markdown(f"<div style='text-align:left; font-weight:bold; font-size:1rem; padding-top:6px;'>{part['flag_v']} {part['visita']}</div>", unsafe_allow_html=True)
            
            # Guardamos temporalmente el valor actual del input (esté bloqueado o no)
            respuestas_temporales[pid] = {"l": g_l, "v": g_v}
            
        st.write("---")
        # El botón de guardado ahora envía el bloque completo de golpe de forma segura
        enviar_formulario = st.form_submit_button(label="💾 GUARDAR APUESTAS DE ESTA FECHA EN BLOQUE", use_container_width=True)
        
        if enviar_formulario:
            # Transferimos los datos temporales limpios a nuestra base oficial
            for pid, scores in respuestas_temporales.items():
                # Doble validación por si el partido expiró en el último segundo antes de presionar enviar
                partido_info = next((m for m in partidos_visibles if str(m["id"]) == pid), None)
                if partido_info and not verificar_partido_empezado(partido_info.get("fecha_ref", "2026-06-11 00:00")) and pid not in datos["resultados_reales"]:
                    datos["pronosticos"][usuario][pid] = scores
            
            guardar_datos(datos)
            animar_balon_oficial()
            st.success(f"¡Excelente {usuario}, tus pronósticos activos de la {filtro_fia} fueron procesados y guardados de forma 100% segura!")
            st.rerun()

# --- TAB 4: CRONOGRAMA INTELIGENTE ---
with tabs[3]:
    st.markdown("## 📅 CRONOGRAMA OFICIAL Y MARCADORES EN VIVO")
    ...
