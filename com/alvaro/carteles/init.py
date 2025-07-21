import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

from PIL import Image, ImageDraw, ImageFont

# Función para manejar rutas en PyInstaller o Buildozer (Android)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def generar_cartel(texto_dinamico):
    ancho, alto = 1080, 1346
    fondo_color = (180, 180, 180)  # gris claro
    imagen = Image.new("RGB", (ancho, alto), color=fondo_color)
    draw = ImageDraw.Draw(imagen)

    # CARGAR Y ESCALAR LOGO
    logo_path = resource_path("imagen_logo/logo.jpg")
    logo = Image.open(logo_path).convert("RGBA")
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

    # FUENTES (en Android hay que asegurarse que las fuentes estén disponibles o usar otras)
    fuente_negrita = ImageFont.truetype(resource_path("arialbd.ttf"), 45)
    fuente_normal = ImageFont.truetype(resource_path("arial.ttf"), 54)
    fuente_telefono = ImageFont.truetype(resource_path("arialbd.ttf"), 65)

    # EMOJIS PNG
    emoji_sol = Image.open(resource_path("emojis/sol.png")).convert("RGBA").resize((65, 65))
    emoji_palmera = Image.open(resource_path("emojis/palmera.png")).convert("RGBA").resize((40, 50))
    emoji_tijeras = Image.open(resource_path("emojis/tijeras.png")).convert("RGBA").resize((40, 50))
    emoji_phone = Image.open(resource_path("emojis/phone.png")).convert("RGBA").resize((55, 55))

    # TEXTOS FIJOS
    texto1 = "¡¡NOS VAMOS DE VACACIONES!!"
    texto3 = "Disculpen las molestias"
    ##telefono = "(621181640)"
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
    centrar_texto(draw, texto_dinamico, fuente_normal, y + espacio + 130, "black")
    centrar_texto(draw, texto3, fuente_normal, y + 2 * espacio + 230, "black")
    ##x_tel, _ = centrar_texto(draw, telefono, fuente_telefono, y + 3 * espacio + 230, "blue")
    ##imagen.paste(emoji_phone, (x_tel - 65, y + 3 * espacio + 230 + 10), emoji_phone)
    centrar_texto(draw, texto4, fuente_normal, y + 4 * espacio + 330, "black")

    # Guardar imagen en ruta accesible (en Android podría ser diferente)
    try:
        from android.storage import primary_external_storage_path
        downloads_dir = os.path.join(primary_external_storage_path(), "Download")
    except ImportError:
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    os.makedirs(downloads_dir, exist_ok=True)
    output_path = os.path.join(downloads_dir, "cartel_redes.jpg")
    imagen.convert("RGB").save(output_path, "JPEG")

    return output_path

class GeneradorCarteles(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(text="Generador de Carteles", font_size=24, bold=True))
        self.add_widget(Label(text="¿Qué mensaje quieres poner debajo del título?"))

        self.text_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.text_input)

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_aceptar = Button(text="Generar")
        btn_cancelar = Button(text="Cancelar")
        btn_aceptar.bind(on_press=self.aceptar)
        btn_cancelar.bind(on_press=self.cancelar)

        btn_layout.add_widget(btn_aceptar)
        btn_layout.add_widget(btn_cancelar)

        self.add_widget(btn_layout)

    def aceptar(self, instance):
        texto = self.text_input.text.strip()
        if not texto:
            popup = Popup(title="Error",
                          content=Label(text="Debes escribir un mensaje para continuar."),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
            return

        # Generar cartel con el texto
        try:
            ruta_imagen = generar_cartel(texto)
            popup = Popup(title="Éxito",
                          content=Label(text=f"Cartel generado en:\n{ruta_imagen}"),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            
        except Exception as e:
            popup = Popup(title="Error",
                          content=Label(text=f"Error generando cartel:\n{e}"),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        
    def cancelar(self, instance):
        App.get_running_app().stop()

class CartelApp(App):
    def build(self):
        # Opcional: tamaño ventana en PC para pruebas
        Window.size = (400, 300)
        return GeneradorCarteles()

if __name__ == "__main__":
    CartelApp().run()
