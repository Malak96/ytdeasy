import ytpy
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
class InputUrl(Screen):
    
    
    def compose(self) -> ComposeResult:
        
        with Container(classes="center_all"):
            with Grid(classes="center_all"):
                yield Input(placeholder="Pega una URL", id="url_input",value="https://www.youtube.com/watch?v=CsrmS0id6So")
                yield Button("🔎", id="analizar_btn", classes="center_all")
                yield Button("Salir", id="salir_btn")
    @on(Button.Pressed, "#salir_btn")
    def salir(self, event: Button.Pressed) -> None:
        """Mostrar pantalla de confirmación para salir."""      
        self.app.push_screen(QuitScreen()) 

    @on(Button.Pressed, "#analizar_btn")
    def analizar_url(self, event: Button.Pressed) -> None:
        """Acción cuando se presiona el botón 'Analizar'."""
        url = self.query_one("#url_input", Input).value
        a_table , v_table =  ytpy.filter_json(url)
        #resultado = f"URL: {url}\nFormatos actualizados."
        #self.query_one("#resultado_label", Label).update(resultado)
        a_table = [("Audio 1", "1"), ("Audio 2", "2"), ("Audio 3", "3")]
        v_table = [("Video 1", "1"), ("Video 2", "2"), ("Video 3", "3")]
        if url:
            self.app.push_screen(DownloadOptions(a_table, v_table))

class DownloadOptions(Screen):
    CSS_PATH = "assents.css"
    def __init__(self, a_table=None, v_table=None):
        super().__init__()
        self.id_a = ""
        self.id_v = ""
        self.a_table = a_table or []
        self.v_table = v_table or []
    def compose(self) -> ComposeResult:
        self.app.theme = "monokai"
        #with VerticalScroll():
        with TabbedContent("Descargar", "Configuraciones", id="tab_c", classes="tab_align", disabled=False):
            with VerticalScroll():
                #with ItemGrid(min_column_width=1,regular=True):
                with ItemGrid(min_column_width=1,regular=True,classes="center_all"):
                    yield Input(placeholder="Click derecho para copiar el portapapeles", id="url_input",value="https://www.youtube.com/watch?v=CsrmS0id6So")
                    #yield Button("", id="paste_btn")
                    yield Button("Verificar URL", id="analizar_btn")
                
                yield Label(id="resultado_label")
                with Container(classes="Select"):
                    yield LoadingIndicator()
                yield Select(self.a_table, prompt="Selecciona el audio", classes="Select", id="select_audio")
                yield Select(self.v_table, prompt="Selecciona el video", classes="Select", id="select_video")
                yield Select(formats, prompt="Formato de Salida", classes="Select", id="output_format")
                yield Label("Audio ID: ", id="a-seleccion_label")
                yield Label("Video ID: ", id="v-seleccion_label")
                with Horizontal(classes="cont_btn_op"):
                    yield Button("Cancelar", variant="success",id="cancelar_btn")
                    yield Button("Descargar")
            with Vertical():
                theme_name = []
                for themes in BUILTIN_THEMES:
                    theme_name.append((themes,themes))
                yield Select(theme_name, prompt="Selecciona un tema", classes="Select", id="theme_select")
                yield Button("Aplicar", id="apply_theme")

                
    @on(Button.Pressed, "#analizar_btn")
    def analizar_url(self, event: Button.Pressed) -> None:
        """Acción cuando se presiona el botón 'Analizar'."""
        url = self.query_one("#url_input", Input).value
        a_table , v_table =  ytpy.filter_json(url)
        self.query_one("#select_audio", Select).set_options(a_table)
        self.query_one("#select_video", Select).set_options(v_table)
        #resultado = f"URL: {url}\nFormatos actualizados."
        #self.query_one("#resultado_label", Label).update(resultado)
        #a_table = [("Audio 1", "1"), ("Audio 2", "2"), ("Audio 3", "3")]
        #v_table = [("Video 1", "1"), ("Video 2", "2"), ("Video 3", "3")]


    @on(Button.Pressed, "#apply_theme")
    def apply_theme(self, event: Button.Pressed) -> None:
        """Aplicar tema seleccionado"""
        theme = self.query_one("#theme_select", Select).value
        self.app.theme = theme
        self.notify(f"Tema aplicado: {theme}")
        
    @on(Button.Pressed, "#cancelar_btn")
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

    @on(Select.Changed, "#output_format")
    def output_format(self, event: Select.Changed) -> None:
        """Habilitar o deshabilitar selección de video según formato"""
        selectes = str(event.value)
        self.query_one("#select_video", Select).disabled = selectes in ["m4a", "mp3", "opus"]
        self.notify(f"Formato seleccionado: {selectes}")

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
