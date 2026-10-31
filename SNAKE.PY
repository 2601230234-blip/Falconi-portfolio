import pygame
import random
import sys

# --- Configuración ---
ANCHO, ALTO = 640, 480
TAM_CELDA = 20
COLUMNAS = ANCHO // TAM_CELDA
FILAS = ALTO // TAM_CELDA
FPS = 5

BLANCO = (255,255,255)
NEGRO = (0,0,0)
VERDE = (0,200,0)
VERDE_CLARO = (50,255,50)
ROJO = (255,50,50)

# Inicialización Pygame - módulos clave
pygame.init()  # Inicializa todos los módulos
pygame.mixer.init() # Módulo mixer para sonido
screen = pygame.display.set_mode((ANCHO, ALTO)) # pygame.display
pygame.display.set_caption("Snake Pygame - Prototipo")
clock = pygame.time.Clock() # pygame.time
font = pygame.font.SysFont("Arial", 24) # pygame.font

# Sonidos simples generados (evita archivos externos)
def crear_sonido(frec=440, dur=100):
    # Genera beep simple si no hay archivos wav
    try:
        sample_rate = 22050
        n_samples = int(sample_rate * dur / 1000)
        buf = bytearray()
        # sonido dummy
        return None
    except:
        return None

class Food:
    """Usa pygame.sprite conceptual + pygame.image/draw"""
    def __init__(self, snake_body):
        self.reposicionar(snake_body)
    
    def reposicionar(self, snake_body):
        while True:
            self.x = random.randint(0, COLUMNAS-1)
            self.y = random.randint(0, FILAS-1)
            if (self.x, self.y) not in snake_body:
                break
            # Evita spawn sobre cuerpo (Pruebas y Optimización)
    
    def draw(self):
        rect = pygame.Rect(self.x*TAM_CELDA, self.y*TAM_CELDA, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(screen, ROJO, rect, border_radius=6) # pygame.draw

class Snake:
    def __init__(self):
        self.body = [(COLUMNAS//2, FILAS//2)]
        self.dir = (1,0) # derecha
        self.next_dir = (1,0)
        self.crecer = False

    def cambiar_dir(self, nueva):
        # Bloquea dirección opuesta (error común solucionado)
        if (nueva[0]*-1, nueva[1]*-1) != self.dir:
            self.next_dir = nueva

    def update(self):
        self.dir = self.next_dir
        cabeza = self.body[0]
        nueva_cabeza = (cabeza[0]+self.dir[0], cabeza[1]+self.dir[1])
        
        # Colisión paredes
        if not (0 <= nueva_cabeza[0] < COLUMNAS and 0 <= nueva_cabeza[1] < FILAS):
            return False # Game Over
        # Colisión consigo mismo
        if nueva_cabeza in self.body:
            return False
        
        self.body.insert(0, nueva_cabeza)
        if not self.crecer:
            self.body.pop()
        else:
            self.crecer = False
        return True

    def draw(self):
        for i, (x,y) in enumerate(self.body):
            rect = pygame.Rect(x*TAM_CELDA, y*TAM_CELDA, TAM_CELDA-2, TAM_CELDA-2)
            color = VERDE_CLARO if i==0 else VERDE
            pygame.draw.rect(screen, color, rect, border_radius=4)

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0
    running = True

    # --- Game Loop Principal ---
    while running:
        # 1. Manejo de eventos - pygame.event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    snake.cambiar_dir((0,-1))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.cambiar_dir((0,1))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.cambiar_dir((-1,0))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.cambiar_dir((1,0))

        # 2. Lógica / Update
        vivo = snake.update()
        if not vivo:
            running = False
            break
        
        # 3. Colisiones - rect.colliderect conceptual
        if snake.body[0] == (food.x, food.y):
            snake.crecer = True
            score += 10
            food.reposicionar(snake.body)
            # pygame.mixer.Sound.play() aquí si tuvieras wav

        # 4. Render
        screen.fill(NEGRO) # Limpia pantalla
        snake.draw() # Sprites
        food.draw()
        
        # Texto - pygame.font
        txt = font.render(f"Score: {score}", True, BLANCO)
        screen.blit(txt, (10,10)) # blit

        # 5. Flip y Framerate - doble buffering
        pygame.display.flip() # actualiza toda la pantalla
        clock.tick(FPS) # limita FPS - evita consumo CPU excesivo

    # Game Over
    screen.fill(NEGRO)
    over = font.render(f"GAME OVER - Score {score} - Presiona ESC", True, BLANCO)
    screen.blit(over, (ANCHO//2-180, ALTO//2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE):
                esperando=False
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()