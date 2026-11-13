import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import requests
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_data():
    """Obtiene horas, temperatura, humedad y viento de Los Ángeles."""
    try:
        params = {
            "latitude": 34.05,
            "longitude": -118.24,
            "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "timezone": "America/Los_Angeles",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "past_hours": 24,
            "forecast_hours": 1,
        }
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast", params=params, timeout=20
        )
        response.raise_for_status()
        hourly = response.json()["hourly"]

        # Excluye la hora actual y conserva las 24 horas anteriores.
        horas = [datetime.fromisoformat(hora) for hora in hourly["time"][:24]]
        temperaturas = hourly["temperature_2m"][:24]
        humedades = hourly["relative_humidity_2m"][:24]
        vientos = hourly["wind_speed_10m"][:24]
        series = (temperaturas, humedades, vientos)
        if len(horas) != 24 or any(len(serie) != 24 for serie in series):
            raise ValueError("La API no devolvió las 24 horas completas.")
        if any(valor is None for serie in series for valor in serie):
            raise ValueError("La API devolvió valores meteorológicos faltantes.")

        return horas, temperaturas, humedades, vientos
    except (requests.RequestException, KeyError, ValueError, TypeError) as error:
        messagebox.showerror("Error", f"No se pudieron obtener los datos:\n{error}")
        return [], [], [], []


def configurar_eje_horas(ax):
    """Muestra pocas etiquetas de hora para que los ejes sean legibles."""
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel("Hora local de Los Ángeles", fontsize=9)
    ax.tick_params(axis="both", labelsize=9)
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)


def create_line_chart(ax, horas, humedades):
    """Humedad relativa por hora: gráfica de líneas."""
    ax.plot(horas, humedades, color="#2463a6", marker="o", markersize=3)
    ax.set_title("Humedad relativa (líneas)", fontsize=11)
    ax.set_ylabel("Humedad (%)", fontsize=10)
    ax.set_ylim(0, 100)
    configurar_eje_horas(ax)


def create_bar_chart(ax, horas, temperaturas):
    """Temperatura por hora: gráfica de barras."""
    ax.bar(horas, temperaturas, width=0.032, color="#df7135")
    ax.set_title("Temperatura (barras)", fontsize=11)
    ax.set_ylabel("Temperatura (°C)", fontsize=10)
    ax.axhline(0, color="#666666", linewidth=0.7)
    configurar_eje_horas(ax)


def create_scatter_chart(ax, horas, vientos):
    """Velocidad del viento por hora: gráfica de dispersión."""
    ax.scatter(horas, vientos, color="#178569", s=32, alpha=0.85)
    ax.set_title("Velocidad del viento (dispersión)", fontsize=11)
    ax.set_ylabel("Velocidad (km/h)", fontsize=10)
    ax.set_ylim(bottom=0)
    configurar_eje_horas(ax)


def mostrar_graficas(frm, horas, temperaturas, humedades, vientos):
    """Muestra las tres gráficas juntas y reemplaza la carga anterior."""
    anterior = getattr(frm, "_canvas_graficas", None)
    if anterior is not None:
        anterior.get_tk_widget().destroy()
        anterior.figure.clear()

    fig = Figure(figsize=(10, 6), dpi=100, constrained_layout=True)
    distribucion = fig.add_gridspec(2, 2)
    ax_humedad = fig.add_subplot(distribucion[0, 0])
    ax_temperatura = fig.add_subplot(distribucion[0, 1])
    ax_viento = fig.add_subplot(distribucion[1, :])

    create_line_chart(ax_humedad, horas, humedades)
    create_bar_chart(ax_temperatura, horas, temperaturas)
    create_scatter_chart(ax_viento, horas, vientos)

    canvas = FigureCanvasTkAgg(fig, master=frm)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()
    frm._canvas_graficas = canvas


def open_win_canvas(parent: tk.Tk):
    """Abre la ventana de clima sin modificar las otras ventanas."""
    win = tk.Toplevel(parent)
    win.title("Clima de Los Ángeles - tres gráficas")
    ancho = min(1100, parent.winfo_screenwidth() - 80)
    alto = min(820, parent.winfo_screenheight() - 100)
    win.geometry(f"{ancho}x{alto}")
    win.minsize(min(800, ancho), min(600, alto))

    frm = ttk.Frame(win, padding=12)
    frm.pack(fill="both", expand=True)
    ttk.Label(
        frm, text="Los Ángeles | últimas 24 horas", font=("Segoe UI", 14, "bold")
    ).pack(pady=(0, 4))
    controles = ttk.Frame(frm)
    controles.pack(fill="x", pady=(0, 4))
    periodo = tk.StringVar(value="Pulsa el botón para consultar Open-Meteo.")
    ttk.Label(frm, textvariable=periodo, font=("Segoe UI", 9)).pack(pady=(0, 4))
    graficas = ttk.Frame(frm)
    graficas.pack(fill="both", expand=True)

    def cargar():
        horas, temperaturas, humedades, vientos = fetch_data()
        if horas and temperaturas and humedades and vientos:
            mostrar_graficas(graficas, horas, temperaturas, humedades, vientos)
            periodo.set(
                f"{horas[0]:%d/%m/%Y %H:%M} a {horas[-1]:%d/%m/%Y %H:%M}"
                " | hora local de Los Ángeles"
            )

    ttk.Button(
        controles, text="Cargar y mostrar gráficas", command=cargar
    ).pack()
    return win


# Para pruebas independientes (opcional)
#if __name__ == "__main__":
#    root = tk.Tk()
#    root.title("Prueba win_canvas")
#    ttk.Button(root, text="Abrir ventana Canvas", command=lambda: open_win_canvas(root)).pack(pady=20)
#    root.mainloop()