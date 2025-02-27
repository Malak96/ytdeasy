import ytpy 
from textual import on ,containers
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical 
from textual.theme import BUILTIN_THEMES
from textual.widgets import (
    Select,
    Label,
    Input,
    Header,
    TabbedContent,
    TextArea, 
    Button, 
    Static)
id_a = ""
id_v = ""

class UserSelected(App):
    #self.theme = BUILTIN_THEMES["dark"]
    CSS_PATH = "select.css"
    def compose(self) -> ComposeResult:
        with VerticalScroll():
        # Crear los widgets
            with Container(id="menu",classes="center_all") as container:
            #    container.border_title = "Menu"
                with Container(classes="url_container"):
                    #yield Header("Descargar Videos de Youtube",level=1,classes="center_all")
                    with containers.ItemGrid(min_column_width=2, regular=False,classes="center_m"):
                        yield Input(placeholder="Pega una URL",id="url_input")
                        yield Button("Analizar",variant="success",id="analizar_btn",classes="center_all")
                    
                with TabbedContent ("Descargar Video", "Descargar Audio", "Configuraciones",classes="center_all"):
                    with Container(classes="container"):
                        yield Label(id="resultado_label") 
                        yield Label("Secciona Los formatos de audio y video")
                        yield Select([],prompt="Selecciona un formato de audio",classes="Select",id="audio")
                        yield Select([],prompt="Selecciona un formato de video",classes="Select",id="video")
                        yield Label("Audio ID: ",id="a-seleccion_label") 
                        yield Label("Video ID: ",id="v-seleccion_label")
                    with Container(classes="container"):
                        #yield Static("Secciona el formato de audio")
                        yield Select([],prompt="Selecciona un formato de audio",classes="select",id="audio_only")
                        
                        yield Label("Audio ID: ", id="a-seleccion_label")

                # Crear los botones
                    cancel_button = Button("Cancelar",variant="success")
                    download_button = Button("Descargar")
                    with Horizontal():
                        yield cancel_button
                        yield download_button
        @on(Button.Pressed, "#analizar_btn")
        def analizar_url(self, event: Button.Pressed) -> None:
            """Acción cuando se presiona el botón 'Analizar'."""
            url = self.query_one("#url_input", Input).value
            a_table = None
            v_table = None
            a_table , v_table =  ytpy.filter_json(url)
            self.query_one("#audio", Select).set_options(a_table)
            self.query_one("#audio_only", Select).set_options(a_table)
            self.query_one("#video", Select).set_options(v_table)
            resultado = f"URL: {url}\nFormatos actualizados."
            self.query_one("#resultado_label", Label).update(resultado)

    @on(Select.Changed, "#audio")
    def audio_selected(self, event: Select.Changed) -> None:
        """Acción cuando se selecciona un formato de audio."""
        if event.value != Select.BLANK:
            selected = event.value
        else:
            selected = ""
        id_a = selected
        self.query_one("#a-seleccion_label", Label).update(f"Audio ID: {id_a}")
    
    @on(Select.Changed, "#video")
    def video_selected(self, event: Select.Changed) -> None:
        """Acción cuando se selecciona un formato de video."""
        if event.value != Select.BLANK:
            selected = event.value
        else:
            selected = ""
        id_v = selected
        self.query_one("#v-seleccion_label", Label).update(f"Video ID: {id_v}")




app = UserSelected()
app.run()
    
