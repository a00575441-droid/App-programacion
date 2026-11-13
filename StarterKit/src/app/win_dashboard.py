import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from src.core.data_io import cargar_csv
from src.core.logic import resumir_registros

def open_win_dashboard(parent: tk.Tk):
    win=tk.Toplevel(parent); win.title("Dashboard base"); win.geometry("560x340")
    frm=ttk.Frame(win,padding=18); frm.pack(fill="both",expand=True)
    datos=cargar_csv(ROOT/"data"/"sample_traffic.csv")
    resumen=resumir_registros(datos)
    ttk.Label(frm,text="Dashboard base",font=("Segoe UI",14,"bold")).pack(anchor="w")
    for k,v in resumen.items(): ttk.Label(frm,text=f"{k.replace('_',' ').title()}: {v}").pack(anchor="w",pady=4)
    ttk.Label(frm,text="En el Technology Booster reemplazarás esta vista por una gráfica Matplotlib y análisis con Pandas.",wraplength=500).pack(anchor="w",pady=18)
