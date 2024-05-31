# Librería principal que vamos a utilizar para desarrollar el proyecto
import pygame

# Para trabajar con sonido
from pygame import mixer
# Del modulo personaje necesitamos la clase Personaje
from personaje import Personaje

# Inicializando pygame y mixer
mixer.init()
pygame.init()

# Crear una ventana
# Se crea una ventana, especificando el largo y alto
LARGO = 1000
ALTO = 600

# Variable screen, la cual utiliza una función de pygame que recibe como
# parametros el ancho y largo específicados anteriormente
screen = pygame.display.set_mode((LARGO, ALTO))

# Etiqueta de la ventana, utilizando una función de pygame
pygame.display.set_caption("Tico Fighter")

# Establecer tasa de refresco (framerate)
clock = pygame.time.Clock()
FPS = 60

# Colores
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# Variables del juego
conteo_inicial = 3
ultima_actualizacion_conteo = pygame.time.get_ticks()
puntaje = [0, 0]
round_over = False
round_over_cd = 2000



# Data de los personajes

HEROE_TAMAÑO = 250

HEROE_idle=pygame.image.load("assets/images/hero/idle.png").convert_alpha()
H_idle = pygame.transform.scale(HEROE_idle, (100, 250))

HEROE_running=pygame.image.load("assets/images/hero/running.png").convert_alpha()
H_running = pygame.transform.scale(HEROE_running, (100, 250))

HEROE_attack_1=pygame.image.load("assets/images/hero/attack_1.png").convert_alpha()
H_attack_1 = pygame.transform.scale(HEROE_attack_1, (100, 250))

HEROE_attack_2=pygame.image.load("assets/images/hero/attack_2.png").convert_alpha()
H_attack_2 = pygame.transform.scale(HEROE_attack_2, (100, 250))

HEROE_jump=pygame.image.load("assets/images/hero/jump.png").convert_alpha()
H_jump = pygame.transform.scale(HEROE_jump, (100, 250))

HEROE_hit=pygame.image.load("assets/images/hero/hit.png").convert_alpha()
H_hit = pygame.transform.scale(HEROE_hit, (100, 250))

HEROE_death=pygame.image.load("assets/images/hero/death.png").convert_alpha()
H_death = pygame.transform.scale(HEROE_death, (100, 250))


HEROE_DATA = [HEROE_TAMAÑO, H_idle, H_running, H_attack_1, H_attack_2, H_jump, H_hit, H_death]

############

VILLANO_TAMAÑO = 250

VILLANO_idle=pygame.image.load("assets/images/villain/idle.png").convert_alpha()
V_idle = pygame.transform.scale(VILLANO_idle, (100, 250))

VILLANO_running=pygame.image.load("assets/images/villain/running.png").convert_alpha()
V_running = pygame.transform.scale(VILLANO_running, (100, 250))

VILLANO_attack_1=pygame.image.load("assets/images/villain/attack_1.png").convert_alpha()
V_attack_1 = pygame.transform.scale(VILLANO_attack_1, (100, 250))

VILLANO_attack_2=pygame.image.load("assets/images/villain/attack_2.png").convert_alpha()
V_attack_2 = pygame.transform.scale(VILLANO_attack_2, (100, 250))

VILLANO_jump=pygame.image.load("assets/images/villain/jump.png").convert_alpha()
V_jump = pygame.transform.scale(VILLANO_jump, (100, 250))

VILLANO_hit=pygame.image.load("assets/images/villain/hit.png").convert_alpha()
V_hit = pygame.transform.scale(VILLANO_hit, (100, 250))

VILLANO_death=pygame.image.load("assets/images/villain/death.png").convert_alpha()
V_death = pygame.transform.scale(VILLANO_death, (100, 250))


VILLANO_DATA = [VILLANO_TAMAÑO, V_idle, V_running, V_attack_1, V_attack_2, V_jump, V_hit, V_death]


# Cargar musica y sonidos
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)
round_music = pygame.mixer.Sound("assets/audio/round.mp3")
punch = pygame.mixer.Sound("assets/audio/punch.mp3")
slash = pygame.mixer.Sound("assets/audio/slash.mp3")
hit_1 = pygame.mixer.Sound("assets/audio/hit1.mp3")
hit_2 = pygame.mixer.Sound("assets/audio/hit2.mp3")


# Cargar el background, establecemos una variable para el background
bg_img = pygame.image.load("assets/images/background/background1.jpg").convert_alpha()

# Cargar imagen de victoria
victoria_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Definir la fuente
font = pygame.font.Font(None, 80)

# Funcion para escribir texto
def dibujar_texto(texto, font, color, x, y):
    img = font.render(texto, True, color)
    screen.blit(img, (x,y))


# Función para dibujar el background
def dibujar_bg():
    # Resize del background al tamaño de la ventana
    bg_escalado = pygame.transform.scale(bg_img, (LARGO, ALTO))
    screen.blit(bg_escalado, (0, 0))

# Funcion para barras de vida
def dibujar_vida(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLANCO, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, ROJO, (x, y, 400, 30))
    pygame.draw.rect(screen, VERDE, (x, y, 400 * ratio, 30))

# Crear dos objetos tipo Personaje
personaje_1 = Personaje(1, 200, 240, False, HEROE_DATA, punch, hit_1) 
personaje_2 = Personaje(2, 700, 240, True, VILLANO_DATA, slash, hit_2)

# Bucle del juego, para que se mantenga corriendo
run = True
while run:

    clock.tick(FPS)

    # Dibujar background
    dibujar_bg()

    # Dibujar vida y puntajes
    dibujar_vida(personaje_1.health, 20, 20)
    dibujar_vida(personaje_2.health, 580, 20)
    dibujar_texto("P1: " + str(puntaje[0]), font, ROJO, 20, 60)
    dibujar_texto("P2: " + str(puntaje[1]), font, ROJO, 580, 60)
    if conteo_inicial <= 0:
        # Mover los personajes
        
        personaje_1.movimiento(LARGO, ALTO, screen, personaje_2, round_over)
        personaje_2.movimiento(LARGO, ALTO, screen, personaje_1, round_over)

    else:
        round_music.play()
        # Mostrar el contador
        dibujar_texto(str(conteo_inicial), font, ROJO, LARGO / 2, ALTO / 3 )
        # Actualizar el conteo
        if (pygame.time.get_ticks() - ultima_actualizacion_conteo) >= 1000:
            conteo_inicial -= 1
            ultima_actualizacion_conteo = pygame.time.get_ticks()

    # Actualizar personajes
    personaje_1.update(screen)
    personaje_2.update(screen)

    # Dibujar personajes
    personaje_1.dibujar(screen)
    personaje_2.dibujar(screen)

    # Revisar si hay KO
    if round_over == False:
        if personaje_1.KO == True:
            puntaje[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        if personaje_2.KO == True:
            puntaje[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victoria_img, (230, 50))
        if pygame.time.get_ticks() - round_over_time > round_over_cd:
            round_over = False
            contador_inicial = 3
            personaje_1 = Personaje(1, 200, 310, False, HEROE_DATA, punch, hit_1) 
            personaje_2 = Personaje(2, 700, 310, True, VILLANO_DATA, slash, hit_2)
    
    # Manager de Eventos
    for event in pygame.event.get():

        # Este evento me permite salir del bucle
        if event.type == pygame.QUIT:
            run = False

    # Actualizar pantalla
    pygame.display.update()


# Cerrar la ventana que se creo
pygame.quit()
