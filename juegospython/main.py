import pygame
import sys
from pantallas import Menu, Juego, Tutorial
aaaaaa
# Configuracion de la ventana
ANCHO_VENTANA = 1080
ALTO_VENTANA = 600
FPS = 60
TITULO = "Set-Zero"

class JuegoSetZero:
    def __init__(self):
        """
        Inicializa el juego principal
        """
        # Inicializar pygame
        pygame.init()
        
        # Crear ventana
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption(TITULO)
        
        # Reloj para controlar FPS
        self.reloj = pygame.time.Clock()
        
        # Estado actual del juego
        self.estado = "menu"  # Puede ser: 'menu', 'juego', 'tutorial'
        
        # Instanciar pantallas
        self.menu = Menu(ANCHO_VENTANA, ALTO_VENTANA)
        self.juego = Juego(ANCHO_VENTANA, ALTO_VENTANA)
        self.tutorial = Tutorial(ANCHO_VENTANA, ALTO_VENTANA)
        
        # Variable de control del loop principal
        self.ejecutando = True
    
    def manejar_eventos(self):
        """
        Maneja todos los eventos del juego
        """
        for evento in pygame.event.get():
            # Evento de cierre de ventana
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            
            # Delegar eventos segun el estado actual
            if self.estado == "menu":
                accion = self.menu.manejar_evento(evento)
                if accion == "jugar":
                    self.estado = "juego"
                elif accion == "tutorial":
                    self.estado = "tutorial"
                elif accion == "salir":
                    self.ejecutando = False
            
            elif self.estado == "juego":
                accion = self.juego.manejar_evento(evento)
                if accion == "menu":
                    self.estado = "menu"
            
            elif self.estado == "tutorial":
                accion = self.tutorial.manejar_evento(evento)
                if accion == "menu":
                    self.estado = "menu"
    
    def actualizar(self):
        """
        Actualiza la logica del juego
        """
        if self.estado == "juego":
            self.juego.actualizar()
    
    def dibujar(self):
        """
        Dibuja el estado actual del juego
        """
        # Dibujar segun el estado actual
        if self.estado == "menu":
            self.menu.dibujar(self.pantalla)
        elif self.estado == "juego":
            self.juego.dibujar(self.pantalla)
        elif self.estado == "tutorial":
            self.tutorial.dibujar(self.pantalla)
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def ejecutar(self):
        """
        Loop principal del juego
        """
        while self.ejecutando:
            # Manejar eventos
            self.manejar_eventos()
            
            # Actualizar logica
            self.actualizar()
            
            # Dibujar
            self.dibujar()
            
            # Controlar FPS
            self.reloj.tick(FPS)
        
        # Salir del juego
        pygame.quit()
        sys.exit()


# Punto de entrada del programa
if __name__ == "__main__":
    juego = JuegoSetZero()
    juego.ejecutar()