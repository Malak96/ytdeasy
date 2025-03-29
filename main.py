import subprocess
import json
from textual.events import Focus
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical, Grid, ItemGrid
from textual.screen import Screen, ModalScreen
from textual.theme import BUILTIN_THEMES
from textual.widgets import (
    Select, Label, Input, Button, TabbedContent, LoadingIndicator, ListItem,ListView
)

formats = [("mp4 (Video)", "mp4"),
           ("webm (Video)", "webm"),
           ("mkv (Video)", "mkv"),
           ("mp3 (Audio)", "mp3"),
           ("m4a (Audio)", "m4a"),
           ("opus (Audio)", "opus")]

class DownloadOptions(Screen):
    CSS_PATH = "assents.css"
    def __init__(self, a_table=None, v_table=None, title="", formats=None):
        super().__init__()
        self.id_a = ""
        self.id_v = ""
        self.a_table = a_table or []
        self.v_table = v_table or []
        self.formats = formats or []
        self.title = title

    def compose(self) -> ComposeResult:
        self.app.theme = "nord"

        with TabbedContent("Inicio", "Configuraciones", id="tab_c", disabled=False):
            with VerticalScroll(classes="center_all"):
                with ItemGrid(min_column_width=1,regular=True,classes="center_all"):
                    yield Input(placeholder="Click derecho para pegar", id="url_input",value="https://www.youtube.com/watch?v=3VZFpwlXKpg")
                    yield Button("Verificar URL", id="analizar_btn")
                yield Select(self.a_table, prompt="Selecciona el audio", classes="Select", id="select_audio")
                yield Select(self.v_table, prompt="Selecciona el video", classes="Select", id="select_video")
                yield Select(formats, prompt="Formato de Salida", classes="Select", id="output_format")
                yield Label("Título: ", id="title_label")
                yield Label("Audio ID: ", id="a-seleccion_label")
                yield Label("Video ID: ", id="v-seleccion_label")
                with Horizontal(classes="cont_btn_op"):
                    yield Button("Descargar")
                    yield Button("Salir", id="salir_btn",variant="error")
            with Vertical():
                theme_name = []
                for themes in BUILTIN_THEMES:
                    theme_name.append((themes,themes))
                yield Select(theme_name, prompt="Selecciona un tema", classes="Select", id="theme_select")
                yield Button("Aplicar", id="apply_theme")

    def receive_data(self, a_table, v_table, title, formats):
        """Recibe los datos de Verfy_URL y actualiza la pantalla."""
        self.a_table = a_table
        self.v_table = v_table
        self.title = title
        self.formats = formats
        self.update_display()

    def update_display(self):
        """Actualizar la interfaz con los nuevos datos."""
        self.query_one("#select_audio", Select).set_options(self.a_table)
        self.query_one("#select_video", Select).set_options(self.v_table)
        self.query_one("#title_label", Label).update(f"Título: {self.title}")
        
        self.notify("URL verificada correctamente.",timeout=2)

    @on(Button.Pressed, "#analizar_btn")
    def analizar_url(self, event: Button.Pressed) -> None:
        """Acción cuando se presiona el botón 'Analizar'."""
        url = self.query_one("#url_input", Input).value
        if url:
            self.app.push_screen(Verfy_URL(url, previous_screen=self))  # Ir a la siguiente pantalla
        else:
            self.notify("No se ha ingresado una URL",severity="warning")

    @on(Button.Pressed, "#apply_theme")
    def apply_theme(self, event: Button.Pressed) -> None:
        """Aplicar tema seleccionado"""
        theme = self.query_one("#theme_select", Select).value
        self.app.theme = theme
        self.notify(f"Tema aplicado: {theme}")
        
    @on(Button.Pressed, "#salir_btn")
    def cancelar(self, event: Button.Pressed) -> None:
        """Volver a la pantalla de inicio"""
        self.app.push_screen(QuitScreen())
    @on(Select.Changed, "#select_audio")
    def audio_selected(self, event: Select.Changed) -> None:
        """Actualizar ID de audio"""
        self.id_a = event.value if event.value != Select.BLANK else ""
        item_select = next((f for f in self.formats if f["format_id"] == self.id_a), None)
        if self.id_a:
            self.query_one("#a-seleccion_label",Label).update(f"Audio ID: {item_select["format_id"]} Canales: {item_select["audio_channels"]}")
            


    @on(Select.Changed, "#select_video")
    def video_selected(self, event: Select.Changed) -> None:
        """Actualizar ID de video"""
        self.id_v = event.value if event.value != Select.BLANK else ""
        item_select = next((f for f in self.formats if f["format_id"] == self.id_v), None)
        if self.id_v:
            #self.query_one("#a-seleccion_label", Label).update(f"Resolucion: {format[0]['resolution']}")
            self.query_one("#v-seleccion_label", Label).update(f"Video ID: {item_select["format_id"]} Resolucion: {item_select['resolution']} Tamaño: {filesize(item_select)}")
        #self.query_one("#resolution_label", Label).update(f"Resolucion: {values_for_key}")

    @on(Select.Changed, "#output_format")
    def output_format(self, event: Select.Changed) -> None:
        """Habilitar o deshabilitar selección de video según formato"""
        selectes = str(event.value)
        self.query_one("#select_video", Select).disabled = selectes in ["m4a", "mp3", "opus"]
        self.notify(f"Formato seleccionado: {selectes}")

class Verfy_URL(ModalScreen):
    
    def __init__(self, url="", previous_screen=None):
        super().__init__()
        self.url = url
        self.previous_screen = previous_screen # Pantalla anterior
        self.a_tuple = []
        self.v_tuple = []
        self.formats = []
        self.title = ""

    def compose(self) -> ComposeResult:
            yield Grid(
                LoadingIndicator(),
                Label("Verificando URL espera...", id="question"),
                id="Verfy_URL",
            )
         
    def on_mount(self) -> None:
        """Ejecutar al montar la pantalla."""
        #self.a_tuple, self.v_tuple = ytpy.filter_json(self.url,exc)  # Procesar URL   
        self.run_worker(self.verify_url,exclusive=True,thread=True)  # Ejecutar en segundo plano


    def verify_url(self):
        """Ejecuta la verificación de la URL en segundo plano."""
        self.a_tuple, self.v_tuple,self.title,self.formats = filter_json(self.url)  # Procesa la URL
        # Cuando termine, pasa los datos a DownloadOptions en el hilo principal
        if self.previous_screen:
            self.previous_screen.receive_data(self.a_tuple, self.v_tuple,self.title,self.formats)
        self.app.pop_screen()

class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("¿Estás seguro de que quieres salir?", id="question"),
            Button("Salir", variant="error", id="quit", classes="quit_btn"),
            Button("Cancelar", variant="primary", id="cancel", classes="quit_btn"),
            id="dialog",
        )
           
    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

class MyApp(App):

    def on_mount(self) -> None:
        self.push_screen(DownloadOptions([],[]))  # Instanciar correctamente

def read_link (url):
    
    #command = ["yt-dlp.exe", "--no-warnings","--no-playlist", "--cookies","cookies.txt", "-q", "-j", url]
    command = ["C://yt-dlp.exe", "--no-warnings","--no-playlist", "-q", "-j", url]
    salida = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        resultado_json = json.loads(salida.stdout)
    except json.JSONDecodeError:
        print("Error al decodificar el JSON.")
        return []

    formatos_filtrados = [
        {
            "format_id": f.get("format_id", None),
            "ext": f.get("ext", None),
            "resolution": f.get("resolution", None),
            "filesize": f.get("filesize", None),
            "fps": f.get("fps", None),
            "vcodec": f.get("vcodec", None),
            "acodec": f.get("acodec", None),
            "format_note": f.get("format_note",None),
            "vbr": f.get("vbr",None),
            "abr": f.get("abr",None),
            "audio_channels": f.get("audio_channels",None)
        }
        for f in resultado_json.get('formats', [])
    ]
    title = resultado_json.get("title", None)
    return formatos_filtrados, title
    
def filesize(format):
    if format["filesize"] is not None:
            try:
                size=["B","KB","MB","GB","?"]
                count_size=0
                filesize_kb = format['filesize']
                while True:
                    if filesize_kb >= 1024:
                        count_size=count_size+1
                        filesize_kb = int(filesize_kb) / 1024
                    else:
                        break
                if count_size < 5: 
                    filesize_kb = f"{filesize_kb:.2f}{size[count_size]}"
                else: 
                    filesize_kb = f"{filesize_kb:.2f}{size[4]}"
            except (ValueError, TypeError):
                filesize_kb = None
    else:
            filesize_kb = None
    return filesize_kb 
def filter_json(url):
    a_table=[]
    v_table=[]
    formatos, title = read_link(url)
    if not formatos:
        print("No se encontraron formatos disponibles.")
        return
    
    for f in formatos:
        
        vcodec = f.get("vcodec", None)
        try:
            if vcodec != None:
                if vcodec=="none"or vcodec=="None":vcodec=None
                if "avc" in vcodec: vcodec = f"{vcodec}(x264)"
        except(ValueError,TypeError):
            vcodec = None
            
        try:
            acodec = (f["acodec"])
            if acodec == "None" or acodec == "none": acodec=None
        except(ValueError,TypeError):
            acodec = None
            
        try:
            fps = str(f["fps"]) + "FPS"
            if fps == "None" or fps == "none": fps=None
            
        except(ValueError,TypeError):
            fps = None

        if vcodec is None and acodec is not None:
            a_table.append((
                f"{f['ext']}|{str(f['abr'])}kbps|{acodec}|{f['format_note']}",
                f["format_id"]
            ))

        elif vcodec is not None:
            v_table.append(( 
                f"{f['ext']}|{f['resolution']}|{fps}|{str(f['vbr'])}kbps|{vcodec}|{f['format_note']}",
                f["format_id"]
            ))

    return a_table, v_table, title , formatos


if __name__ == "__main__":
    app = MyApp()
    app.run()