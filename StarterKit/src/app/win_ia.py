"""Ventana Tkinter que consulta una IA mediante OpenRouter."""

import queue
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import requests

URL = "https://openrouter.ai/api/v1/chat/completions"
MODELO = "nvidia/nemotron-3.5-lightning:free"


def open_win_ia(parent):
    """Abre una ventana para enviar preguntas y visualizar respuestas."""
    win = tk.Toplevel(parent)
    win.title("Mi primera aplicación con IA")
    win.geometry("650x560")
    win.minsize(600, 500)

    frm = ttk.Frame(win, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="API Key de OpenRouter:").pack(anchor="w")
    campo_clave = ttk.Entry(frm, show="*")
    campo_clave.pack(fill="x", pady=(4, 12))

    ttk.Label(frm, text="Escribe tu pregunta:").pack(anchor="w")
    campo_pregunta = ScrolledText(frm, height=4, wrap="word")
    campo_pregunta.pack(fill="x", pady=(4, 12))

    ttk.Label(frm, text="Respuesta de la IA:").pack(anchor="w")
    campo_respuesta = ScrolledText(frm, height=12, wrap="word", state="disabled")
    campo_respuesta.pack(fill="both", expand=True, pady=(4, 8))

    estado = ttk.Label(frm, text="Listo para preguntar")
    estado.pack(anchor="w")
    resultados = queue.Queue()
    sondeo = None

    def mostrar_texto(texto):
        campo_respuesta.config(state="normal")
        campo_respuesta.delete("1.0", "end")
        campo_respuesta.insert("end", texto)
        campo_respuesta.config(state="disabled")

    def consultar(api_key, pregunta):
        """Ejecuta la petición HTTP fuera del hilo de la interfaz."""
        try:
            respuesta = requests.post(
                URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODELO,
                    "messages": [{"role": "user", "content": pregunta}],
                    "max_tokens": 1000,
                },
                timeout=120,
            )
            respuesta.raise_for_status()
            datos = respuesta.json()
            texto = datos["choices"][0]["message"]["content"]
            if texto is not None and not isinstance(texto, str):
                raise ValueError("El contenido debe ser texto.")
            resultados.put(("ok", texto or "(El modelo no devolvió texto)"))
        except requests.exceptions.Timeout:
            resultados.put(("error", "Se agotó el tiempo de espera."))
        except requests.exceptions.HTTPError as error:
            codigo = error.response.status_code if error.response is not None else "desconocido"
            resultados.put(("error", f"OpenRouter devolvió HTTP {codigo}."))
        except (ValueError, KeyError, IndexError, TypeError):
            resultados.put(("error", "La respuesta de la API no tiene el formato esperado."))
        except requests.exceptions.RequestException:
            resultados.put(("error", "No se pudo conectar con OpenRouter."))

    def revisar_respuesta():
        """Actualiza los widgets desde el hilo principal de Tkinter."""
        nonlocal sondeo
        sondeo = None
        if not win.winfo_exists():
            return
        try:
            tipo, texto = resultados.get_nowait()
        except queue.Empty:
            sondeo = win.after(150, revisar_respuesta)
            return

        mostrar_texto(texto)
        estado.config(text="Consulta terminada" if tipo == "ok" else "Ocurrió un error")
        boton.config(state="normal")

    def enviar():
        api_key = campo_clave.get().strip()
        pregunta = campo_pregunta.get("1.0", "end").strip()
        if not api_key or not pregunta:
            estado.config(text="Escribe tu API Key y una pregunta.")
            return

        boton.config(state="disabled")
        estado.config(text="Consultando a la IA...")
        mostrar_texto("")
        threading.Thread(target=consultar, args=(api_key, pregunta), daemon=True).start()
        revisar_respuesta()

    def cerrar():
        nonlocal sondeo
        if sondeo is not None:
            win.after_cancel(sondeo)
            sondeo = None
        campo_clave.delete(0, "end")
        win.destroy()

    boton = ttk.Button(frm, text="Preguntar a la IA", command=enviar)
    boton.pack(pady=8)
    win.protocol("WM_DELETE_WINDOW", cerrar)
    return win
