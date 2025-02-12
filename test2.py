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
a_table=("x","y","x")
v_table=("1","2","3")
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
            #header = Static("Selecciona un formato de Audio y Video")
                with Container():
                    yield Input(placeholder="Pega una URL")
                    yield Button("Analizar",variant="success",id="Descargar")
                    yield Label() 
                    yield Static("oliguis")
                    yield Select.from_values(
                    a_table,
                    prompt="Selecciona un formato de audio"
                    )
                    yield Select.from_values(
                    v_table,
                    prompt="Selecciona un formato de video"
                    )
        # Crear los botones
                cancel_button = Button("Cancelar",variant="success")
                download_button = Button("Descargar")
                with Horizontal():
                    yield cancel_button
                    yield download_button
    @on(Button.Pressed, "#Descargar")
    def percent_pressed(self) -> None:
        print("")

#def select_format(a_table, v_table, url):
app = UserSelected()
app.run()
    
