from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.gridlayout import GridLayout
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
                                               'progress_bar': None, 
                                               'reset_button': None,
                                               'dias_label': None,
                                               'horas_label': None,
                                               'minutos_label': None,
                                               'segundos_label': None}
        
        # Crear un Label para la actividad
        actividad_label = Label(text=f"{nombre_actividad}: ", font_size='20sp', size_hint_y=None, height=40)
        
        # Crear un botón para reiniciar la actividad
        reset_button = Button(text="Reiniciar", size_hint_y=None, height=40)
        reset_button.bind(on_press=lambda instance, nombre_actividad=nombre_actividad: self.reiniciar_contador(nombre_actividad))
        self.actividades[nombre_actividad]['reset_button'] = reset_button
        
        # Crear una barra de progreso personalizada para mostrar los días, horas, minutos y segundos
        barra_contenedora = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.actividades[nombre_actividad]['progress_bar'] = barra_contenedora
        
        # **Creación de las etiquetas de días, horas, minutos y segundos dentro de la barra**:
        dias_label = Label(text="0d", size_hint_x=None, width=80)
        horas_label = Label(text="0h", size_hint_x=None, width=80)
        minutos_label = Label(text="0m", size_hint_x=None, width=80)
        segundos_label = Label(text="0s", size_hint_x=None, width=80)
        
        # **Guardar las etiquetas dentro del diccionario de la actividad**:
        self.actividades[nombre_actividad]['dias_label'] = dias_label
        self.actividades[nombre_actividad]['horas_label'] = horas_label
        self.actividades[nombre_actividad]['minutos_label'] = minutos_label
        self.actividades[nombre_actividad]['segundos_label'] = segundos_label
        
        # Añadir las etiquetas dentro de la barra
        barra_contenedora.add_widget(dias_label)
        barra_contenedora.add_widget(horas_label)
        barra_contenedora.add_widget(minutos_label)
        barra_contenedora.add_widget(segundos_label)
        
        # Agregar la etiqueta de la actividad, la barra de progreso y el botón de reinicio al contenedor
        self.actividades_container.add_widget(actividad_label)
        self.actividades_container.add_widget(barra_contenedora)
        self.actividades_container.add_widget(reset_button)
    
    # Limpiar el campo de entrada
    self.nombre_actividad_input.text = ""


    def actualizar_contadores(self, dt):
        # Recorre todas las actividades y actualiza su barra de progreso
        ahora = datetime.now()
        
        for nombre_actividad, datos in self.actividades.items():
            # Calcula el tiempo transcurrido para cada actividad
            tiempo_transcurrido = ahora - datos['ultima_actividad']
            
            # Divide en días, horas, minutos y segundos
            dias, resto = divmod(tiempo_transcurrido.total_seconds(), 86400)
            horas, resto = divmod(resto, 3600)
            minutos, segundos = divmod(resto, 60)
            
            # Actualiza las etiquetas de días, horas, minutos y segundos
            datos['dias_label'].text = f"{int(dias)}d"
            datos['horas_label'].text = f"{int(horas)}h"
            datos['minutos_label'].text = f"{int(minutos)}m"
            datos['segundos_label'].text = f"{int(segundos)}s"
            
            # Calcular el porcentaje total de tiempo transcurrido del día
            tiempo_total_segundos = 86400  # Un día tiene 86400 segundos
            tiempo_pasado_segundos = tiempo_transcurrido.total_seconds()
            porcentaje = tiempo_pasado_segundos / tiempo_total_segundos
            
            # Asigna el valor al contenedor de la barra (representa el tiempo total de un día)
            # Cada sección dentro de la barra representa días, horas, minutos y segundos.
            datos['progress_bar'].width = (porcentaje * 320)  # Ancho total para la barra (320px como ejemplo)
            
    def reiniciar_contador(self, nombre_actividad):
        # Reinicia el tiempo de la última actividad de la actividad específica
        self.actividades[nombre_actividad]['ultima_actividad'] = datetime.now()

if __name__ == "__main__":
    ContadorApp().run()
