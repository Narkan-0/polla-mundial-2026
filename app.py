import streamlit as st
import pandas as pd
import json
import os
import random
import base64
import requests
from datetime import datetime
import pytz

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Polla Mundial 2026", page_icon="🏆", layout="wide")

# CONFIGURACIÓN GENERAL DE USUARIOS Y VARIABLES
PARTICIPANTES = ["Constanza", "David", "Franco", "José Alonso", "José Mario", "Leonardo", "Marlene", "Mario", "Néstor", "Renato", "Sergio"]
CUOTA_INSCRIPCION = 5000
PASSWORD_ADMIN = "admin123"
ARCHIVO_DATOS = "datos_polla.json"

# 🚨 CONFIGURACIÓN DE TU REPOSITORIO PARA EL AUTO-GUARDADO 🚨
REPO_GITHUB = "Narkan-0/polla-mundial-2026" 

# CONSOLIDADO OFICIAL DE LOS 104 PARTIDOS SEGÚN FORMATO FIFA (ORDEN CRONOLÓGICO ESTRICTO)
@st.cache_data
def obtener_fixture_completo():
    return [
        # --- FECHA 1 ---
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
        {"id": 18, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha_ref": "2026-06-16 18:00", "fecha": "16 de Junio", "hora": "18:00", "local": "IRAK", "flag_l": "🇮🇶", "visita": "NORUEGA", "flag_v": "🇳🇴", "estadio": "Boston"},
        {"id": 19, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha_ref": "2026-06-16 21:00", "fecha": "16 de Junio", "hora": "21:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "Kansas City"},
        {"id": 20, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha_ref": "2026-06-17 00:00", "fecha": "17 de Junio", "hora": "00:00", "local": "AUSTRIA", "flag_l": "🇦🇹", "visita": "JORDANIA", "flag_v": "🇯🇴", "estadio": "San Francisco"},
        {"id": 21, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha_ref": "2026-06-17 13:00", "fecha": "17 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "RD CONGO", "flag_v": "🇨🇩", "estadio": "Houston"},
        {"id": 22, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha_ref": "2026-06-17 16:00", "fecha": "17 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Dallas"},
        {"id": 23, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha_ref": "2026-06-17 19:00", "fecha": "17 de Junio", "hora": "19:00", "local": "GHANA", "flag_l": "🇬🇭", "visita": "PANAMÁ", "flag_v": "🇵🇦", "estadio": "Toronto"},
        {"id": 24, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha_ref": "2026-06-17 22:00", "fecha": "17 de Junio", "hora": "22:00", "local": "UZBEKISTÁN", "flag_l": "🇺🇿", "visita": "COLOMBIA", "flag_v": "🇨🇴", "estadio": "Ciudad de México"},

        # --- FECHA 2 ---
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
        {"id": 38, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha_ref": "2026-06-21 15:00", "fecha": "21 de Junio", "hora": "21:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Los Angeles"},
        {"id": 39, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha_ref": "2026-06-21 18:00", "fecha": "21 de Junio", "hora": "18:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Miami"},
        {"id": 40, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha_ref": "2026-06-21 21:00", "fecha": "21 de Junio", "hora": "21:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Vancouver"},
        {"id": 42, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha_ref": "2026-06-22 13:00", "fecha": "22 de Junio", "hora": "13:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Dallas"},
        {"id": 44, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha_ref": "2026-06-22 17:00", "fecha": "22 de Junio", "hora": "17:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Filadelfia"},
        {"id": 46, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha_ref": "2026-06-22 20:00", "fecha": "22 de Junio", "hora": "20:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 48, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha_ref": "2026-06-22 23:00", "fecha": "22 de Junio", "hora": "23:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "San Francisco"},
        {"id": 41, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha_ref": "2026-06-23 13:00", "fecha": "23 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Houston"},
        {"id": 43, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha_ref": "2026-06-23 16:00", "fecha": "23 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Boston"},
        {"id": 45, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha_ref": "2026-06-23 19:00", "fecha": "23 de Junio", "hora": "19:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Toronto"},
        {"id": 47, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha_ref": "2026-06-23 22:00", "fecha": "23 de Junio", "hora": "22:00", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "RD CONGO", "flag_v": "🇨🇩", "estadio": "Guadalajara"},

        # --- FECHA 3 ---
        {"id": 49, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha_ref": "2026-06-24 15:00", "fecha": "24 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "CANADÁ", "flag_v": "🇨🇦", "estadio": "Vancouver"},
        {"id": 50, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha_ref": "2026-06-24 15:00", "fecha": "24 de Junio", "hora": "15:00", "local": "BOSNIA Y HERZEG.", "flag_l": "🇧🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Seattle"},
        {"id": 51, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha_ref": "2026-06-24 18:00", "fecha": "24 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "BRASIL", "flag_v": "🇧🇷", "estadio": "Miami"},
        {"id": 52, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha_ref": "2026-06-24 18:00", "fecha": "24 de Junio", "hora": "18:00", "local": "MARRUECOS", "flag_l": "🇲🇦", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Atlanta"},
        {"id": 53, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha_ref": "2026-06-24 21:00", "fecha": "24 de Junio", "hora": "21:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "MÉXICO", "flag_v": "🇲🇽", "estadio": "Ciudad de México"},
        {"id": 54, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha_ref": "2026-06-24 21:00", "fecha": "24 de Junio", "hora": "21:00", "local": "SUDÁFRICA", "flag_l": "🇿🇦", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Monterrey"},
        {"id": 57, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha_ref": "2026-06-25 16:00", "fecha": "25 de Junio", "hora": "16:00", "local": "CURAZAO", "flag_l": "🇨🇼", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Filadelfia"},
        {"id": 58, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha_ref": "2026-06-25 16:00", "fecha": "25 de Junio", "hora": "16:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "ALEMANIA", "flag_v": "🇩🇪", "estadio": "N. York/N. Jersey"},
        {"id": 61, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha_ref": "2026-06-25 19:00", "fecha": "25 de Junio", "hora": "19:00", "local": "JAPÓN", "flag_l": "🇯🇵", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Dallas"},
        {"id": 62, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha_ref": "2026-06-25 19:00", "fecha": "25 de Junio", "hora": "19:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "PAÍSES BAJOS", "flag_v": "🇳🇱", "estadio": "Kansas City"},
        {"id": 67, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha_ref": "2026-06-25 22:00", "fecha": "25 de Junio", "hora": "22:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "ESTADOS UNIDOS", "flag_v": "🇺🇸", "estadio": "Los Angeles"},
        {"id": 68, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha_ref": "2026-06-25 22:00", "fecha": "25 de Junio", "hora": "22:00", "local": "PARAGUAY", "flag_l": "🇵🇾", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "San Francisco"},
        {"id": 55, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha_ref": "2026-06-26 15:00", "fecha": "26 de Junio", "hora": "15:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "FRANCIA", "flag_v": "🇫🇷", "estadio": "Boston"},
        {"id": 56, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha_ref": "2026-06-26 15:00", "fecha": "26 de Junio", "hora": "15:00", "local": "SENEGAL", "flag_l": "🇸🇳", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Toronto"},
        {"id": 65, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha_ref": "2026-06-26 20:00", "fecha": "26 de Junio", "hora": "20:00", "local": "CABO VERDE", "flag_l": "🇨🇻", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Houston"},
        {"id": 66, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha_ref": "2026-06-26 20:00", "fecha": "26 de Junio", "hora": "20:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "ESPAÑA", "flag_v": "🇪🇸", "estadio": "Guadalajara"},
        {"id": 71, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha_ref": "2026-06-26 23:00", "fecha": "26 de Junio", "hora": "23:00", "local": "EGIPTO", "flag_l": "🇪🇬", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Seattle"},
        {"id": 72, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha_ref": "2026-06-26 23:00", "fecha": "26 de Junio", "hora": "23:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "BÉLGICA", "flag_v": "🇧🇪", "estadio": "Vancouver"},
        {"id": 59, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha_ref": "2026-06-27 17:00", "fecha": "27 de Junio", "hora": "17:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "INGLATERRA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "estadio": "N. York/N. Jersey"},
        {"id": 60, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha_ref": "2026-06-27 17:00", "fecha": "27 de Junio", "hora": "17:00", "local": "CROACIA", "flag_l": "🇭🇷", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Filadelfia"},
        {"id": 63, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha_ref": "2026-06-27 19:30", "fecha": "27 de Junio", "hora": "19:30", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "PORTUGAL", "flag_v": "🇵🇹", "estadio": "Miami"},
        {"id": 64, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha_ref": "2026-06-27 19:30", "fecha": "27 de Junio", "hora": "19:30", "local": "RD CONGO", "flag_l": "🇨🇩", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Atlanta"},
        {"id": 69, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha_ref": "2026-06-27 22:00", "fecha": "27 de Junio", "hora": "22:00", "local": "ARGELIA", "flag_l": "🇩🇿", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Kansas City"},
        {"id": 70, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha_ref": "2026-06-27 22:00", "fecha": "27 de Junio", "hora": "22:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGENTINA", "flag_v": "🇦🇷", "estadio": "Dallas"},

        # --- DIEZISEISAVOS DE FINAL ---
        {"id": 73, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-28 16:00", "fecha": "28 de Junio", "hora": "16:00", "local": "2A", "flag_l": "⚽", "visita": "2B", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 74, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 15:00", "fecha": "29 de Junio", "hora": "15:00", "local": "1A", "flag_l": "⚽", "visita": "3C/E/F/I", "flag_v": "⚽", "estadio": "Boston"},
        {"id": 75, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 18:00", "fecha": "29 de Junio", "hora": "18:00", "local": "1B", "flag_l": "⚽", "visita": "3A/C/F/H", "flag_v": "⚽", "estadio": "Atlanta"},
        {"id": 76, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 21:00", "fecha": "29 de Junio", "hora": "21:00", "local": "2C", "flag_l": "⚽", "visita": "2D", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 77, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-30 14:00", "fecha": "30 de Junio", "hora": "14:00", "local": "1F", "flag_l": "⚽", "visita": "2E", "flag_v": "⚽", "estadio": "Dallas"},
        {"id": 78, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-30 17:00", "fecha": "30 de Junio", "hora": "17:00", "local": "1E", "flag_l": "⚽", "visita": "3A/B/C/D", "flag_v": "⚽", "estadio": "Seattle"},
        {"id": 79, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-30 20:00", "fecha": "30 de Junio", "hora": "20:00", "local": "1D", "flag_l": "⚽", "visita": "3F/G/H/I", "flag_v": "⚽", "estadio": "San Francisco"},
        {"id": 80, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-01 13:00", "fecha": "01 de Julio", "hora": "13:00", "local": "1C", "flag_l": "⚽", "visita": "3D/E/I/J", "flag_v": "⚽", "estadio": "Toronto"},
        {"id": 81, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-01 16:00", "fecha": "01 de Julio", "hora": "16:00", "local": "1I", "flag_l": "⚽", "visita": "3G/H/K/L", "flag_v": "⚽", "estadio": "Filadelfia"},
        {"id": 82, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-01 19:00", "fecha": "01 de Julio", "hora": "19:00", "local": "2G", "flag_l": "⚽", "visita": "2H", "flag_v": "⚽", "estadio": "Kansas City"},
        {"id": 83, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-02 14:00", "fecha": "02 de Julio", "hora": "14:00", "local": "1K", "flag_l": "⚽", "visita": "3I/J/L", "flag_v": "⚽", "estadio": "Miami"},
        {"id": 84, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-02 17:00", "fecha": "02 de Julio", "hora": "17:00", "local": "1G", "flag_l": "⚽", "visita": "3A/B/E/F", "flag_v": "⚽", "estadio": "Vancouver"},
        {"id": 85, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-02 20:00", "fecha": "02 de Julio", "hora": "20:00", "local": "1H", "flag_l": "⚽", "visita": "2J", "flag_v": "⚽", "estadio": "Ciudad de México"},
        {"id": 86, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-03 14:00", "fecha": "03 de Julio", "hora": "14:00", "local": "1J", "flag_l": "⚽", "visita": "2K", "flag_v": "⚽", "estadio": "Monterrey"},
        {"id": 87, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-03 17:00", "fecha": "03 de Julio", "hora": "17:00", "local": "1L", "flag_l": "⚽", "visita": "3G/H/J/K", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 88, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-03 20:00", "fecha": "03 de Julio", "hora": "20:00", "local": "2I", "flag_l": "⚽", "visita": "2L", "flag_v": "⚽", "estadio": "Dallas"},

        # --- OCTAVOS DE FINAL ---
        {"id": 89, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-04 15:00", "fecha": "04 de Julio", "hora": "15:00", "local": "GANADOR P74", "flag_l": "🥇", "visita": "GANADOR P73", "flag_v": "🥇", "estadio": "Philadelphia"},
        {"id": 90, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-04 18:00", "fecha": "04 de Julio", "hora": "18:00", "local": "GANADOR P75", "flag_l": "🥇", "visita": "GANADOR P76", "flag_v": "🥇", "estadio": "Houston"},
        {"id": 91, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-05 14:00", "fecha": "05 de Julio", "hora": "14:00", "local": "GANADOR P77", "flag_l": "🥇", "visita": "GANADOR P78", "flag_v": "🥇", "estadio": "N. York/N. Jersey"},
        {"id": 92, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-05 18:00", "fecha": "05 de Julio", "hora": "18:00", "local": "GANADOR P79", "flag_l": "🥇", "visita": "GANADOR P80", "flag_v": "🥇", "estadio": "Mexico City"},
        {"id": 93, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-06 15:00", "fecha": "06 de Julio", "hora": "15:00", "local": "GANADOR P81", "flag_l": "🥇", "visita": "GANADOR P82", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 94, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-06 19:00", "fecha": "06 de Julio", "hora": "19:00", "local": "GANADOR P83", "flag_l": "🥇", "visita": "GANADOR P84", "flag_v": "🥇", "estadio": "Seattle"},
        {"id": 95, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-07 16:00", "fecha": "07 de Julio", "hora": "16:00", "local": "GANADOR P85", "flag_l": "🥇", "visita": "GANADOR P86", "flag_v": "🥇", "estadio": "Atlanta"},
        {"id": 96, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-07 20:00", "fecha": "07 de Julio", "hora": "20:00", "local": "GANADOR P87", "flag_l": "🥇", "visita": "GANADOR P88", "flag_v": "🥇", "estadio": "Vancouver"},

        # --- CUARTOS DE FINAL ---
        {"id": 97, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-09 16:00", "fecha": "09 de Julio", "hora": "16:00", "local": "GANADOR P89", "flag_l": "🥇", "visita": "GANADOR P90", "flag_v": "🥇", "estadio": "Boston"},
        {"id": 98, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-10 18:00", "fecha": "10 de Julio", "hora": "18:00", "local": "GANADOR P91", "flag_l": "🥇", "visita": "GANADOR P92", "flag_v": "🥇", "estadio": "Los Angeles"},
        {"id": 99, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-11 15:00", "fecha": "11 de Julio", "hora": "15:00", "local": "GANADOR P93", "flag_l": "🥇", "visita": "GANADOR P94", "flag_v": "🥇", "estadio": "Miami"},
        {"id": 100, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-11 20:00", "fecha": "11 de Julio", "hora": "20:00", "local": "GANADOR P95", "flag_l": "🥇", "visita": "GANADOR P96", "flag_v": "🥇", "estadio": "Kansas City"},

        # --- SEMIFINALES ---
        {"id": 101, "fase_bloque": "Fases Finales", "grupo": "Semifinales", "fecha_ref": "2026-07-14 15:00", "fecha": "14 de Julio", "hora": "15:00", "local": "GANADOR P97", "flag_l": "🥇", "visita": "GANADOR P98", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 102, "fase_bloque": "Fases Finales", "grupo": "Semifinales", "fecha_ref": "2026-07-15 18:00", "fecha": "15 de Julio", "hora": "18:00", "local": "GANADOR P99", "flag_l": "🥇", "visita": "GANADOR P100", "flag_v": "🥇", "estadio": "Atlanta"},

        # --- TERCER PUESTO ---
        {"id": 103, "fase_bloque": "Fases Finales", "grupo": "Tercer Puesto", "fecha_ref": "2026-07-18 15:00", "fecha": "18 de Julio", "hora": "15:00", "local": "PERDEDOR P101", "flag_l": "🥉", "visita": "PERDEDOR P102", "flag_v": "🥉", "estadio": "Miami"},

        # --- GRAN FINAL ---
        {"id": 104, "fase_bloque": "Fases Finales", "grupo": "Gran Final", "fecha_ref": "2026-07-19 15:00", "fecha": "19 de Julio", "hora": "15:00", "local": "GANADOR P101", "flag_l": "🏆", "visita": "GANADOR P102", "flag_v": "🏆", "estadio": "N. York/N. Jersey"}
    ]

# FIJAR ORDEN CRONOLÓGICO NATURAL POR FECHA DE REFERENCIA
FIXTURE = sorted(obtener_fixture_completo(), key=lambda x: x['fecha_ref'])

@st.cache_data(ttl=120)
def obtener_frase_futbolera():
    frases = [
        "«Todo lo que sé con mayor certeza sobre la moral y las obligaciones de los hombres, se lo debo al fútbol.» — Albert Camus",
        "«El fútbol es el juego más lindo y más sano del mundo. Yo me equivoqué y pagué, pero la pelota no se mancha.» — Diego Maradona",
        "«El fútbol es música, danza y armonía. Y no hay nada más hermoso que la alegría que le da a la gente.» — Pelé",
        "«Por más que los poderosos lo manipulen, el fútbol sigue queriendo ser el arte de lo imprevisto.» — Eduardo Galeano"
    ]
    return random.choice(frases)

# --- INYECTAR TEMA OSCURO FORZADO ---
st.markdown(
    """
    <script>
        var elements = window.parent.document.getElementsByTagName('html');
        if (elements.length > 0) {
            elements[0].setAttribute('data-theme', 'dark');
        }
    </script>
    """,
    unsafe_allow_html=True
)

# --- CARGA SEGURA DE IMÁGENES ---
def cargar_imagen_local(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

portada_base64 = cargar_imagen_local("portada.jpeg")
fondo_base64 = cargar_imagen_local("fondo.png")
balon_base64 = cargar_imagen_local("balon.jpeg")

# --- DISEÑO Y CSS ---
estilos_css = f"""
<style>
    .stApp {{
        background-color: #0e1117;
        color: #ffffff;
    }}
    {" .stApp { background-image: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85)), url('data:image/png;base64," + fondo_base64 + "'); background-size: cover; background-position: top center; background-attachment: scroll; }" if fondo_base64 else ""}

    .banner-portada {{
        width: 100%;
        height: 220px;
        background-image: url('data:image/jpeg;base64,{portada_base64}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
</style>
"""
st.markdown(estilos_css, unsafe_allow_html=True)

if portada_base64:
    st.markdown('<div class="banner-portada"></div>', unsafe_allow_html=True)
else:
    st.title("🏆 Polla Mundial 2026")

st.markdown(f"<p style='text-align:center; font-style:italic; color:#f1f5f9; font-size:1.05rem; padding:15px 20px 0 20px;'>{obtener_frase_futbolera()}</p>", unsafe_allow_html=True)

if "mensaje_exito" in st.session_state:
    st.success(st.session_state["mensaje_exito"])
    del st.session_state["mensaje_exito"]

st.write("---")

# --- LÓGICA DE PERSISTENCIA ---
def inicializar_base_de_datos():
    base_inicial = {
        "resultados_reales": {},
        "pronosticos": {p: {} for p in PARTICIPANTES}
    }
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            try:
                content = json.load(f)
                if isinstance(content, dict):
                    if "resultados_reales" in content:
                        base_inicial["resultados_reales"] = content["resultados_reales"]
                    if "pronosticos" in content:
                        for p in PARTICIPANTES:
                            base_inicial["pronosticos"][p] = content["pronosticos"].get(p, {})
                    return base_inicial
            except: pass
    return base_inicial

if "datos_globales" not in st.session_state:
    st.session_state["datos_globales"] = inicializar_base_de_datos()

datos = st.session_state["datos_globales"]

def guardar_datos(datos_completos):
    st.session_state["datos_globales"] = datos_completos
    try:
        with open(ARCHIVO_DATOS, "w") as f:
            json.dump(datos_completos, f, indent=4)
    except: pass
        
    if "GITHUB_TOKEN" in st.secrets and REPO_GITHUB != "tu-usuario/polla-mundial-2026":
        try:
            token = st.secrets["GITHUB_TOKEN"]
            url = f"https://api.github.com/repos/{REPO_GITHUB}/contents/{ARCHIVO_DATOS}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            res_get = requests.get(url, headers=headers)
            sha = res_get.json().get("sha", "") if res_get.status_code == 200 else ""
                
            json_texto = json.dumps(datos_completos, indent=4, ensure_ascii=False)
            contenido_base64 = base64.b64encode(json_texto.encode("utf-8")).decode("utf-8")
            
            payload = {"message": "Actualización automática de Polla 🚀", "content": contenido_base64, "branch": "main"}
            if sha: payload["sha"] = sha
            requests.put(url, headers=headers, json=payload)
        except: pass

def calcular_puntos(real_l, real_v, pred_l, pred_v):
    if real_l is None or real_v is None or pred_l is None or pred_v is None:
        return 0, "#64748b", "⚪ Sin Jugar"
    try:
        rl, rv = int(real_l), int(real_v)
        pl, pv = int(pred_l), int(pred_v)
    except: return 0, "#64748b", "⚪ Sin Jugar"
        
    if rl == pl and rv == pv: return 3, "#22c55e", "🟢 Exacto (+3)"
    if (rl > rv) - (rl < rv) == (pl > pv) - (pl < pv): return 1, "#eab308", "🟡 Tendencia (+1)"
    return 0, "#ef4444", "🔴 Fallado (0)"

def verificar_partido_empezado(fecha_ref_str):
    tz_chile = pytz.timezone('America/Santiago')
    try:
        hora_partido_tz = tz_chile.localize(datetime.strptime(fecha_ref_str, "%Y-%m-%d %H:%M"))
        return datetime.now(tz_chile) >= hora_partido_tz
    except: return False

def animar_balon_oficial():
    src_balon = f"data:image/jpeg;base64,{balon_base64}" if balon_base64 else "⚽"
    html_anim = f"<div id='ball-box' style='position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:99999;display:flex;justify-content:center;align-items:center;'><img src='{src_balon}' style='width:160px;height:160px;border-radius:50%;animation: spin 1.5s ease-out forwards;'></div><script>setTimeout(() => {{ document.getElementById('ball-box').remove(); }}, 1500);</script>"
    st.components.v1.html(html_anim, height=0, width=0)

def abreviar_fase(nombre_fase):
    for orig, dest in [("Dieciseisavos", "16avos"), ("Octavos", "8vos"), ("Cuartos", "4tos"), ("Semifinales", "Semis"), ("Tercer Puesto", "3er Puesto"), ("Gran Final", "Final")]:
        nombre_fase = nombre_fase.replace(orig, dest)
    return nombre_fase

def obtener_tablas_grupos():
    stats = {}
    for m in FIXTURE:
        if m["fase_bloque"] in ["Fecha 1", "Fecha 2", "Fecha 3"]:
            g = m["grupo"]
            if g not in stats: stats[g] = {}
            for eq, flag in [(m["local"], m["flag_l"]), (m["visita"], m["flag_v"])]:
                if eq not in stats[g]:
                    stats[g][eq] = {"Bandera": flag, "Pts": 0, "PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "DIF": 0}
            
            pid = str(m["id"])
            real = datos["resultados_reales"].get(pid)
            if real and "l" in real and "v" in real:
                rl, rv = int(real["l"]), int(real["v"])
                loc, vis = m["local"], m["visita"]
                
                stats[g][loc]["PJ"] += 1; stats[g][loc]["GF"] += rl; stats[g][loc]["GC"] += rv; stats[g][loc]["DIF"] += (rl - rv)
                stats[g][vis]["PJ"] += 1; stats[g][vis]["GF"] += rv; stats[g][vis]["GC"] += rl; stats[g][vis]["DIF"] += (rv - rl)
                
                if rl > rv:
                    stats[g][loc]["Pts"] += 3; stats[g][loc]["PG"] += 1; stats[g][vis]["PP"] += 1
                elif rv > rl:
                    stats[g][vis]["Pts"] += 3; stats[g][vis]["PG"] += 1; stats[g][loc]["PP"] += 1
                else:
                    stats[g][loc]["Pts"] += 1; stats[g][loc]["PE"] += 1; stats[g][vis]["Pts"] += 1; stats[g][vis]["PE"] += 1
    return stats

# MOTOR INTERNO: CALCULAR EN TIEMPO REAL LOS 8 MEJORES TERCEROS
def calcular_mejores_terceros_globales(stats_grupos):
    lista_terceros = []
    for g_nome, equipos in stats_grupos.items():
        df_g = pd.DataFrame.from_dict(equipos, orient='index').reset_index()
        df_g.rename(columns={'index': 'Equipo_Puro'}, inplace=True)
        df_g = df_g.sort_values(by=['Pts', 'DIF', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
        if len(df_g) >= 3:
            row_3 = df_g.iloc[2].to_dict()
            row_3["GrupoOriginal"] = g_nome
            lista_terceros.append(row_3)
    if lista_terceros:
        df_t = pd.DataFrame(lista_terceros).sort_values(by=['Pts', 'DIF', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
        return list(df_t.head(8)['Equipo_Puro'])
    return []

# RESOLVER ARBOL DE LLAVES FINAL DINÁMICAMENTE BASADO EN TABLAS PROVISIONALES
def resolver_fixture_dinamico(fixture_base, resultados_reales):
    fixture_copia = [dict(m) for m in fixture_base]
    stats_g = obtener_tablas_grupos()
    
    map_dinamico = {}
    lista_terceros_para_arbol = []
    
    for g_nome, eqs in stats_g.items():
        g_letra = g_nome.replace("Grupo ", "")
        df_g = pd.DataFrame.from_dict(eqs, orient='index').reset_index()
        df_g.rename(columns={'index': 'Equipo_Puro'}, inplace=True)
        df_g = df_g.sort_values(by=['Pts', 'DIF', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
        
        if len(df_g) >= 1: map_dinamico[f"1{g_letra}"] = {"name": df_g.iloc[0]['Equipo_Puro'], "flag": df_g.iloc[0]['Bandera']}
        if len(df_g) >= 2: map_dinamico[f"2{g_letra}"] = {"name": df_g.iloc[1]['Equipo_Puro'], "flag": df_g.iloc[1]['Bandera']}
        if len(df_g) >= 3:
            lista_terceros_para_arbol.append({
                "name": df_g.iloc[2]['Equipo_Puro'], "flag": df_g.iloc[2]['Bandera'], "letra": g_letra,
                "Pts": df_g.iloc[2]['Pts'], "DIF": df_g.iloc[2]['DIF'], "GF": df_g.iloc[2]['GF']
            })
            
    lista_terceros_para_arbol = sorted(lista_terceros_para_arbol, key=lambda x: (x['Pts'], x['DIF'], x['GF']), reverse=True)
    top_8_thirds_arbol = lista_terceros_para_arbol[:8]
    
    usados_thirds = set()
    for m in fixture_copia:
        # Resolver locales
        loc_key = m["local"]
        if loc_key in map_dinamico:
            m["local"] = map_dinamico[loc_key]["name"].upper(); m["flag_l"] = map_dinamico[loc_key]["flag"]
        elif loc_key.startswith("3") and "/" in loc_key:
            letras_ok = [c for c in loc_key if c.isalpha()]
            found = None
            for t in top_8_thirds_arbol:
                if t["letra"] in letras_ok and t["name"] not in usados_thirds:
                    found = t; break
            if found:
                m["local"] = found["name"].upper(); m["flag_l"] = found["flag"]; usados_thirds.add(found["name"])
        elif "GANADOR P" in loc_key:
            prev_id = loc_key.replace("GANADOR P", "")
            if prev_id in resultados_reales and "avanza" in resultados_reales[prev_id]:
                m["local"] = resultados_reales[prev_id]["avanza"].upper(); m["flag_l"] = "✅"
        elif "PERDEDOR P" in loc_key:
            prev_id = loc_key.replace("PERDEDOR P", "")
            if prev_id in resultados_reales and "l" in resultados_reales[prev_id]:
                r_m = resultados_reales[prev_id]
                prev_match = next((x for x in fixture_copia if str(x["id"]) == prev_id), None)
                if prev_match:
                    if int(r_m["l"]) > int(r_m["v"]): m["local"] = prev_match["visita"].upper(); m["flag_l"] = prev_match["flag_v"]
                    else: m["local"] = prev_match["local"].upper(); m["flag_l"] = prev_match["flag_l"]
                    
        # Resolver visitas
        vis_key = m["visita"]
        if vis_key in map_dinamico:
            m["visita"] = map_dinamico[vis_key]["name"].upper(); m["flag_v"] = map_dinamico[vis_key]["flag"]
        elif vis_key.startswith("3") and "/" in vis_key:
            letras_ok = [c for c in vis_key if c.isalpha()]
            found = None
            for t in top_8_thirds_arbol:
                if t["letra"] in letras_ok and t["name"] not in usados_thirds:
                    found = t; break
            if found:
                m["visita"] = found["name"].upper(); m["flag_v"] = found["flag"]; usados_thirds.add(found["name"])
        elif "GANADOR P" in vis_key:
            prev_id = vis_key.replace("GANADOR P", "")
            if prev_id in resultados_reales and "avanza" in resultados_reales[prev_id]:
                m["visita"] = resultados_reales[prev_id]["avanza"].upper(); m["flag_v"] = "✅"
        elif "PERDEDOR P" in vis_key:
            prev_id = vis_key.replace("PERDEDOR P", "")
            if prev_id in resultados_reales and "l" in resultados_reales[prev_id]:
                r_m = resultados_reales[prev_id]
                prev_match = next((x for x in fixture_copia if str(x["id"]) == prev_id), None)
                if prev_match:
                    if int(r_m["l"]) > int(r_m["v"]): m["visita"] = prev_match["visita"].upper(); m["flag_v"] = prev_match["flag_v"]
                    else: m["visita"] = prev_match["local"].upper(); m["flag_v"] = prev_match["flag_l"]
    return fixture_copia

FIXTURE_DINAMICO = resolver_fixture_dinamico(FIXTURE, datos["resultados_reales"])

# --- PESTAÑAS PRINCIPALES CON ORDEN DE PORTADA REESTRUCTURADO ---
tabs = st.tabs(["📊 RANKING FAMILIAR", "✍️ PRONÓSTICOS", "📅 CRONOGRAMA COMPLETO MUNDIAL", "🏆 EL MUNDIAL", "📜 BASES DEL JUEGO", "⚙️ PANEL CONTROL"])

# --- TAB 1: PORTADA / RANKING FAMILIAR (ALTURA CORREGIDA PARA DESPLIEGUE COMPLETO) ---
with tabs[0]:
    st.markdown("<h2>📊 RENDIMIENTO DE LA FAMILIA</h2>", unsafe_allow_html=True)
    tabla_posiciones = []
    fondo_total = len(PARTICIPANTES) * CUOTA_INSCRIPCION
    
    for p in PARTICIPANTES:
        pts_totales, exactos, tendencias = 0, 0, 0
        for part in FIXTURE_DINAMICO:
            pid = str(part["id"])
            real, pred = datos["resultados_reales"].get(pid), datos["pronosticos"].get(p, {}).get(pid)
            if real and pred and "l" in real and "v" in real and "l" in pred and "v" in pred:
                pts, _, _ = calcular_puntos(real["l"], real["v"], pred["l"], pred["v"])
                pts_totales += pts
                if pts == 3: exactos += 1
                elif pts == 1: tendencias += 1
        tabla_posiciones.append({"Participante": p, "Puntos Totales 🌟": pts_totales, "Marcadores Exactos 🎯": exactos, "Aciertos Simples (1pt) 🏟️": tendencias})
    
    df_tabla = pd.DataFrame(tabla_posiciones).sort_values(by=["Puntos Totales 🌟", "Marcadores Exactos 🎯"], ascending=False).reset_index(drop=True)
    df_tabla.index += 1
    
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1: st.markdown(f"<div style='background:rgba(34,197,94,0.15);padding:15px;border-radius:10px;border:1px solid #22c55e;text-align:center;'><span>🥇 1er Lugar</span><br><strong style='font-size:1.6rem;color:#fbbf24;'>{df_tabla.iloc[0]['Participante'].upper()}</strong><br><span>${fondo_total * 0.50:,.0f}</span></div>", unsafe_allow_html=True)
    with c_p2: st.markdown(f"<div style='background:rgba(234,179,8,0.1);padding:15px;border-radius:10px;border:1px solid #eab308;text-align:center;'><span>🥈 2do Lugar</span><br><strong style='font-size:1.4rem;color:#e2e8f0;'>{df_tabla.iloc[1]['Participante'].upper()}</strong><br><span>${fondo_total * 0.333:,.0f}</span></div>", unsafe_allow_html=True)
    with c_p3: st.markdown(f"<div style='background:rgba(239,68,68,0.1);padding:15px;border-radius:10px;border:1px solid #ef4444;text-align:center;'><span>🥉 3er Lugar</span><br><strong style='font-size:1.4rem;color:#e2e8f0;'>{df_tabla.iloc[2]['Participante'].upper()}</strong><br><span>${fondo_total * 0.166:,.0f}</span></div>", unsafe_allow_html=True)
    st.write("---")
    # ST.TABLE USA HTML NATIVO: NO FALLA EN IPAD Y MUESTRA A LOS 11 JUGADORES DE GOLPE
    st.table(df_tabla)


# --- TAB 2: PRONÓSTICOS ---
    with tabs[1]:
        st.markdown("<h2>✍️ ARMA TU JUGADA MUNDIALERA</h2>", unsafe_allow_html=True)
        usuario = st.selectbox("Selecciona tu nombre para apostar:", PARTICIPANTES)
    
    # Lógica inteligente para ocultar fases que ya están completamente terminadas
    fases_opciones = []
    for fase_val, etiqueta in [("Fecha 1", "Fecha 1 (Partidos 1-24)"), ("Fecha 2", "Fecha 2 (Partidos 25-48)"), ("Fecha 3", "Fecha 3 (Partidos 49-72)"), ("Fases Finales", "Fases Finales")]:
        partidos_fase = [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == fase_val or (fase_val=="Fases Finales" and "Fases" in m["fase_bloque"])]
        todos_cerrados = all(str(p["id"]) in datos["resultados_reales"] for p in partidos_fase)
        if not todos_cerrados or not partidos_fase:
            fases_opciones.append(etiqueta)

    if not fases_opciones: fases_opciones = ["Fases Finales"] # Respaldo por si todo terminó
    
    bloque_seleccionado = st.radio("Filtrar por fase del torneo:", fases_opciones, horizontal=True)
    filtro_fia = bloque_seleccionado.split(" (")[0] if "(" in bloque_seleccionado else "Fases Finales"
    
    with st.form(key=f"form_seguro_{usuario}_{filtro_fia}"):
        resp_temp = {}
        for part in [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == filtro_fia]:
            pid = str(part["id"])
            pred_actual = datos["pronosticos"].get(usuario, {}).get(pid, {})
            real_actual = datos["resultados_reales"].get(pid)
            
            ya_empezo = verificar_partido_empezado(part.get("fecha_ref", "2026-06-11 00:00"))
            bloquear = ya_empezo or (pid in datos["resultados_reales"])
            
            real_l, real_v = (real_actual.get("l"), real_actual.get("v")) if real_actual else (None, None)
            pred_l, pred_v = pred_actual.get("l"), pred_actual.get("v")
            
            _, color_hex, texto_status = calcular_puntos(real_l, real_v, pred_l, pred_v)
            if pid in datos["resultados_reales"]: texto_status += " | 🔒 CERRADO"
            elif ya_empezo: color_hex, texto_status = "#be123c", "🔒 EN CURSO"
            
            st.markdown(f"<div style='background:rgba(30,41,59,0.7);padding:6px 12px;border-left:5px solid {color_hex};font-size:0.85rem;margin-top:12px;'><b>{part['grupo'].upper()}</b> ({part['fecha']} - {part['hora']} hrs) | <span style='color:{color_hex};font-weight:bold;'>{texto_status}</span></div>", unsafe_allow_html=True)
            
            c_l, c_in1, c_in2, c_v = st.columns([4, 1, 1, 4])
            with c_l: st.markdown(f"<div style='text-align:right;font-weight:bold;font-size:1rem;padding-top:6px;'>{part['local']} {part['flag_l']}</div>", unsafe_allow_html=True)
            with c_in1: g_l = st.number_input("L", 0, 15, pred_l, key=f"l_{usuario}_{pid}", disabled=bloquear, label_visibility="collapsed")
            with c_in2: g_v = st.number_input("V", 0, 15, pred_v, key=f"v_{usuario}_{pid}", disabled=bloquear, label_visibility="collapsed")
            with c_v: st.markdown(f"<div style='text-align:left;font-weight:bold;font-size:1rem;padding-top:6px;'>{part['flag_v']} {part['visita']}</div>", unsafe_allow_html=True)
            resp_temp[pid] = {"l": g_l, "v": g_v}
            
        st.write("---")
        if st.form_submit_button("💾 GUARDAR APUESTAS", use_container_width=True):
            if usuario not in datos["pronosticos"]: datos["pronosticos"][usuario] = {}
            for pid, scores in resp_temp.items():
                p_info = next((m for m in FIXTURE_DINAMICO if str(m["id"]) == pid), None)
                if p_info and not verificar_partido_empezado(p_info.get("fecha_ref", "")) and pid not in datos["resultados_reales"]:
                    if scores["l"] is not None and scores["v"] is not None: datos["pronosticos"][usuario][pid] = {"l": int(scores["l"]), "v": int(scores["v"])}
                    else: datos["pronosticos"][usuario].pop(pid, None)
            guardar_datos(datos)
            animar_balon_oficial()
            st.session_state["mensaje_exito"] = "¡Tus pronósticos se guardaron y sincronizaron con éxito!"
            st.rerun()

# --- TAB 3: CRONOGRAMA DE IMPRESIÓN LIMPIA (SIN ENCABEZADOS DE NÚMERO NI ESTADIO) ---
with tabs[2]:
    st.markdown("<h2>📅 CRONOGRAMA COMPLETO MUNDIAL</h2>", unsafe_allow_html=True)
    lista_cronograma = []
    for part in FIXTURE_DINAMICO:
        pid = str(part["id"])
        real = datos["resultados_reales"].get(pid)
        
        fase_abr = abreviar_fase(part["grupo"])
        dia_hora_fmt = f"{part['fecha'].replace(' de ', ' ')}, {part['hora']} hrs"
        
        if real:
            estado = "🔒 FINALIZADO"
            partido_fmt = f"{part['flag_l']} {part['local']}  {real['l']} - {real['v']}  {part['flag_v']} {part['visita']}"
        elif verificar_partido_empezado(part.get("fecha_ref", "")):
            estado = "⏱️ EN CURSO"
            partido_fmt = f"{part['flag_l']} {part['local']}  vs  {part['flag_v']} {part['visita']}"
        else:
            estado = "🔒 CERRADO" if (pid in datos["resultados_reales"]) else "🟢 ABIERTO"
            partido_fmt = f"{part['flag_l']} {part['local']}  vs  {part['flag_v']} {part['visita']}"
        
        lista_cronograma.append({
            "fecha_orden": part["fecha_ref"],
            "Fase": fase_abr,
            "Día y Hora": dia_hora_fmt,
            "Partido y Resultado": partido_fmt,
            "Estado": estado
        })
        
    df_crono = pd.DataFrame(lista_cronograma).sort_values("fecha_orden").drop(columns=["fecha_orden"])
    st.dataframe(df_crono.style.apply(lambda r: ['background:rgba(71,85,105,0.3);color:#cbd5e1;font-style:italic;']*len(r) if r["Estado"]=="🔒 FINALIZADO" else ['background:rgba(186,18,60,0.2);color:#fda4af;font-weight:bold;']*len(r) if r["Estado"]=="⏱️ EN CURSO" else ['']*len(r), axis=1), use_container_width=True, hide_index=True)

# --- TAB 4: EL MUNDIAL (FUSIÓN RESPONSIVA GRUPOS + LLAVES DINÁMICAS) ---
with tabs[3]:
    st.markdown("<h2>🏆 ESTADÍSTICAS DEL MUNDIAL REAL</h2>", unsafe_allow_html=True)
    seccion_mundial = st.radio("Selecciona qué deseas revisar:", ["Tablas de Posiciones (Grupos)", "Llaves de la Fase Final (Árbol Dynamic)"], horizontal=True)
    st.write("---")
    
    if seccion_mundial == "Tablas de Posiciones (Grupos)":
        stats_grupos = obtener_tablas_grupos()
        mejores_3ros_ok = calcular_mejores_terceros_globales(stats_grupos)
        
        # FILAS EXPLICITAS DE 3 COLUMNAS PARA EVITAR LA CORRUPCIÓN DE ENLACE EN IPHONE (MANTIENE ORDEN A,B,C,D...)
        orden_bloques = [
            ["Grupo A", "Grupo B", "Grupo C"],
            ["Grupo D", "Grupo E", "Grupo F"],
            ["Grupo G", "Grupo H", "Grupo I"],
            ["Grupo J", "Grupo K", "Grupo L"]
        ]
        
        for fila in orden_bloques:
            cols_g = st.columns(3)
            for i, nombre_grupo in enumerate(fila):
                equipos = stats_grupos.get(nombre_grupo, {})
                df_g = pd.DataFrame.from_dict(equipos, orient='index').reset_index()
                df_g.rename(columns={'index': 'Equipo_Puro'}, inplace=True)
                
                if not df_g.empty:
                    df_g = df_g.sort_values(by=['Pts', 'DIF', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
                    df_g['Equipo'] = df_g.apply(lambda r: f"{r['Bandera']} {r['Equipo_Puro']}", axis=1)
                    df_g = df_g[['Equipo', 'Pts', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF']]
                    df_g.index += 1
                    
                    # PINTADO UNIFICADO: 1RO, 2DO Y MEJORES TERCEROS QUEDAN VERDES
                    def color_filas_grupo(row):
                        eq_limpio = row['Equipo'].split(" ", 1)[1] if " " in row['Equipo'] else row['Equipo']
                        if row.name <= 2:
                            return ['background-color: rgba(34, 197, 94, 0.18)'] * len(row)
                        elif row.name == 3 and eq_limpio in mejores_3ros_ok:
                            return ['background-color: rgba(34, 197, 94, 0.18)'] * len(row)
                        return [''] * len(row)
                    
                    with cols_g[i]:
                        st.markdown(f"<h4 style='color:#fbbf24;margin-bottom:4px;'>{nombre_grupo}</h4>", unsafe_allow_html=True)
                        st.dataframe(df_g.style.apply(color_filas_grupo, axis=1), use_container_width=True, hide_index=True)
            st.write("")
                    
    else:
        fases_orden = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinales", "Tercer Puesto", "Gran Final"]
        for fase in fases_orden:
            st.markdown(f"<h3 style='text-align:center; color:#fbbf24; border-bottom: 1px solid #475569; padding-bottom:10px;'>{fase.upper()}</h3>", unsafe_allow_html=True)
            partidos_fase = [m for m in FIXTURE_DINAMICO if m["grupo"] == fase]
            cols_llaves = st.columns(2) if len(partidos_fase) > 1 else st.columns(1)
            
            for i, p in enumerate(partidos_fase):
                pid = str(p["id"])
                real = datos["resultados_reales"].get(pid)
                estado_texto = "⏳ Esperando clasificación de fase previa" if ("GANADOR" in p['local'] or "1A" in p['local'] or "2A" in p['local']) else "🔜 Listo para jugarse"
                bg_color, borde, goles_l, goles_v = "rgba(30, 41, 59, 0.6)", "1px solid #475569", "-", "-"
                
                if real:
                    goles_l, goles_v = real["l"], real["v"]
                    estado_texto = f"✅ Avanza: {real.get('avanza', 'Ganador')}"
                    bg_color, borde = "rgba(15, 23, 42, 0.9)", "2px solid #22c55e"
                elif verificar_partido_empezado(p.get("fecha_ref", "")):
                    estado_texto, borde = "⏱️ En Curso", "2px solid #e11d48"
                    
                tarjeta_html = f"""
                <div style='background:{bg_color}; border:{borde}; border-radius:8px; padding:12px; margin-bottom:15px;'>
                    <div style='font-size:0.8rem; color:#94a3b8; text-align:center; margin-bottom:8px;'>{p['fecha']} ({p['hora']} hrs)</div>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <div style='width:42%; text-align:right; font-weight:bold;'>{p['local']} {p['flag_l']}</div>
                        <div style='width:16%; text-align:center; font-size:1.1rem; font-weight:bold; color:#fbbf24; background:#000; padding:2px; border-radius:4px;'>{goles_l} - {goles_v}</div>
                        <div style='width:42%; text-align:left; font-weight:bold;'>{p['flag_v']} {p['visita']}</div>
                    </div>
                    <div style='font-size:0.75rem; color:#64748b; text-align:center; margin-top:8px; font-weight:bold;'>{estado_texto}</div>
                </div>
                """
                with cols_llaves[i % len(cols_llaves)]: st.markdown(tarjeta_html, unsafe_allow_html=True)

# --- TAB 5: BASES AL FINAL ---
with tabs[4]:
    st.markdown("""
    ## 📜 BASES REGLAMENTARIAS POLLA FAMILIAR
    
    ⚽ **Inscripción:** $5.000 por cartilla. El 100% de la recaudación va directo al pozo familiar.
    
    📅 **Plazo de envío:** Puedes ingresar, cambiar o rehacer tu pronóstico las veces que quieras **hasta el minuto exacto en que comience el partido**. Una vez comenzado, se congela.
    
    ⏱️ **Tiempo Reglamentario:** Válido exclusivamente para los **90 minutos reglamentarios** más el descuento del árbitro. No considera prórrogas ni penales.
    
    💰 **Distribución de Premios:**
    * 🥇 **1er Lugar:** 50% de la recaudación total.
    * 🥈 **2do Lugar:** 33,3% de la recaudación total.
    * 🥉 **3er Lugar:** 16,6% de la recaudación total.
    
    📊 **Puntuación del Juego:**
    * **3 puntos (Marcador Exacto):** Le achuntaste al ganador y a la cantidad exacta de goles de ambos.
    * **1 punto (Tendencia):** Le achuntaste al ganador o al empate, pero erraste en el número de goles.
    * **0 puntos:** No se acierta a la tendencia.
    """)

# --- TAB 6: PANEL CONTROL (ADMIN + GENERADOR WHATSAPP SEGURO) ---
with tabs[5]:
    st.markdown("<h2>⚙️ PANEL DE CONTROL EXCLUSIVO</h2>", unsafe_allow_html=True)
    if st.text_input("Ingresa Token de Seguridad Mandamás:", type="password") == PASSWORD_ADMIN:
        st.success("🔓 Acceso Concedido de forma exitosa")
        
        # 🛟 BOTÓN DE RESPALDO MANUAL AL IPAD
        st.download_button("📥 DESCARGAR COPIA DE SEGURIDAD (.JSON) AL IPAD", data=json.dumps(datos, indent=4, ensure_ascii=False), file_name="datos_polla.json", mime="application/json", use_container_width=True)
        st.write("---")
        
       # 📱 UBICACIÓN SEGURA: GENERADOR DIARIO PARA WHATSAPP
        st.markdown("### 📱 GENERADOR DIARIO RECORDATORIO WHATSAPP")
        
        # Filtro inteligente: Mostrar solo fechas que tengan partidos pendientes o en curso
        fechas_disponibles = []
        for m in FIXTURE_DINAMICO:
            partidos_dia = [p for p in FIXTURE_DINAMICO if p["fecha"] == m["fecha"]]
            todos_cerrados = all(str(p["id"]) in datos["resultados_reales"] for p in partidos_dia)
            if not todos_cerrados and m["fecha"] not in fechas_disponibles:
                fechas_disponibles.append(m["fecha"])
                
        if not fechas_disponibles: fechas_disponibles = [FIXTURE_DINAMICO[-1]["fecha"]]
        
        fecha_sel = st.selectbox("Elige la fecha para enviar al grupo familiar:", fechas_disponibles)
        
        texto_whatsapp = f"🏆 *PARTIDOS DEL {fecha_sel.upper()}* 🏆\n"
        texto_whatsapp += "=============================\n\n"
        
        partidos_del_dia = [m for m in FIXTURE_DINAMICO if m["fecha"] == fecha_sel]
        for part in partidos_del_dia:
            pid = str(part["id"])
            ya_empezo = verificar_partido_empezado(part.get("fecha_ref", ""))
            real = datos["resultados_reales"].get(pid)
            grupo_fmt = abreviar_fase(part["grupo"])
                
            if real:
                texto_whatsapp += f"🕣 *{part['hora']} hrs* ({grupo_fmt}):\n{part['flag_l']} {part['local']} *{real['l']} - {real['v']}* {part['visita']} {part['flag_v']} ✅\n\n"
            elif ya_empezo:
                texto_whatsapp += f"🕣 *{part['hora']} hrs* ({grupo_fmt}):\n{part['flag_l']} {part['local']} *vs* {part['visita']} {part['flag_v']} ⏳ (Jugándose)\n\n"
            else:
                texto_whatsapp += f"🕣 *{part['hora']} hrs* ({grupo_fmt}):\n{part['flag_l']} {part['local']} *vs* {part['visita']} {part['flag_v']}\n\n"
                
        texto_whatsapp += "⚽*¡No olviden ingresar o modificar sus pronósticos en la app antes del pitazo inicial de cada partido!*⚽"
        st.text_area("Haz TRIPLE TOQUE adentro para copiar los partidos del día:", value=texto_whatsapp, height=180)
        st.write("---")
        
        # 📊 NUEVA MEJORA: GENERADOR DE RESUMEN DE APUESTAS POR PARTIDO
        st.markdown("### 📊 GENERADOR DE RESUMEN DE APUESTAS")
        
        MAPA_APODOS = {
            "Constanza": "Coni", "David": "David", "Franco": "Franco", 
            "José Alonso": "José Alonso", "José Mario": "José Mario", 
            "Leonardo": "Leo", "Marlene": "Mane", "Mario": "Mario", 
            "Néstor": "Néstor", "Renato": "Renato", "Sergio": "Sergio"
        }
        
        # Filtro inteligente: Mostrar solo partidos que NO tienen resultado oficial
        opciones_partidos = []
        for p in FIXTURE_DINAMICO:
            if str(p["id"]) not in datos["resultados_reales"]:
                opciones_partidos.append(f"Partido #{p['id']} | {p['local']} vs {p['visita']}")
                
        if not opciones_partidos: opciones_partidos = ["Todos los partidos han finalizado"]
        
        partido_seleccionado = st.selectbox("Selecciona el partido para el resumen de WhatsApp:", opciones_partidos)
        
        if partido_seleccionado != "Todos los partidos han finalizado":
            pid_seleccionado = partido_seleccionado.split("Partido #")[1].split(" |")[0]
            p_obj = next((x for x in FIXTURE_DINAMICO if str(x["id"]) == pid_seleccionado), None)
            
            if p_obj:
                # El título ahora incluye las banderas Y los nombres
                texto_resumen = f"Resumen {p_obj['flag_l']} {p_obj['local']} vs {p_obj['visita']} {p_obj['flag_v']}\n"
                texto_resumen += "=============================\n"
                
                for part_name in PARTICIPANTES:
                    apodo = MAPA_APODOS.get(part_name, part_name)
                    pred_user = datos["pronosticos"].get(part_name, {}).get(pid_seleccionado)
                    
                    if pred_user and "l" in pred_user and "v" in pred_user:
                        # El cuerpo solo muestra las banderas
                        texto_resumen += f"{apodo}: {p_obj['flag_l']} {pred_user['l']} - {pred_user['v']} {p_obj['flag_v']}\n"
                    else:
                        texto_resumen += f"{apodo}: ⚪ Sin Pronóstico\n"
                
                st.text_area("Haz TRIPLE TOQUE adentro para copiar el resumen de apuestas:", value=texto_resumen, height=280)
        st.write("---")
        
        # ADMINISTRACIÓN DE RESULTADOS
        accion_admin = st.radio("Acción de Control:", ["Marcadores Oficiales Reales", "Forzar Apuestas Familiares"], horizontal=True)
        fase_admin = st.selectbox("Bloque de Partidos:", ["Fecha 1", "Fecha 2", "Fecha 3", "Fases Finales"])
        st.write("---")
        
        if accion_admin == "Marcadores Oficiales Reales":
            nuevos_cierres = dict(datos["resultados_reales"])
            for part in [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == fase_admin]:
                pid = str(part["id"])
                real_actual = datos["resultados_reales"].get(pid, {"l": 0, "v": 0})
                st.markdown(f"**Partido #{pid} ({part['grupo']}): {part['local']} vs {part['visita']}**")
                c_l, c_v, c_chk = st.columns([2, 2, 3])
                with c_l: g_l = st.number_input("L", 0, 15, int(real_actual.get("l", 0)), key=f"ar_{pid}l", label_visibility="collapsed")
                with c_v: g_v = st.number_input("V", 0, 15, int(real_actual.get("v", 0)), key=f"ar_{pid}v", label_visibility="collapsed")
                with c_chk: fin = st.checkbox("Cerrar Oficial", value=(pid in datos["resultados_reales"]), key=f"chk_{pid}")
                
                if fin: 
                    nuevos_cierres[pid] = {"l": g_l, "v": g_v}
                    if "Fases Finales" in part["fase_bloque"]:
                        if g_l == g_v: nuevos_cierres[pid]["avanza"] = st.selectbox("🏆 Clasifica:", [part['local'], part['visita']], key=f"avanza_{pid}")
                        else: nuevos_cierres[pid]["avanza"] = part['local'] if g_l > g_v else part['visita']
                else: nuevos_cierres.pop(pid, None)
            
            if st.button("🔄 ACTUALIZAR MARCADORES MUNDIALES", use_container_width=True):
                datos["resultados_reales"] = nuevos_cierres
                guardar_datos(datos)
                st.session_state["mensaje_exito"] = "¡Marcadores actualizados con éxito y sincronizados en GitHub!"
                st.rerun()

        elif accion_admin == "Forzar Apuestas Familiares":
            jugador = st.selectbox("Seleccionar Jugador:", PARTICIPANTES)
            resp_admin = {}
            for part in [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == fase_admin]:
                pid = str(part["id"])
                pred = datos["pronosticos"].get(jugador, {}).get(pid, {})
                st.markdown(f"**Partido #{pid}: {part['local']} vs {part['visita']}**")
                c_l, c_v = st.columns(2)
                with c_l: gl = st.number_input("L", 0, 15, pred.get("l"), key=f"fa_{pid}l")
                with c_v: gv = st.number_input("V", 0, 15, pred.get("v"), key=f"fa_{pid}v")
                resp_admin[pid] = {"l": gl, "v": gv}
                
            if st.button(f"💾 SALVAR CARTILLA DE {jugador.upper()}", use_container_width=True):
                if jugador not in datos["pronosticos"]: datos["pronosticos"][jugador] = {}
                for pid, sc in resp_admin.items():
                    if sc["l"] is not None and sc["v"] is not None: datos["pronosticos"][jugador][pid] = {"l": int(sc["l"]), "v": int(sc["v"])}
                    else: datos["pronosticos"][jugador].pop(pid, None)
                guardar_datos(datos)
                st.session_state["mensaje_exito"] = f"¡Las apuestas forzadas de {jugador} se subieron con éxito!"
                st.rerun()
