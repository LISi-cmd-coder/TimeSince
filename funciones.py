from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from datetime import datetime

class ContadorApp(App):
    def build(self):
        # Inicializa el tiempo de la última actividad
        self.actividades = {}  # Diccionario para almacenar actividades y tiempos
        
        # Crea la interfaz de usuario
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.bg_color = (20/255, 54/255, 66/255, 1)  # Fondo en color #143642
        
        # Campo de entrada para el nombre de la actividad
        self.nombre_actividad_input = TextInput(hint_text="Nombre de la actividad", size_hint_y=None, height=30)
        layout.add_widget(self.nombre_actividad_input)
        
        # Botón para agregar una nueva actividad
        self.agregar_actividad_button = Button(text="Agregar Actividad", size_hint_y=None, height=40)
        self.agregar_actividad_button.bind(on_press=self.agregar_actividad)
        layout.add_widget(self.agregar_actividad_button)
        
        # Panel para mostrar las actividades
        self.actividades_panel = ScrollView(size_hint=(1, None), size=(400, 400))
        self.actividades_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.actividades_container.bind(minimum_height=self.actividades_container.setter('height'))
        self.actividades_panel.add_widget(self.actividades_container)
        layout.add_widget(self.actividades_panel)
        
        # Inicia el contador de tiempo para las actividades
        Clock.schedule_interval(self.actualizar_contadores, 1)
        
        return layout

    def agregar_actividad(self, instance):
        # Obtiene el nombre de la actividad desde el campo de entrada
        nombre_actividad = self.nombre_actividad_input.text.strip()
        
        if nombre_actividad:
            # Inicializa el tiempo de la última actividad
            self.actividades[nombre_actividad] = {'ultima_actividad': datetime.now(), 
                                                   'label': None, 
                                                   'progress_bar': None}
            
            # Crear un Label para la actividad
            actividad_label = Label(text=f"{nombre_actividad}: ", font_size='20sp', size_hint_y=None, height=40)
            self.actividades[nombre_actividad]['label'] = actividad_label
            
            # Crear un ProgressBar para mostrar el tiempo transcurrido
            progress_bar = ProgressBar(max=86400, size_hint_y=None, height=40)  # Maximo en segundos por un día
            self.actividades[nombre_actividad]['progress_bar'] = progress_bar
            
            # Agregar la etiqueta de la actividad y la barra de progreso al contenedor
            self.actividades_container.add_widget(actividad_label)
            self.actividades_container.add_widget(progress_bar)
        
        # Limpiar el campo de entrada
        self.nombre_actividad_input.text = ""

    def actualizar_contadores(self, dt):
        # Recorre todas las actividades y actualiza su barra de progreso
        ahora = datetime.now()
        
        for nombre_actividad, datos in self.actividades.items():
            # Calcula el tiempo transcurrido para cada actividad
            tiempo_transcurrido = ahora - datos['ultima_actividad']
            
            # Obtiene el tiempo total de un día (86400 segundos)
            tiempo_total_segundos = 86400  # Un día tiene 86400 segundos
            tiempo_pasado_segundos = tiempo_transcurrido.total_seconds()
            
            # Calcula el porcentaje de tiempo transcurrido
            porcentaje = tiempo_pasado_segundos / tiempo_total_segundos
            
            # Actualiza la barra de progreso para la actividad
            datos['progress_bar'].value = porcentaje * datos['progress_bar'].max
            
            # Actualiza la etiqueta para mostrar el tiempo en formato de días, horas, minutos y segundos
            dias, resto = divmod(tiempo_transcurrido.total_seconds(), 86400)
            horas, resto = divmod(resto, 3600)
            minutos, segundos = divmod(resto, 60)
            
            # Actualiza el texto de la actividad
            datos['label'].text = f"{nombre_actividad}: {int(dias)}d {int(horas)}h {int(minutos)}m {int(segundos)}s"

    def reiniciar_contador(self, nombre_actividad):
        # Reinicia el tiempo de la última actividad de la actividad específica
        self.actividades[nombre_actividad]['ultima_actividad'] = datetime.now()

if __name__ == "__main__":
    ContadorApp().run()
