import ytpy 
from textual import on ,containers
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, Horizontal, Vertical
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
    CSS_PATH = "select.css"
    # def __init__(self, a_table, v_table):
    #     super().__init__()
    #     self.a_table = a_table 
    #     self.a_table = [(option, option) for option in a_table]    
    #     self.v_table = v_table 
    #     self.v_table = [(option, option) for option in v_table]
    
    def compose(self) -> ComposeResult:
        
        # Crear los widgets
        with Container(id="menu",classes="container") as container:
            container.border_title = "Menu"
            with TabbedContent ("opciones", "configurciones",classes="grid"):
                with Container(classes="container"):
                    yield Input(placeholder="Pega una URL",id="url_input")
                    yield Button("Analizar",variant="success",id="analizar_btn")
                    yield Label(id="resultado_label") 
                    yield Static("Secciona Los formatos de audio y video")
                    yield Select([],prompt="Selecciona un formato de audio",classes="select",id="audio")
                    yield Select([],prompt="Selecciona un formato de video",classes="select",id="video")
                    yield Label(id="seleccion_label") 
        # Crear los botones
                cancel_button = Button("Cancelar",variant="success")
                download_button = Button("Descargar")
                with Horizontal():
                    yield cancel_button
                    yield download_button
    @on(Button.Pressed, "#analizar_btn")
    def analizar_url(self, event: Button.Pressed) -> None:
        """Acción cuando se presiona el botón 'Analizar'."""
        
        #self.query_one("#audio", Select).set_options([])       
        #self.query_one("#video", Select).set_options([])
        url = self.query_one("#url_input", Input).value
        a_table , v_table =  ytpy.filter_json(url)
        self.query_one("#audio", Select).set_options(a_table)
        self.query_one("#video", Select).set_options(v_table)
        resultado = f"URL: {url}\nFormatos actualizados."
        self.query_one("#resultado_label", Label).update(resultado)

    @on(Select.Changed, "#audio")
    def audio_selected(self, event: Select.Changed) -> None:
        """Acción cuando se selecciona un formato de audio."""
        selected = event.value
        id_a = selected
        self.query_one("#seleccion_label", Label).update(f"Audio ID: {id_a} Video ID: {id_v}")
    
    @on(Select.Changed, "#video")
    def video_selected(self, event: Select.Changed) -> None:
        """Acción cuando se selecciona un formato de video."""
        selected = event.value
        id_v = selected
        self.query_one("#seleccion_label", Label).update(f"Audio ID: {id_a} Video ID: {id_v}")

app = UserSelected()
app.run()
    
