# Librería principal que vamos a utilizar para desarrollar el proyecto
import pygame
# Para no spammear botones
import time

# Clase personaje
class Personaje():
    # Inicializador, recibe como parametros las posiciones "x" y "y"
    def __init__(self, jugador, x, y, flip, data, sonido, hit_sound):
        self.jugador = jugador
        self.size = data[0]
        # Dirección frontal
        self.flip = flip
        # 0.idle, 1-correr, 2-salto, 3-attack_1, 4-attack_2, 5-golpe, 6-muerto
        self.action = 0
        self.rect = pygame.Rect((x, y, 100, 250))
        self.vel_y = 0
        self.running = False
        self.idle_img = data[1]
        self.idle = data[1]
        self.image = data[1]
        self.running_img = data[2]
        self.attack_1_img = data[3]
        self.attack_2_img = data[4]
        self.jump_img = data[5]
        self.hit_img = data[6]
        self.death_img = data[7] 
        
        # Para no saltar infinitamente
        self.jump = False
        # Para no atacar infinitamente
        self.attacking = False
        self.tipo_ataque = 0
        self.health = 100
        self.attack_cd = 50
        self.hit = False
        self.KO = False
        self.sonido = sonido
        self.hit_sound = hit_sound

        # Para que la imagen de ataque y hit duren mas tiempo
        self.hit_duration = 500
        self.attack_duration = 500
        self.attack_start_time = 0
        self.hit_start_time = 0
    # Función de movimiento
    def movimiento(self, largo, alto, surface, target, round_over):
        VELOCIDAD = 10
        GRAVEDAD = 2
        dx = 0
        dy = 0
        self.running = False
        #self.tipo_ataque = 0

        # Variable que guarda la tecla pulsada
        key = pygame.key.get_pressed()

        # Solo puedo hacer cosas cuando no estoy atacando
        if self.attacking == False and self.KO == False and round_over == False:

            # Controles del jugador 1
            if self.jugador == 1:
                # Movimiento
                if key[pygame.K_a]:
                    dx = -VELOCIDAD
                    self.running = True
                if key[pygame.K_d]:
                    dx = VELOCIDAD
                    self.running = True
                # Saltos
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # Ataques
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.ataque(surface, target)
                    # Diferenciar ataque
                    if key[pygame.K_r]:
                        self.tipo_ataque = 1
                    if key[pygame.K_t]:
                        self.tipo_ataque = 2

            # Controles del jugador 2
            if self.jugador == 2:
                # Movimiento
                if key[pygame.K_LEFT]:
                    dx = -VELOCIDAD
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = VELOCIDAD
                    self.running = True
                # Saltos
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # Ataques
                if key[pygame.K_o] or key[pygame.K_p]:
                    self.ataque(surface, target)
                    # Diferenciar ataque
                    if key[pygame.K_o]:
                        self.tipo_ataque = 1
                    if key[pygame.K_p]:
                        self.tipo_ataque = 2
                    
        # Efecto de la gravedad
        self.vel_y = self.vel_y + GRAVEDAD
        dy = dy + self.vel_y
        

        # Para no salirme de los bordes
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > largo:
            dx = largo - self.rect.right
        if self.rect.bottom + dy > alto - 110:
            self.vel_y = 0
            self.jump = False
            dy = alto - 110 - self.rect.bottom
            
        # Para siempre verme de frente
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # El cd de los ataques
        if self.attack_cd > 0:
            self.attack_cd -= 1

        # Actualizar la posición del personaje
        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy


    # Metodo para actualizar acciones
    def update(self, surface):
        # Ver que acción se esta realizando y ajustar la animación acorde

        if self.health <= 0:
            self.health = 0
            self.KO = True
            self.action = 6
            self.image = self.death_img
        
        elif self.hit == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_start_time <= 300:
                self.image = self.hit_img
            else:
                self.action = 5
        
        elif self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_start_time <= 300 and self.tipo_ataque == 1:
                self.image = self.attack_1_img
            elif current_time - self.attack_start_time <= 300 and self.tipo_ataque == 2:
                self.image = self.attack_2_img
            else:
                self.action = 3
        elif self.jump == True:
            self.action = 2
            self.image = self.jump_img
        
        elif self.running:
            self.action = 1
            self.image = self.running_img
        else:
            self.action = 0
            self.image = self.idle_img

        self.image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # Revisar si personaje esta muerto
        
        if self.action == 3:
            self.action = 0
            self.attacking = False
            self.attack_cd = 50
        if self.action == 5:
            self.action == 0
            self.attacking = False
            self.attack_cd = 50
            self.hit = False
        
    # Metodo para atacar
    def ataque(self, surface, target):
        if self.attack_cd == 0:
            self.attacking = True
            self.sonido.play()
            self.attack_start_time = pygame.time.get_ticks()
            rect_ataque = pygame.Rect(self.rect.centerx - (0.5 * self.rect.width * self.flip), self.rect.y, 0.5 * self.rect.width, self.rect.height)
            if rect_ataque.colliderect(target.rect):
                target.health -= 10
                target.hit = True
                target.hit_start_time = pygame.time.get_ticks()
                target.hit_sound.play()
            #pygame.draw.rect(surface, (0, 255, 0), rect_ataque)
        
    
    # Función para dibujar el personaje sobre la superficie background
    def dibujar(self, surface):
        # Imagen para rotar y verse de frente
        img = pygame.transform.flip(self.idle, self.flip, False)
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
