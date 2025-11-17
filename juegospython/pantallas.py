import pygame
from componentes import Boton, GeneradorConjuntos, dibujar_texto, dibujar_conjunto, dibujar_diagrama_venn

# Colores globales
BLANCO = (255, 255, 255)
NEGRO = (50, 50, 50)
MORADO = (102, 126, 234)
MORADO_OSCURO = (118, 75, 162)
GRIS_CLARO = (248, 249, 250)
GRIS = (200, 200, 200)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)

class Menu:
    def __init__(self, ancho, alto):
        """
        Inicializa el menu principal
        
        Args:
            ancho: Ancho de la pantalla
            alto: Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        
        # Crear botones del menu
        boton_ancho = 300
        boton_alto = 60
        boton_x = ancho // 2 - boton_ancho // 2
        inicio_y = 300
        
        self.boton_jugar = Boton(
            boton_x, inicio_y, boton_ancho, boton_alto,
            "JUGAR", MORADO, MORADO_OSCURO, BLANCO
        )
        
        self.boton_tutorial = Boton(
            boton_x, inicio_y + 80, boton_ancho, boton_alto,
            "TUTORIAL", BLANCO, GRIS_CLARO, MORADO
        )
        
        self.boton_salir = Boton(
            boton_x, inicio_y + 160, boton_ancho, boton_alto,
            "SALIR", BLANCO, GRIS_CLARO, MORADO
        )
        
    def dibujar(self, pantalla):
        """
        Dibuja el menu principal en la pantalla
        """
        # Fondo blanco
        pantalla.fill(BLANCO)
        
        # Titulo del juego
        dibujar_texto(pantalla, "SET-ZERO", self.ancho // 2, 150, 100, MORADO)
        
        # Subtitulo
        dibujar_texto(pantalla, "Domina la Teoria de Conjuntos", 
                     self.ancho // 2, 220, 28, GRIS)
        
        # Dibujar botones
        self.boton_jugar.dibujar(pantalla)
        self.boton_tutorial.dibujar(pantalla)
        self.boton_salir.dibujar(pantalla)
        
    def manejar_evento(self, evento):
        """
        Maneja los eventos del menu
        
        Returns:
            String indicando la accion: 'jugar', 'tutorial', 'salir', o None
        """
        if self.boton_jugar.click(evento):
            return "jugar"
        elif self.boton_tutorial.click(evento):
            return "tutorial"
        elif self.boton_salir.click(evento):
            return "salir"
        return None


class Juego:
    def __init__(self, ancho, alto):
        """
        Inicializa el juego Set Battle
        
        Args:
            ancho: Ancho de la pantalla
            alto: Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        self.generador = GeneradorConjuntos()
        self.puntos = 0
        self.tiempo_restante = 15
        self.tiempo_inicio = None
        self.pregunta_actual = None
        self.juego_activo = False
        
        # Variables para feedback visual
        self.respuesta_seleccionada = None
        self.es_correcta = None
        self.tiempo_feedback = 0
        self.mostrando_feedback = False
        
        # Crear boton de volver
        self.boton_volver = Boton(
            50, alto - 80, 200, 50,
            "VOLVER", BLANCO, GRIS_CLARO, MORADO
        )
        
        # Botones para las respuestas
        self.botones_respuesta = []
        self.crear_botones_respuesta()
        
    def crear_botones_respuesta(self):
        """
        Crea los 4 botones para las opciones de respuesta
        """
        self.botones_respuesta = []
        boton_ancho = 300
        boton_alto = 60
        espacio = 20
        inicio_x = self.ancho // 2 - (boton_ancho + espacio // 2)
        inicio_y = 450
        
        # Crear grid 2x2 de botones
        posiciones = [
            (inicio_x, inicio_y),
            (inicio_x + boton_ancho + espacio, inicio_y),
            (inicio_x, inicio_y + boton_alto + espacio),
            (inicio_x + boton_ancho + espacio, inicio_y + boton_alto + espacio)
        ]
        
        for x, y in posiciones:
            boton = Boton(x, y, boton_ancho, boton_alto, "", BLANCO, GRIS_CLARO, NEGRO)
            self.botones_respuesta.append(boton)
    
    def iniciar_juego(self):
        """
        Inicia una nueva partida
        """
        self.juego_activo = True
        self.puntos = 0
        self.nueva_pregunta()
        
    def nueva_pregunta(self):
        """
        Genera una nueva pregunta y reinicia el temporizador
        """
        self.pregunta_actual = self.generador.generar_pregunta()
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_restante = 15
        
        # Resetear feedback
        self.mostrando_feedback = False
        self.respuesta_seleccionada = None
        self.es_correcta = None
        
        # Actualizar texto de los botones con las opciones
        for i, opcion in enumerate(self.pregunta_actual["opciones"]):
            elementos = sorted(list(opcion))
            texto = "{" + ", ".join(map(str, elementos)) + "}"
            self.botones_respuesta[i].texto = texto
            
    def actualizar(self):
        """
        Actualiza el estado del juego (temporizador y feedback)
        """
        if self.juego_activo and self.tiempo_inicio:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) // 1000
            self.tiempo_restante = 15 - tiempo_transcurrido
            
            # Si se acaba el tiempo, generar nueva pregunta
            if self.tiempo_restante <= 0:
                self.nueva_pregunta()
            
            # Manejar feedback visual (mostrar por 1 segundo)
            if self.mostrando_feedback:
                tiempo_desde_feedback = tiempo_actual - self.tiempo_feedback
                if tiempo_desde_feedback > 1000:  # 1 segundo
                    self.mostrando_feedback = False
                    self.respuesta_seleccionada = None
                    self.es_correcta = None
                    self.nueva_pregunta()
    
    def verificar_respuesta(self, indice_boton):
        """
        Verifica si la respuesta seleccionada es correcta
        
        Args:
            indice_boton: Indice del boton clickeado (0-3)
        """
        opcion_seleccionada = self.pregunta_actual["opciones"][indice_boton]
        respuesta_correcta = self.pregunta_actual["respuesta_correcta"]
        
        # Guardar que boton fue clickeado
        self.respuesta_seleccionada = indice_boton
        
        # Verificar si es correcta
        if opcion_seleccionada == respuesta_correcta:
            self.es_correcta = True
            self.puntos += 10
        else:
            self.es_correcta = False
        
        # Activar feedback visual
        self.mostrando_feedback = True
        self.tiempo_feedback = pygame.time.get_ticks()
    
    def dibujar(self, pantalla):
        """
        Dibuja el juego en la pantalla
        """
        # Fondo blanco
        pantalla.fill(BLANCO)
        
        if not self.juego_activo or not self.pregunta_actual:
            # Pantalla de inicio del juego
            dibujar_texto(pantalla, "SET BATTLE", self.ancho // 2, 200, 80, MORADO)
            dibujar_texto(pantalla, "Presiona ESPACIO para comenzar", 
                         self.ancho // 2, 300, 36, GRIS)
            self.boton_volver.dibujar(pantalla)
            return
        
        # Dibujar encabezado con tiempo y puntos
        # Caja de tiempo
        pygame.draw.rect(pantalla, MORADO, (50, 30, 200, 60), border_radius=12)
        dibujar_texto(pantalla, f"Tiempo: {self.tiempo_restante}s", 150, 60, 32, BLANCO)
        
        # Caja de puntos
        pygame.draw.rect(pantalla, MORADO, (self.ancho - 250, 30, 200, 60), border_radius=12)
        dibujar_texto(pantalla, f"Puntos: {self.puntos}", self.ancho - 150, 60, 32, BLANCO)
        
        # Area de pregunta
        pygame.draw.rect(pantalla, GRIS_CLARO, (100, 120, self.ancho - 200, 300), border_radius=15)
        
        # Texto de la pregunta
        pregunta_texto = f"Cual es el resultado de A {self.pregunta_actual['simbolo']} B?"
        dibujar_texto(pantalla, pregunta_texto, self.ancho // 2, 160, 36, NEGRO)
        
        # Dibujar conjuntos
        conjunto_a = self.pregunta_actual["conjunto_a"]
        conjunto_b = self.pregunta_actual["conjunto_b"]
        
        dibujar_conjunto(pantalla, conjunto_a, 150, 200, 250, 100, "A", MORADO)
        dibujar_conjunto(pantalla, conjunto_b, self.ancho - 400, 200, 250, 100, "B", MORADO_OSCURO)
        
        # Dibujar diagrama de Venn
        dibujar_diagrama_venn(pantalla, self.ancho // 2, 280, conjunto_a, conjunto_b)
        
        # Dibujar botones de respuesta con colores segun feedback
        for i, boton in enumerate(self.botones_respuesta):
            # Si esta mostrando feedback y es este boton
            if self.mostrando_feedback and i == self.respuesta_seleccionada:
                # Cambiar color segun si es correcta o no
                if self.es_correcta:
                    boton.color = VERDE
                    boton.color_hover = VERDE
                else:
                    boton.color = ROJO
                    boton.color_hover = ROJO
            else:
                # Colores normales
                boton.color = BLANCO
                boton.color_hover = GRIS_CLARO
            
            boton.dibujar(pantalla)
        
        # Boton volver
        self.boton_volver.dibujar(pantalla)
    
    def manejar_evento(self, evento):
        """
        Maneja los eventos del juego
        
        Returns:
            String indicando la accion o None
        """
        # Boton volver
        if self.boton_volver.click(evento):
            self.juego_activo = False
            return "menu"
        
        # Iniciar juego con ESPACIO
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if not self.juego_activo:
                self.iniciar_juego()
        
        # Verificar clicks en botones de respuesta solo si no esta mostrando feedback
        if self.juego_activo and self.pregunta_actual and not self.mostrando_feedback:
            for i, boton in enumerate(self.botones_respuesta):
                if boton.click(evento):
                    self.verificar_respuesta(i)
        
        return None


class Tutorial:
    def __init__(self, ancho, alto):
        """
        Inicializa el tutorial
        
        Args:
            ancho: Ancho de la pantalla
            alto: Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        self.pagina_actual = 0
        
        # Definir conceptos del tutorial
        self.conceptos = [
            {
                "nombre": "Union",
                "simbolo": "∪",
                "descripcion": "La union de dos conjuntos contiene todos los elementos que estan en A, en B, o en ambos.",
                "ejemplo_a": "{1, 2, 3}",
                "ejemplo_b": "{3, 4, 5}",
                "ejemplo_resultado": "{1, 2, 3, 4, 5}"
            },
            {
                "nombre": "Interseccion",
                "simbolo": "∩",
                "descripcion": "La interseccion contiene solo los elementos que estan en ambos conjuntos simultaneamente.",
                "ejemplo_a": "{1, 2, 3}",
                "ejemplo_b": "{3, 4, 5}",
                "ejemplo_resultado": "{3}"
            },
            {
                "nombre": "Diferencia",
                "simbolo": "-",
                "descripcion": "La diferencia A - B contiene los elementos que estan en A pero no en B.",
                "ejemplo_a": "{1, 2, 3, 4}",
                "ejemplo_b": "{3, 4, 5}",
                "ejemplo_resultado": "{1, 2}"
            },
            {
                "nombre": "Complemento",
                "simbolo": "'",
                "descripcion": "El complemento de A contiene todos los elementos del universo que no estan en A.",
                "ejemplo_a": "U = {1, 2, 3, 4, 5}",
                "ejemplo_b": "A = {1, 2}",
                "ejemplo_resultado": "A' = {3, 4, 5}"
            },
            {
                "nombre": "Diferencia Simetrica",
                "simbolo": "Δ",
                "descripcion": "La diferencia simetrica contiene elementos que estan en A o en B, pero no en ambos.",
                "ejemplo_a": "{1, 2, 3}",
                "ejemplo_b": "{3, 4, 5}",
                "ejemplo_resultado": "{1, 2, 4, 5}"
            }
        ]
        
        # Crear botones de navegacion
        self.boton_volver = Boton(
            50, alto - 80, 200, 50,
            "VOLVER", BLANCO, GRIS_CLARO, MORADO
        )
        
        self.boton_anterior = Boton(
            ancho // 2 - 220, alto - 80, 200, 50,
            "ANTERIOR", BLANCO, GRIS_CLARO, MORADO
        )
        
        self.boton_siguiente = Boton(
            ancho // 2 + 20, alto - 80, 200, 50,
            "SIGUIENTE", MORADO, MORADO_OSCURO, BLANCO
        )
    
    def dibujar(self, pantalla):
        """
        Dibuja el tutorial en la pantalla
        """
        # Fondo blanco
        pantalla.fill(BLANCO)
        
        # Titulo
        dibujar_texto(pantalla, "TUTORIAL", self.ancho // 2, 60, 64, MORADO)
        dibujar_texto(pantalla, "Operaciones de Conjuntos", self.ancho // 2, 110, 32, GRIS)
        
        # Obtener concepto actual
        concepto = self.conceptos[self.pagina_actual]
        
        # Caja del concepto
        pygame.draw.rect(pantalla, GRIS_CLARO, (100, 160, self.ancho - 200, 350), border_radius=15)
        
        # Borde izquierdo de color
        pygame.draw.rect(pantalla, MORADO, (100, 160, 8, 350), border_radius=15)
        
        # Nombre y simbolo del concepto
        texto_titulo = f"{concepto['nombre']} ({concepto['simbolo']})"
        dibujar_texto(pantalla, texto_titulo, self.ancho // 2, 200, 48, NEGRO)
        
        # Descripcion
        self.dibujar_texto_multiple_lineas(
            pantalla, concepto['descripcion'], 
            150, 250, self.ancho - 300, 28, NEGRO
        )
        
        # Caja de ejemplo
        pygame.draw.rect(pantalla, BLANCO, (150, 350, self.ancho - 300, 130), border_radius=10)
        
        dibujar_texto(pantalla, "Ejemplo:", 200, 370, 28, MORADO, centrado=False)
        
        # Lineas del ejemplo
        y_ejemplo = 400
        dibujar_texto(pantalla, f"A = {concepto['ejemplo_a']}", 200, y_ejemplo, 24, NEGRO, centrado=False)
        dibujar_texto(pantalla, f"B = {concepto['ejemplo_b']}", 200, y_ejemplo + 30, 24, NEGRO, centrado=False)
        dibujar_texto(pantalla, concepto['ejemplo_resultado'], 200, y_ejemplo + 60, 24, MORADO, centrado=False)
        
        # Indicador de pagina
        texto_pagina = f"{self.pagina_actual + 1} / {len(self.conceptos)}"
        dibujar_texto(pantalla, texto_pagina, self.ancho // 2, 540, 24, GRIS)
        
        # Dibujar botones
        self.boton_volver.dibujar(pantalla)
        
        # Solo mostrar boton anterior si no estamos en la primera pagina
        if self.pagina_actual > 0:
            self.boton_anterior.dibujar(pantalla)
        
        # Solo mostrar boton siguiente si no estamos en la ultima pagina
        if self.pagina_actual < len(self.conceptos) - 1:
            self.boton_siguiente.dibujar(pantalla)
    
    def dibujar_texto_multiple_lineas(self, pantalla, texto, x, y, ancho_max, tamaño, color):
        """
        Dibuja texto que se ajusta en multiples lineas
        
        Args:
            pantalla: Surface de pygame
            texto: Texto a dibujar
            x, y: Posicion inicial
            ancho_max: Ancho maximo antes de hacer salto de linea
            tamaño: Tamaño de fuente
            color: Color del texto
        """
        fuente = pygame.font.Font(None, tamaño)
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            prueba = linea_actual + palabra + " "
            if fuente.size(prueba)[0] <= ancho_max:
                linea_actual = prueba
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual)
        
        # Dibujar cada linea
        for i, linea in enumerate(lineas):
            superficie_texto = fuente.render(linea, True, color)
            pantalla.blit(superficie_texto, (x, y + i * 30))
    
    def manejar_evento(self, evento):
        """
        Maneja los eventos del tutorial
        
        Returns:
            String indicando la accion o None
        """
        if self.boton_volver.click(evento):
            return "menu"
        
        if self.boton_anterior.click(evento):
            if self.pagina_actual > 0:
                self.pagina_actual -= 1
        
        if self.boton_siguiente.click(evento):
            if self.pagina_actual < len(self.conceptos) - 1:
                self.pagina_actual += 1
        
        return None