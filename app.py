import streamlit as st
import pandas as pd
import json
import os
import random
import base64

# CONFIGURACIÓN DE LA PÁGINA (Diseño Responsive)
st.set_page_config(page_title="Polla Mundial 2026", page_icon="⚽", layout="wide")

# CONSOLIDADO OFICIAL DE LOS 72 PARTIDOS DE GRUPOS EXTRAÍDOS DE TU EXCEL
@st.cache_data
def obtener_fixture_completo():
    return [
        # --- FECHA 1 (Partidos 1 al 24) ---
        {"id": 1, "fase_bloque": "Fecha 1", "grupo": "Grupo A", "fecha": "11 de Junio", "hora": "15:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Ciudad de México"},
        {"id": 2, "fase_bloque": "Fecha 1", "grupo": "Grupo A", "fecha": "11 de Junio", "hora": "22:00", "local": "COREA DEL SUR", "flag_l": "🇰🇷", "visita": "REP. CHECA", "flag_v": "🇨🇿", "estadio": "Guadalajara"},
        {"id": 3, "fase_bloque": "Fecha 1", "grupo": "Grupo B", "fecha": "12 de Junio", "hora": "15:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Toronto"},
        {"id": 4, "fase_bloque": "Fecha 1", "grupo": "Grupo D", "fecha": "12 de Junio", "hora": "21:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "Los Angeles"},
        {"id": 5, "fase_bloque": "Fecha 1", "grupo": "Grupo C", "fecha": "13 de Junio", "hora": "21:00", "local": "HAITÍ", "flag_l": "🇭🇹", "visita": "ESCOCIA", "flag_v": "🏴\u200d󠁧\u200db\u200ds\u200dc\u200dt\u200d󠁿", "estadio": "Boston"},
        {"id": 6, "fase_bloque": "Fecha 1", "grupo": "Grupo D", "fecha": "14 de Junio", "hora": "00:00", "local": "AUSTRALIA", "flag_l": "🇦🇺", "visita": "TURQUÍA", "flag_v": "🇹🇷", "estadio": "Vancouver"},
        {"id": 7, "fase_bloque": "Fecha 1", "grupo": "Grupo C", "fecha": "13 de Junio", "hora": "18:00", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "N. York/N. Jersey"},
        {"id": 8, "fase_bloque": "Fecha 1", "grupo": "Grupo B", "fecha": "13 de Junio", "hora": "15:00", "local": "CATAR", "flag_l": "🇶🇦", "visita": "SUIZA", "flag_v": "🇨🇭", "estadio": "San Francisco"},
        {"id": 9, "fase_bloque": "Fecha 1", "grupo": "Grupo E", "fecha": "14 de Junio", "hora": "19:00", "local": "COSTA DE MARFIL", "flag_l": "🇨🇮", "visita": "ECUADOR", "flag_v": "🇪🇨", "estadio": "Filadelfia"},
        {"id": 10, "fase_bloque": "Fecha 1", "grupo": "Grupo E", "fecha": "14 de Junio", "hora": "13:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Houston"},
        {"id": 11, "fase_bloque": "Fecha 1", "grupo": "Grupo F", "fecha": "14 de Junio", "hora": "16:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Dallas"},
        {"id": 12, "fase_bloque": "Fecha 1", "grupo": "Grupo F", "fecha": "14 de Junio", "hora": "22:00", "local": "SUECIA", "flag_l": "🇸🇪", "visita": "TÚNEZ", "flag_v": "🇹🇳", "estadio": "Monterrey"},
        {"id": 13, "fase_bloque": "Fecha 1", "grupo": "Grupo H", "fecha": "15 de Junio", "hora": "18:00", "local": "ARABIA SAUDITA", "flag_l": "🇸🇦", "visita": "URUGUAY", "flag_v": "🇺🇾", "estadio": "Miami"},
        {"id": 14, "fase_bloque": "Fecha 1", "grupo": "Grupo H", "fecha": "15 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Atlanta"},
        {"id": 15, "fase_bloque": "Fecha 1", "grupo": "Grupo G", "fecha": "15 de Junio", "hora": "21:00", "local": "IRÁN", "flag_l": "🇮🇷", "visita": "NUEVA ZELANDA", "flag_v": "🇳🇿", "estadio": "Los Angeles"},
        {"id": 16, "fase_bloque": "Fecha 1", "grupo": "Grupo G", "fecha": "15 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Seattle"},
        {"id": 17, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha": "16 de Junio", "hora": "15:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 18, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha": "16 de Junio", "hora": "18:00", "local": "IRAK", "flag_l": "🇮🇶", "visita": "NORUEGA", "flag_v": "🇳🇴", "estadio": "Boston"},
        {"id": 19, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha": "16 de Junio", "hora": "21:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "Kansas City"},
        {"id": 20, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha": "17 de Junio", "hora": "00:00", "local": "AUSTRIA", "flag_l": "🇦🇹", "visita": "JORDANIA", "flag_v": "🇯🇴", "estadio": "San Francisco"},
        {"id": 21, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha": "17 de Junio", "hora": "19:00", "local": "GHANA", "flag_l": "🇬🇭", "visita": "PANAMÁ", "flag_v": "🇵🇦", "estadio": "Toronto"},
        {"id": 22, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha": "17 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "🏴\u200d󠁧\u200de\u200dn\u200dg\u200dt\u200d󠁿", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Dallas"},
        {"id": 23, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha": "17 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "REP. DEL CONGO", "flag_v": "🇨🇬", "estadio": "Houston"},
        {"id": 24, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha": "17 de Junio", "hora": "22:00", "local": "UZBEKISTÁN", "flag_l": "🇺🇿", "visita": "COLOMBIA", "flag_v": "🇨🇴", "estadio": "Ciudad de México"},

        # --- FECHA 2 (Partidos 25 al 48) ---
        {"id": 25, "fase_bloque": "Fecha 2", "grupo": "Grupo A", "fecha": "18 de Junio", "hora": "12:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Atlanta"},
        {"id": 26, "fase_bloque": "Fecha 2", "grupo": "Grupo B", "fecha": "18 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Los Angeles"},
        {"id": 27, "fase_bloque": "Fecha 2", "grupo": "Grupo B", "fecha": "18 de Junio", "hora": "18:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Vancouver"},
        {"id": 28, "fase_bloque": "Fecha 2", "grupo": "Grupo A", "fecha": "18 de Junio", "hora": "21:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Guadalajara"},
        {"id": 29, "fase_bloque": "Fecha 2", "grupo": "Grupo C", "fecha": "19 de Junio", "hora": "20:30", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Filadelfia"},
        {"id": 30, "fase_bloque": "Fecha 2", "grupo": "Grupo C", "fecha": "19 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "🏴\u200d󠁧\u200db\u200ds\u200dc\u200dt\u200d󠁿", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "Boston"},
        {"id": 31, "fase_bloque": "Fecha 2", "grupo": "Grupo D", "fecha": "19 de Junio", "hora": "23:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "San Francisco"},
        {"id": 32, "fase_bloque": "Fecha 2", "grupo": "Grupo D", "fecha": "19 de Junio", "hora": "15:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "Seattle"},
        {"id": 33, "fase_bloque": "Fecha 2", "grupo": "Grupo E", "fecha": "20 de Junio", "hora": "16:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Toronto"},
        {"id": 34, "fase_bloque": "Fecha 2", "grupo": "Grupo E", "fecha": "20 de Junio", "hora": "20:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Kansas City"},
        {"id": 35, "fase_bloque": "Fecha 2", "grupo": "Grupo F", "fecha": "20 de Junio", "hora": "13:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Houston"},
        {"id": 36, "fase_bloque": "Fecha 2", "grupo": "Grupo F", "fecha": "21 de Junio", "hora": "00:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Monterrey"},
        {"id": 37, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha": "21 de Junio", "hora": "18:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Miami"},
        {"id": 38, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha": "21 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Atlanta"},
        {"id": 39, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha": "21 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Los Angeles"},
        {"id": 40, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha": "21 de Junio", "hora": "21:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Vancouver"},
        {"id": 41, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha": "22 de Junio", "hora": "20:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 42, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha": "22 de Junio", "hora": "17:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Filadelfia"},
        {"id": 43, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha": "22 de Junio", "hora": "13:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Dallas"},
        {"id": 44, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha": "22 de Junio", "hora": "23:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "San Francisco"},
        {"id": 45, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha": "23 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "🏴\u200d󠁧\u200de\u200dn\u200dg\u200dt\u200d󠁿", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Boston"},
        {"id": 46, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha": "23 de Junio", "hora": "19:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Toronto"},
        {"id": 47, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha": "23 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Houston"},
        {"id": 48, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha": "23 de Junio", "hora": "22:00", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "REP. DEL CONGO", "flag_v": "🇨🇬", "estadio": "Guadalajara"},

        # --- FECHA 3 (Partidos 49 al 72) ---
        {"id": 49, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha": "24 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "🏴\u200d󠁧\u200db\u200ds\u200dc\u200dt\u200d󠁿", "visita": "BRASIL", "flag_v": "🇧🇷", "estadio": "Miami"},
        {"id": 50, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha": "24 de Junio", "hora": "18:00", "local": "MARRUECOS", "flag_l": "🇲🇦", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Atlanta"},
        {"id": 51, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha": "24 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "CANADÁ", "flag_v": "🇨🇦", "estadio": "Vancouver"},
        {"id": 52, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha": "24 de Junio", "hora": "15:00", "local": "BOSNIA Y HERZEG.", "flag_l": "🇧🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Seattle"},
        {"id": 53, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha": "24 de Junio", "hora": "21:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "MÉXICO", "flag_v": "🇲🇽", "estadio": "Ciudad de México"},
        {"id": 54, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha": "24 de Junio", "hora": "21:00", "local": "SUDÁFRICA", "flag_l": "🇿🇦", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Monterrey"},
        {"id": 55, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha": "25 de Junio", "hora": "16:00", "local": "CURAZAO", "flag_l": "🇨🇼", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Filadelfia"},
        {"id": 56, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha": "25 de Junio", "hora": "16:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "ALEMANIA", "flag_v": "🇩🇪", "estadio": "N. York/N. Jersey"},
        {"id": 57, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha": "25 de Junio", "hora": "19:00", "local": "JAPÓN", "flag_l": "🇯🇵", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Dallas"},
        {"id": 58, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha": "25 de Junio", "hora": "19:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "PAÍSES BAJOS", "flag_v": "🇳🇱", "estadio": "Kansas City"},
        {"id": 59, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha": "25 de Junio", "hora": "22:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "ESTADOS UNIDOS", "flag_v": "🇺🇸", "estadio": "Los Angeles"},
        {"id": 60, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha": "25 de Junio", "hora": "22:00", "local": "PARAGUAY", "flag_l": "🇵🇾", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "San Francisco"},
        {"id": 61, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha": "26 de Junio", "hora": "15:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "FRANCIA", "flag_v": "🇫🇷", "estadio": "Boston"},
        {"id": 62, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha": "26 de Junio", "hora": "15:00", "local": "SENEGAL", "flag_l": "🇸🇳", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Toronto"},
        {"id": 63, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha": "26 de Junio", "hora": "23:00", "local": "EGIPTO", "flag_l": "🇪🇬", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Seattle"},
        {"id": 64, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha": "26 de Junio", "hora": "23:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "BÉLGICA", "flag_v": "🇧🇪", "estadio": "Vancouver"},
        {"id": 65, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha": "26 de Junio", "hora": "20:00", "local": "CABO VERDE", "flag_l": "🇨🇻", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Houston"},
        {"id": 66, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha": "26 de Junio", "hora": "20:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "ESPAÑA", "flag_v": "🇪🇸", "estadio": "Guadalajara"},
        {"id": 67, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha": "27 de Junio", "hora": "17:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "INGLATERRA", "flag_v": "🏴\u200djs\u200dc\u200dt\u200d󠁿", "estadio": "N. York/N. Jersey"},
        {"id": 68, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha": "27 de Junio", "hora": "17:00", "local": "CROACIA", "flag_l": "🇭🇷", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Filadelfia"},
        {"id": 69, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha": "27 de Junio", "hora": "22:00", "local": "ARGELIA", "flag_l": "🇩🇿", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Kansas City"},
        {"id": 70, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha": "27 de Junio", "hora": "22:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGENTINA", "flag_v": "🇦🇷", "estadio": "Dallas"},
        {"id": 71, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha": "27 de Junio", "hora": "19:30", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "PORTUGAL", "flag_v": "🇵🇹", "estadio": "Miami"},
        {"id": 72, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha": "27 de Junio", "hora": "19:30", "local": "REP. DEL CONGO", "flag_l": "🇨🇬", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Atlanta"},

        # --- ELIMINACIÓN DIRECTA ---
        {"id": 73, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha": "28 de Junio", "hora": "15:00", "local": "1A", "flag_l": "⚽", "visita": "3C/D/F", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 74, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "13:00", "local": "1B", "flag_l": "⚽", "visita": "3A/C/F", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 75, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "16:30", "local": "1C", "flag_l": "⚽", "visita": "2F", "flag_v": "⚽", "estadio": "Boston"},
        {"id": 76, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha": "29 de Junio", "hora": "21:00", "local": "2A", "flag_l": "⚽", "visita": "2B", "flag_v": "⚽", "estadio": "Monterrey"},
        {"id": 89, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha": "04 de Julio", "hora": "13:00", "local": "GANADOR P73", "flag_l": "🥇", "visita": "GANADOR P74", "flag_v": "🥇", "estadio": "Houston"},
        {"id": 97, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha": "09 de Julio", "hora": "16:00", "local": "GANADOR P89", "flag_l": "🥇", "visita": "GANADOR P90", "flag_v": "🥇", "estadio": "Boston"},
        {"id": 101, "fase_bloque": "Fases Finales", "grupo": "Semifinales", "fecha": "14 de Julio", "hora": "15:00", "local": "GANADOR P97", "flag_l": "🥇", "visita": "GANADOR P98", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 104, "fase_bloque": "Fases Finales", "grupo": "Gran Final", "fecha": "19 de Julio", "hora": "15:00", "local": "GANADOR P101", "flag_l": "🥇", "visita": "GANADOR P102", "flag_v": "🥇", "estadio": "N. York/N. Jersey"}
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

# CONFIGURACIÓN GENERAL DE USUARIOS (Mantenida exactamente como la tienes tú)
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

# ESTILOS ADAPTADOS (Inyección de imágenes locales reales)
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

# LÓGICA DE PERSISTENCIA DE DATOS
def cargar_datos():
    if os.path.exists("datos_polla.json"):
        with open("datos_polla.json", "r") as f: return json.load(f)
    return {"resultados_reales": {}, "pronosticos": {p: {} for p in PARTICIPANTES}}

def guardar_datos(datos_completos):
    with open("datos_polla.json", "w") as f: json.dump(datos_completos, f, indent=4)

datos = cargar_datos()

for p in PARTICIPANTES:
    if p not in datos["pronosticos"]: datos["pronosticos"][p] = {}

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
    if real_l == pred_l and real_v == pred_v:
        return 3, "#22c55e", "🟢 Marcador Exacto (+3 Pts)"
    signo_real = (real_l > real_v) - (real_l < real_v)
    signo_pred = (pred_l > pred_v) - (pred_l < pred_v)
    if signo_real == signo_pred:
        return 1, "#eab308", "🟡 Tendencia Acertada (+1 Pt)"
    return 0, "#ef4444", "🔴 Fallado (0 Pts)"

# ANIMACIÓN DEL BALÓN REAL (balon.png)
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
    
    ⚽ **Inscripción:** $5.000 por cartilla. El 100% va al pozo.
    
    📅 **Plazo de envío:** Hasta 2 horas antes de que empiece cada partido.
    
    💰 **Premios (Al final del Mundial):**
    * 🥇 **1er Lugar:** 50% del pozo acumulado.
    * 🥈 **2do Lugar:** 33,3% del pozo acumulado.
    * 🥉 **3er Lugar:** 16,6% del pozo acumulado.
    
    📊 **Puntuación:**
    * **3 puntos:** Resultado exacto.
    * **1 point:** Acierto a Ganador o Empate (pero no al marcador exacto).
    * **0 puntos:** No acierta nada. *(Válido solo para los 90' reglamentarios)*.
    
    ⚔️ **Desempate (Si hay igualdad de puntos al final):**
    * Gana quien tenga más resultados exactos (de 3 puntos) anotados.
    * Si persiste el empate, el premio del puesto se divide en partes iguales.
    """)

# --- TAB 2: CLASIFICACIÓN ---
with tabs[1]:
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
    st.markdown(f"### 💰 Pozo Acumulado Familiar: **${fondo_total:,.0f}**")
    st.dataframe(df_tabla, use_container_width=True)

# --- TAB 3: REGISTRAR PRONÓSTICOS ---
with tabs[2]:
    st.markdown("## ✍️ ARMA TU JUGADA")
    usuario = st.selectbox("Selecciona tu nombre para apostar:", PARTICIPANTES)
    
    bloque_seleccionado = st.radio(
        "Selecciona la fecha que deseas pronosticar para reducir la lista:",
        ["Fecha 1 (Partidos 1-24)", "Fecha 2 (Partidos 25-48)", "Fecha 3 (Partidos 49-72)", "Fases Finales Eliminatorias"],
        horizontal=True
    )
    
    if "Fecha 1" in bloque_seleccionado: filtro_fase = "Fecha 1"
    elif "Fecha 2" in bloque_seleccionado: filtro_fase = "Fecha 2"
    elif "Fecha 3" in bloque_seleccionado: filtro_fase = "Fecha 3"
    else: filtro_fase = "Fases Finales"
    
    partidos_visibles = [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == filtro_fase]
    
    st.write(f"### 🏟️ Mostrando {len(partidos_visibles)} partidos de: **{bloque_seleccionado}**")
    st.write("---")
    
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
        if ya_jugado: texto_status += " | 🔒 CONGELADA"
        
        st.markdown(f'<div style="background: rgba(15, 23, 42, 0.85); padding: 10px; border-radius: 8px; border-left: 5px solid {color_hex}; margin-top: 10px;"><b>{part["grupo"].upper()} — PARTIDO #{pid}</b> ({part["fecha"]} - {part["hora"]} hrs) | {part["estadio"]} | <span style="color:{color_hex}; font-weight:bold;">{texto_status}</span></div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
        with col1: st.markdown(f"<p style='text-align:right; font-weight:bold;'>{part['local']} {part['flag_l']}</p>", unsafe_allow_html=True)
        with col2: g_l = st.number_input("GL", min_value=0, max_value=15, value=int(pred_actual["l"]), key=f"l_{usuario}_{pid}", disabled=ya_jugado, label_visibility="collapsed")
        with col3: g_v = st.number_input("GV", min_value=0, max_value=15, value=int(pred_actual["v"]), key=f"v_{usuario}_{pid}", disabled=ya_jugado, label_visibility="collapsed")
        with col4: st.markdown(f"<p style='font-weight:bold;'>{part['flag_v']} {part['visita']}</p>", unsafe_allow_html=True)
        
        if not ya_jugado: 
            datos["pronosticos"][usuario][pid] = {"l": g_l, "v": g_v}
            
    st.write("---")
    if st.button("💾 GUARDAR APUESTAS DE ESTA FECHA", use_container_width=True):
        guardar_datos(datos)
        animar_balon_oficial()
        st.success(f"¡Excelente {usuario}, tus pronósticos de la {filtro_fase} fueron guardados correctamente con el balón oficial!")

# --- TAB 4: CRONOGRAMA ---
with tabs[3]:
    st.markdown("## 📅 CRONOGRAMA OFICIAL")
    df_cronograma = pd.DataFrame(FIXTURE_DINAMICO)[["id", "grupo", "fecha", "hora", "local", "visita", "estadio"]]
    st.dataframe(df_cronograma, use_container_width=True, hide_index=True)

# --- TAB 5: PANEL CONTROL ADMINISTRADOR (REPARADO Y BLINDADO) ---
with tabs[4]:
    st.markdown("## ⚙️ PANEL DE CONTROL DE ADMINISTRADOR")
    pass_input = st.text_input("Token de Seguridad Mandamás:", type="password")
    
    if pass_input == PASSWORD_ADMIN:
        st.success("🔓 Acceso Concedido como Mandamás")
        
        fase_admin = st.selectbox("Selecciona Fecha a Cargar en Sistema:", ["Fecha 1", "Fecha 2", "Fecha 3", "Fases Finales"])
        partidos_admin = [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == fase_admin]
        
        st.write("---")
        st.write("### 📝 RELLENAR MARCADORES OFICIALES MUNDIALISTAS")
        
        # Diccionario temporal para acumular los cambios antes del botón definitivo de guardado
        nuevos_cierres = {}
        
        for part in partidos_admin:
            pid = str(part["id"])
            real_actual = datos["resultados_reales"].get(pid, {"l": 0, "v": 0})
            esta_cerrado = pid in datos["resultados_reales"]
            
            st.markdown(f"**Partido #{pid} ({part['grupo']}): {part['local']} vs {part['visita']}**")
            c_al, c_av, c_check = st.columns([2, 2, 3])
            
            with c_al: 
                g_r_l = st.number_input(f"Goles {part['local']}", min_value=0, max_value=15, value=int(real_actual.get("l", 0)), key=f"rl_{pid}", label_visibility="collapsed")
            with c_av: 
                g_r_v = st.number_input(f"Goles {part['visita']}", min_value=0, max_value=15, value=int(real_actual.get("v", 0)), key=f"rv_{pid}", label_visibility="collapsed")
            with c_check:
                finalizado = st.checkbox("¿Cerrar y bloquear apuestas?", key=f"play_{pid}", value=esta_cerrado)
            
            if finalizado:
                nuevos_cierres[pid] = {"l": g_r_l, "v": g_r_v}
                # Lógica dinámica para fases finales si hay empate
                if "Fases Finales" in part["fase_bloque"]:
                    if g_r_l == g_r_v:
                        avanza_eq = st.selectbox(f"🏆 ¿Quién clasifica por penales?", [part['local'], part['visita']], key=f"avanza_{pid}")
                        nuevos_cierres[pid]["avanza"] = avanza_eq
                    else:
                        nuevos_cierres[pid]["avanza"] = part['local'] if g_r_l > g_r_v else part['visita']
            st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
            
        st.write("---")
        # El botón unificado fuera del bucle que previene el bloqueo de Streamlit
        if st.button("🔄 ACTUALIZAR MARCADORES Y CONGELAR PARTIDOS", use_container_width=True):
            # Limpiar los que se desmarcaron y guardar los nuevos cierres reales
            datos["resultados_reales"] = {}
            for k, v in nuevos_cierres.items():
                datos["resultados_reales"][k] = v
                
            guardar_datos(datos)
            st.toast("¡Tablas y llaves recalculadas con éxito para toda la familia!")
            st.rerun()
