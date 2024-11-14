from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime

class ContadorApp(App):
    def build(self):
        # Inicializa el tiempo de la última actividad
        self.ultima_actividad = datetime.now()
        
        # Crea la interfaz de usuario
        layout = BoxLayout(orientation='vertical')
        self.tiempo_label = Label(text="Tiempo sin actividad:")
        layout.add_widget(self.tiempo_label)
        
        # Etiqueta para el contador
        self.contador_label = Label(text="0d 0h 0m 0s", font_size='30sp')
        layout.add_widget(self.contador_label)
        
        # Botón para reiniciar el contador
        self.reset_button = Button(text="Reiniciar Actividad")
        self.reset_button.bind(on_press=self.reiniciar_contador)
        layout.add_widget(self.reset_button)
        
        # Inicia el contador de tiempo
        Clock.schedule_interval(self.actualizar_contador, 1)
        
        return layout

    def actualizar_contador(self, dt):
        # Calcula el tiempo transcurrido
        ahora = datetime.now()
        tiempo_transcurrido = ahora - self.ultima_actividad
        
        # Divide en días, horas, minutos y segundos
        dias, resto = divmod(tiempo_transcurrido.total_seconds(), 86400)
        horas, resto = divmod(resto, 3600)
        minutos, segundos = divmod(resto, 60)
        
        # Actualiza la etiqueta del contador
        self.contador_label.text = f"{int(dias)}d {int(horas)}h {int(minutos)}m {int(segundos)}s"

    def reiniciar_contador(self, instance):
        # Reinicia el tiempo de la última actividad
        self.ultima_actividad = datetime.now()

if __name__ == "__main__":
    ContadorApp().run()
