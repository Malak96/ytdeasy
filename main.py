import ytpy
from textual.events import Focus
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical, Grid, ItemGrid
from textual.screen import Screen, ModalScreen
from textual.theme import BUILTIN_THEMES
from textual.widgets import (
    Select, Label, Input, Button, TabbedContent, LoadingIndicator
)

formats = [("mp4 (Video)", "mp4"),
           ("webm (Video)", "webm"),
           ("mkv (Video)", "mkv"),
           ("mp3 (Audio)", "mp3"),
           ("m4a (Audio)", "m4a"),
           ("opus (Audio)", "opus")]
# class InputUrl(Screen):
#     def compose(self) -> ComposeResult:
        
#         with Container(classes="center_all"):
#             with Grid(classes="center_all"):
#                 yield Input(placeholder="Pega una URL", id="url_input",value="https://www.youtube.com/watch?v=CsrmS0id6So")
#                 yield Button("🔎", id="analizar_btn", classes="center_all")
#                 yield Button("Salir", id="salir_btn")
#     @on(Button.Pressed, "#salir_btn")
#     def salir(self, event: Button.Pressed) -> None:
#         """Mostrar pantalla de confirmación para salir."""      
#         self.app.push_screen(QuitScreen()) 

#     @on(Button.Pressed, "#analizar_btn")
#     def analizar_url(self, event: Button.Pressed) -> None:
#         """Acción cuando se presiona el botón 'Analizar'."""
#         url = self.query_one("#url_input", Input).value
#         a_table , v_table =  ytpy.filter_json(url)
#         #resultado = f"URL: {url}\nFormatos actualizados."
#         #self.query_one("#resultado_label", Label).update(resultado)
#         a_table = [("Audio 1", "1"), ("Audio 2", "2"), ("Audio 3", "3")]
#         v_table = [("Video 1", "1"), ("Video 2", "2"), ("Video 3", "3")]
#         if url:
#             self.app.push_screen(DownloadOptions(a_table, v_table))

class DownloadOptions(Screen):
    CSS_PATH = "assents.css"
    def __init__(self, a_table=None, v_table=None, title="", formats=None):
        super().__init__()
        self.id_a = ""
        self.id_v = ""
        self.a_table = a_table or []
        self.v_table = v_table or []
        self.formats = formats or []
        title = title
        

    def compose(self) -> ComposeResult:
        self.app.theme = "monokai"
        #with VerticalScroll():
        with TabbedContent("Inicio","Descargas", "Configuraciones", id="tab_c", classes="tab_align", disabled=False):
            with VerticalScroll():
                #with ItemGrid(min_column_width=1,regular=True):
                with ItemGrid(min_column_width=1,regular=True,classes="center_all"):
                    yield Input(placeholder="Click derecho para pegar", id="url_input",value="https://www.youtube.com/watch?v=CsrmS0id6So")
                    #yield Button("", id="paste_btn")
                    yield Button("Verificar URL", id="analizar_btn")
                
                yield Label(id="resultado_label")
                yield Select(self.a_table, prompt="Selecciona el audio", classes="Select", id="select_audio")
                yield Select(self.v_table, prompt="Selecciona el video", classes="Select", id="select_video")
                yield Select(formats, prompt="Formato de Salida", classes="Select", id="output_format")
                yield Label("Título: ", id="title_label")
                yield Label("Audio ID: ", id="a-seleccion_label")
                yield Label("Video ID: ", id="v-seleccion_label")
                yield Label("Resolucion: ", id="resolution_label")
                with Horizontal(classes="cont_btn_op"):
                    yield Button("Descargar")
                    yield Button("Salir", id="salir_btn",variant="error")
            yield Label("Descargas", id="descargas")
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

    @on(Focus)
    async def on_focus(self, event: Focus) -> None:
        """Cuando el campo de entrada recibe foco, borra el contenido y pega el contenido del portapapeles."""
        self.notify("Pega la URL en el campo de entrada.")

    @on(Button.Pressed, "#analizar_btn")
    def analizar_url(self, event: Button.Pressed) -> None:
        """Acción cuando se presiona el botón 'Analizar'."""
        url = self.query_one("#url_input", Input).value
        #a_table = [("Audio 1", "1"), ("Audio 2", "2"), ("Audio 3", "3")]
        #v_table = [("Video 1", "1"), ("Video 2", "2"), ("Video 3", "3")]
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
        self.query_one("#a-seleccion_label", Label).update(f"Audio ID: {self.id_a}")

    @on(Select.Changed, "#select_video")
    def video_selected(self, event: Select.Changed) -> None:
        """Actualizar ID de video"""
        self.id_v = event.value if event.value != Select.BLANK else ""
        self.query_one("#v-seleccion_label", Label).update(f"Video ID: {self.id_v}")
        format = [f for f in self.formats if f["format_id"] == self.id_v]
        self.query_one("#resolution_label", Label).update(f"Resolucion: {format[0]['resolution']}")
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
        self.title = ""
        self.formats = []

    def compose(self) -> ComposeResult:
        
            yield Grid(
                LoadingIndicator(),
                Label("Verificando URL espera...", id="question"),
                id="Verfy_URL",
            )
         
            #with Container(classes="Select"):
            #            yield LoadingIndicator()
    def on_mount(self) -> None:
        """Ejecutar al montar la pantalla."""
        #self.a_tuple, self.v_tuple = ytpy.filter_json(self.url,exc)  # Procesar URL   
        self.run_worker(self.verify_url,exclusive=True,thread=True)  # Ejecutar en segundo plano


    def verify_url(self):
        """Ejecuta la verificación de la URL en segundo plano."""
        self.a_tuple, self.v_tuple,self.title,self.formats = ytpy.filter_json(self.url)  # Procesa la URL
        # Cuando termine, pasa los datos a DownloadOptions en el hilo principal
        if self.previous_screen:
            self.previous_screen.receive_data(self.a_tuple, self.v_tuple,self.title,self.formats)
        self.app.pop_screen()
        
    @on(Button.Pressed, "#cancel")
    def cancel(self, event: Button.Pressed) -> None:
        """Cancelar verificación de URL"""
        self.app.pop_screen()

class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit",classes="quit_btn"),
            Button("Cancel", variant="primary", id="cancel",classes="quit_btn"),
            id="dialog",
        )
           
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

class App(App):

    def on_mount(self) -> None:
        self.push_screen(DownloadOptions([],[]))  # Instanciar correctamente



if __name__ == "__main__":
    app = App()
    app.run()
