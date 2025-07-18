import os
from PIL import Image, ImageDraw, ImageFont

print("Comienzo de la app")
# CONFIGURACIÓN DEL CARTEL
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

# EMOJIS PNG (ajusta el path según tu estructura)
emoji_sol = Image.open("emojis/sol.png").convert("RGBA").resize((65, 65))
emoji_palmera = Image.open("emojis/palmera.png").convert("RGBA").resize((40, 50))
emoji_tijeras = Image.open("emojis/tijeras.png").convert("RGBA").resize((40, 50))
emoji_phone = Image.open("emojis/phone.png").convert("RGBA").resize((55, 55)) 

# TEXTOS
texto1 = "¡¡NOS VAMOS DE VACACIONES!!"
texto2 = "Estaremos cerrados del 22 al 26 de julio"
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

# TÍTULO CON EMOJIS (🌞 texto ✂️ 🌴)
x_texto, texto1_width = centrar_texto(draw, texto1, fuente_negrita, y + 40, "black")
emoji_y = y  # alineación vertical

# Sol a la izquierda
imagen.paste(emoji_sol, (x_texto - 80, emoji_y + 40), emoji_sol)
# Tijeras a la derecha
imagen.paste(emoji_tijeras, (x_texto + texto1_width + 10, emoji_y + 40), emoji_tijeras)
# Palmera más a la derecha
imagen.paste(emoji_palmera, (x_texto + texto1_width + 50, emoji_y + 40), emoji_palmera)

# Líneas de texto
centrar_texto(draw, texto2, fuente_normal, y + espacio + 130, "black")
centrar_texto(draw, texto3, fuente_normal, y + 2 * espacio +230, "black")

# Teléfono con emoji 📞
x_tel, _ = centrar_texto(draw, telefono, fuente_telefono, y + 3 * espacio + 230, "blue")
imagen.paste(emoji_phone, (x_tel - 65, y + 3 * espacio + 230 + 10), emoji_phone)

# Línea final
centrar_texto(draw, texto4, fuente_normal, y + 4 * espacio+ 330, "black")

# GUARDAR
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(downloads_dir, exist_ok=True)
output_path = os.path.join(downloads_dir, "cartel_redes.jpg")
imagen.convert("RGB").save(output_path, "JPEG")

print(f"✅ Cartel generado correctamente en:\n{output_path}")
