# -*- coding: utf-8 -*-
"""08 (AVANZADO) - Automatizar HEC-RAS por COM.
Requisitos: Windows + HEC-RAS + pip install pywin32.
ProgID orientativo por version: HEC-RAS 6.x/7.x puede variar segun instalacion.
"""
from pathlib import Path
import win32com.client as com

BASE = Path(r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA")
if not BASE.exists():
    BASE = Path(__file__).resolve().parents[1]
PROYECTO = str(BASE / r"03_HEC_RAS\Proyecto_HEC_RAS\BahiaBlanca_2025.prj")
PROGID   = "RAS70.HECRASController"  # ajustar si la version instalada usa otro ProgID

ras = com.Dispatch(PROGID)
ras.Project_Open(PROYECTO)
ras.ShowRas()
count, names, ids = ras.Plan_Names(None, None, True)
print("Planes en el proyecto:", names)
# ok, mensajes = ras.Compute_CurrentPlan(None, None, True)  # descomentar para correr el plan actual
# print("Compute OK:", ok, mensajes)
# ras.QuitRas()
