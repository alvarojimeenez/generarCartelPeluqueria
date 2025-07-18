import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont

# ========= VENTANA DE ENTRADA PERSONALIZADA =========
class EntradaTexto:
    def __init__(self):
        self.resultado = None
        self.root = tk.Tk()
        self.root.title("Generador de Carteles")
        self.root.geometry("550x220")
        self.root.resizable(False, False)

        # Título visual
        titulo = tk.Label(self.root, text="Generador de Carteles", font=("Arial", 20, "bold"))
        titulo.pack(pady=10)

        # Etiqueta + campo
        label = tk.Label(self.root, text="¿Qué mensaje quieres poner debajo del título?\n(ej: Estaremos cerrados del dd al dd de mm):")
        label.pack()

        self.entry = tk.Entry(self.root, width=60)
        self.entry.pack(pady=5)

        # Botones
        botones = tk.Frame(self.root)
        botones.pack(pady=10)

        aceptar = tk.Button(botones, text="Aceptar", command=self.aceptar)
        aceptar.pack(side=tk.LEFT, padx=10)

        cancelar = tk.Button(botones, text="Cancelar", command=self.root.destroy)
        cancelar.pack(side=tk.LEFT, padx=10)

        self.root.mainloop()

    def aceptar(self):
        texto = self.entry.get()
        if texto.strip() == "":
            messagebox.showerror("Error", "Debes escribir un mensaje para continuar.")
        else:
            self.resultado = texto
            self.root.destroy()

# ========= OBTENER TEXTO DINÁMICO =========
entrada = EntradaTexto()
texto2 = entrada.resultado

if texto2 is None:
    exit()

# ========= CONFIGURACIÓN DEL CARTEL =========
print("Comienzo de la app")

ancho, alto = 1080, 1346
fondo_color = (180, 180, 180)  # gris claro
imagen = Image.new("RGB", (ancho, alto), color=fondo_color)
draw = ImageDraw.Draw(imagen)

# CARGAR Y ESCALAR LOGO
logo = Image.open("imagen_logo/logo.jpg").convert("RGBA")
max_ancho = 700
max_alto = 340
logo.thumbnail((max_ancho, max_alto), resample=Image.LANCZOS)
pos_logo = ((ancho - logo.width) // 2, 100)
imagen.paste(logo, pos_logo, logo)

# LÍNEAS DECORATIVAS
linea_superior_y = pos_logo[1] - 30
linea_inferior_y = pos_logo[1] + logo.height + 30
draw.line([(0, linea_superior_y), (ancho - 200, linea_superior_y)], fill="black", width=4)
draw.line([(200, linea_inferior_y), (ancho, linea_inferior_y)], fill="black", width=4)

# FUENTES
fuente_negrita = ImageFont.truetype("arialbd.ttf", 45)
fuente_normal = ImageFont.truetype("arial.ttf", 54)
fuente_telefono = ImageFont.truetype("arialbd.ttf", 65)

# EMOJIS PNG
emoji_sol = Image.open("emojis/sol.png").convert("RGBA").resize((65, 65))
emoji_palmera = Image.open("emojis/palmera.png").convert("RGBA").resize((40, 50))
emoji_tijeras = Image.open("emojis/tijeras.png").convert("RGBA").resize((40, 50))
emoji_phone = Image.open("emojis/phone.png").convert("RGBA").resize((55, 55)) 

# TEXTOS FIJOS
texto1 = "¡¡NOS VAMOS DE VACACIONES!!"
texto3 = "Para cualquier duda, contactad al"
telefono = "(621181640)"
texto4 = "¡Nos vemos a la vuelta!"

# CENTRADO DE TEXTO
def centrar_texto(draw, texto, fuente, y, color):
    bbox = fuente.getbbox(texto)
    text_width = bbox[2] - bbox[0]
    x = (ancho - text_width) // 2
    draw.text((x, y), texto, font=fuente, fill=color)
    return x, text_width

# POSICIONES BASE
y = linea_inferior_y + 40
espacio = 100

# TÍTULO CON EMOJIS
x_texto, texto1_width = centrar_texto(draw, texto1, fuente_negrita, y + 40, "black")
emoji_y = y

imagen.paste(emoji_sol, (x_texto - 80, emoji_y + 40), emoji_sol)
imagen.paste(emoji_tijeras, (x_texto + texto1_width + 10, emoji_y + 40), emoji_tijeras)
imagen.paste(emoji_palmera, (x_texto + texto1_width + 50, emoji_y + 40), emoji_palmera)

# TEXTOS
centrar_texto(draw, texto2, fuente_normal, y + espacio + 130, "black")
centrar_texto(draw, texto3, fuente_normal, y + 2 * espacio + 230, "black")
x_tel, _ = centrar_texto(draw, telefono, fuente_telefono, y + 3 * espacio + 230, "blue")
imagen.paste(emoji_phone, (x_tel - 65, y + 3 * espacio + 230 + 10), emoji_phone)
centrar_texto(draw, texto4, fuente_normal, y + 4 * espacio + 330, "black")

# GUARDAR IMAGEN
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(downloads_dir, exist_ok=True)
output_path = os.path.join(downloads_dir, "cartel_redes.jpg")
imagen.convert("RGB").save(output_path, "JPEG")

print(f"✅ Cartel generado correctamente en:\n{output_path}")
