"""Inicio de LlegaBien con la imagen local y dos acciones de clic."""

from math import ceil
from pathlib import Path
import base64
import tkinter as tk
from tkinter import messagebox


def open_win_home(parent: tk.Tk):
    ruta = Path(__file__).resolve().with_name("inicio_llegabien.png")

    try:
        # Carga los datos completos del PNG en lugar de abrirlo desde Tcl/Tk.
        datos = base64.b64encode(ruta.read_bytes()).decode("ascii")
        original = tk.PhotoImage(master=parent, data=datos, format="png")
        if (original.width(), original.height()) != (1448, 1086):
            # Respaldo para entornos que sustituyen archivos de imagen por iconos.
            datos = ruta.with_suffix(".b64").read_text(encoding="ascii").strip()
            original = tk.PhotoImage(master=parent, data=datos, format="png")
    except (OSError, UnicodeError, tk.TclError) as error:
        parent.deiconify()
        messagebox.showerror(
            "No se pudo abrir el fondo",
            f"Coloca inicio_llegabien.png junto a win_home.py.\n\n"
            f"Ruta: {ruta}\n\n{error}",
            parent=parent,
        )
        return

    ancho_original, alto_original = original.width(), original.height()
    if (ancho_original, alto_original) != (1448, 1086):
        parent.deiconify()
        messagebox.showerror(
            "Imagen de fondo incorrecta",
            "Usa la pantalla completa 'Cada llegada cuenta' "
            "de 1448 × 1086 píxeles.",
            parent=parent,
        )
        return

    # Retira la barra de ventana dibujada; Tkinter ya tiene una real.
    recorte = 42
    fondo = tk.PhotoImage(master=parent)
    fondo.tk.call(
        str(fondo), "copy", str(original),
        "-from", 0, recorte, ancho_original, alto_original,
    )

    limite_ancho = max(1, min(1100, parent.winfo_screenwidth() - 80))
    limite_alto = max(1, parent.winfo_screenheight() - 140)
    factor = max(1, ceil(max(
        ancho_original / limite_ancho,
        (alto_original - recorte) / limite_alto,
    )))
    fondo = fondo.subsample(factor, factor)

    win = tk.Toplevel(parent)
    win.title("LlegaBien — Inicio")
    win.geometry(f"{fondo.width()}x{fondo.height()}")
    win.resizable(False, False)

    canvas = tk.Canvas(win, bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.fondo = fondo
    canvas.create_image(0, 0, image=fondo, anchor="nw")

    def volver_menu():
        win.destroy()
        parent.deiconify()
        parent.lift()
        parent.focus_set()

    def mostrar_importancia():
        messagebox.showinfo(
            "¿Por qué importa?",
            "Los traslados difíciles pueden relacionarse con retardos "
            "y rotación de personal.\n\n"
            "LlegaBien ayuda a identificar traslados de riesgo, colonias "
            "prioritarias y el costo estimado de la rotación asociada "
            "al traslado.\n\n"
            "Referencias incluidas en el documento del proyecto:\n"
            "• 47 % de los empleadores reconoce el traslado como causa "
            "de renuncia (OCC Mundial et al., 2023).\n"
            "• $47,000 de costo promedio por salida "
            "(Publimetro, 2022).\n\n"
            "Son datos de referencia, no resultados de tu empresa.",
            parent=win,
        )

    def zona(event):
        x = event.x * factor
        y = event.y * factor + recorte
        if 46 <= x <= 415 and 973 <= y <= 1044:
            return "importancia"
        if 438 <= x <= 725 and 973 <= y <= 1044:
            return "menu"
        return None

    def hacer_clic(event):
        boton = zona(event)
        if boton == "importancia":
            mostrar_importancia()
        elif boton == "menu":
            volver_menu()

    canvas.bind("<Button-1>", hacer_clic)
    canvas.bind(
        "<Motion>",
        lambda event: canvas.configure(cursor="hand2" if zona(event) else ""),
    )
    win.bind("<Escape>", lambda event: volver_menu())
    win.protocol("WM_DELETE_WINDOW", volver_menu)

    parent.withdraw()
    win.focus_set()
    return win
