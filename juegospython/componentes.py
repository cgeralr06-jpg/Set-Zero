import pygame
import random

# Clase para crear botones interactivos
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color, color_hover, color_texto):
        """
        Inicializa un boton con sus propiedades visuales y de posicion
        
        Args:
            x, y: Posicion del boton
            ancho, alto: Dimensiones del boton
            texto: Texto que muestra el boton
            color: Color normal del boton
            color_hover: Color cuando el mouse esta encima
            color_texto: Color del texto
        """
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = pygame.font.Font(None, 36)
        
    def dibujar(self, pantalla):
        """
        Dibuja el boton en la pantalla
        Cambia de color si el mouse esta encima
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Determinar color segun posicion del mouse
        if self.rect.collidepoint(mouse_pos):
            color_actual = self.color_hover
        else:
            color_actual = self.color
            
        # Dibujar rectangulo del boton
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=12)
        
        # Dibujar texto centrado
        texto_surface = self.fuente.render(self.texto, True, self.color_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        pantalla.blit(texto_surface, texto_rect)
        
    def click(self, evento):
        """
        Verifica si el boton fue clickeado
        
        Returns:
            True si el boton fue clickeado, False en caso contrario
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                return True
        return False


# Clase para manejar la logica de conjuntos
class GeneradorConjuntos:
    def __init__(self):
        """
        Inicializa el generador de conjuntos y preguntas
        """
        self.operaciones = [
            {"simbolo": "U", "nombre": "union"},
            {"simbolo": "∩", "nombre": "interseccion"},
            {"simbolo": "-", "nombre": "diferencia"},
            {"simbolo": "Δ", "nombre": "diferencia_simetrica"}
        ]
        
    def generar_conjunto(self, min_elementos=3, max_elementos=6):
        """
        Genera un conjunto aleatorio de numeros
        
        Args:
            min_elementos: Minimo numero de elementos
            max_elementos: Maximo numero de elementos
            
        Returns:
            Set con numeros aleatorios
        """
        cantidad = random.randint(min_elementos, max_elementos)
        return set(random.sample(range(1, 11), cantidad))
    
    def union(self, conjunto_a, conjunto_b):
        """Retorna la union de dos conjuntos"""
        return conjunto_a | conjunto_b
    
    def interseccion(self, conjunto_a, conjunto_b):
        """Retorna la interseccion de dos conjuntos"""
        return conjunto_a & conjunto_b
    
    def diferencia(self, conjunto_a, conjunto_b):
        """Retorna la diferencia A - B"""
        return conjunto_a - conjunto_b
    
    def diferencia_simetrica(self, conjunto_a, conjunto_b):
        """Retorna la diferencia simetrica de dos conjuntos"""
        return conjunto_a ^ conjunto_b
    
    def calcular_operacion(self, conjunto_a, conjunto_b, operacion):
        """
        Calcula el resultado de una operacion entre dos conjuntos
        
        Args:
            conjunto_a: Primer conjunto
            conjunto_b: Segundo conjunto
            operacion: Nombre de la operacion a realizar
            
        Returns:
            Resultado de la operacion
        """
        if operacion == "union":
            return self.union(conjunto_a, conjunto_b)
        elif operacion == "interseccion":
            return self.interseccion(conjunto_a, conjunto_b)
        elif operacion == "diferencia":
            return self.diferencia(conjunto_a, conjunto_b)
        elif operacion == "diferencia_simetrica":
            return self.diferencia_simetrica(conjunto_a, conjunto_b)
        return set()
    
    def generar_pregunta(self):
        """
        Genera una pregunta completa con conjuntos y operacion
        
        Returns:
            Diccionario con la pregunta, conjuntos, operacion y respuesta correcta
        """
        # Generar dos conjuntos aleatorios
        conjunto_a = self.generar_conjunto()
        conjunto_b = self.generar_conjunto()
        
        # Seleccionar operacion aleatoria
        operacion_info = random.choice(self.operaciones)
        operacion = operacion_info["nombre"]
        simbolo = operacion_info["simbolo"]
        
        # Calcular respuesta correcta
        respuesta_correcta = self.calcular_operacion(conjunto_a, conjunto_b, operacion)
        
        # Generar opciones incorrectas
        opciones = [respuesta_correcta]
        
        # Agregar 3 opciones incorrectas
        while len(opciones) < 4:
            # Generar conjunto aleatorio diferente
            opcion_falsa = self.generar_conjunto(min_elementos=2, max_elementos=7)
            
            # Asegurar que no sea igual a la correcta ni a otras opciones
            if opcion_falsa not in opciones and len(opcion_falsa) > 0:
                opciones.append(opcion_falsa)
        
        # Mezclar opciones
        random.shuffle(opciones)
        
        return {
            "conjunto_a": conjunto_a,
            "conjunto_b": conjunto_b,
            "operacion": operacion,
            "simbolo": simbolo,
            "respuesta_correcta": respuesta_correcta,
            "opciones": opciones
        }


# Funciones auxiliares para dibujar elementos
def dibujar_texto(pantalla, texto, x, y, tamaño, color, centrado=True):
    """
    Dibuja texto en la pantalla
    
    Args:
        pantalla: Surface de pygame donde dibujar
        texto: Texto a mostrar
        x, y: Posicion
        tamaño: Tamaño de la fuente
        color: Color del texto
        centrado: Si True, centra el texto en x, y
    """
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, color)
    
    if centrado:
        rect = superficie_texto.get_rect(center=(x, y))
    else:
        rect = superficie_texto.get_rect(topleft=(x, y))
        
    pantalla.blit(superficie_texto, rect)


def dibujar_conjunto(pantalla, conjunto, x, y, ancho, alto, etiqueta, color_borde):
    """
    Dibuja una caja visual representando un conjunto
    
    Args:
        pantalla: Surface de pygame
        conjunto: Set de elementos a mostrar
        x, y: Posicion de la caja
        ancho, alto: Dimensiones de la caja
        etiqueta: Nombre del conjunto (A, B, etc)
        color_borde: Color del borde de la caja
    """
    # Dibujar fondo blanco
    pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho, alto), border_radius=10)
    
    # Dibujar borde
    pygame.draw.rect(pantalla, color_borde, (x, y, ancho, alto), 3, border_radius=10)
    
    # Dibujar etiqueta del conjunto
    dibujar_texto(pantalla, f"Conjunto {etiqueta}", x + ancho // 2, y + 25, 32, color_borde)
    
    # Convertir conjunto a lista ordenada para mostrar
    elementos = sorted(list(conjunto))
    texto_elementos = "{" + ", ".join(map(str, elementos)) + "}"
    
    # Dibujar elementos
    dibujar_texto(pantalla, texto_elementos, x + ancho // 2, y + 60, 28, (50, 50, 50))


def dibujar_diagrama_venn(pantalla, x, y, conjunto_a, conjunto_b):
    """
    Dibuja un diagrama de Venn simple mostrando dos conjuntos
    
    Args:
        pantalla: Surface de pygame
        x, y: Posicion central del diagrama
        conjunto_a: Primer conjunto
        conjunto_b: Segundo conjunto
    """
    # Colores con transparencia
    color_a = (102, 126, 234)
    color_b = (118, 75, 162)
    
    # Crear surfaces con transparencia
    radio = 80
    superficie_a = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
    superficie_b = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
    
    # Dibujar circulos con transparencia
    pygame.draw.circle(superficie_a, (*color_a, 100), (radio, radio), radio)
    pygame.draw.circle(superficie_b, (*color_b, 100), (radio, radio), radio)
    
    # Posicionar circulos
    pantalla.blit(superficie_a, (x - 50, y - radio))
    pantalla.blit(superficie_b, (x + 50 - radio * 2, y - radio))
    
    # Dibujar bordes de los circulos
    # pygame.draw.circle(pantalla, color_a, (x - 50 + radio, y), radio, 3)
    # pygame.draw.circle(pantalla, color_b, (x + 50 - radio + radio, y), radio, 3)
    
    # Etiquetas A y B
    dibujar_texto(pantalla, "A", x - 70, y, 36, color_a)
    dibujar_texto(pantalla, "B", x + 70, y, 36, color_b)