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


    @property
    def jugador(self):
        return self._jugador

    @jugador.setter
    def jugador(self, value):
        self._jugador = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def flip(self):
        return self._flip

    @flip.setter
    def flip(self, value):
        self._flip = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def vel_y(self):
        return self._vel_y

    @vel_y.setter
    def vel_y(self, value):
        self._vel_y = value

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    @property
    def idle_img(self):
        return self._idle_img

    @idle_img.setter
    def idle_img(self, value):
        self._idle_img = value

    @property
    def idle(self):
        return self._idle

    @idle.setter
    def idle(self, value):
        self._idle = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def running_img(self):
        return self._running_img

    @running_img.setter
    def running_img(self, value):
        self._running_img = value

    @property
    def attack_1_img(self):
        return self._attack_1_img

    @attack_1_img.setter
    def attack_1_img(self, value):
        self._attack_1_img = value

    @property
    def attack_2_img(self):
        return self._attack_2_img

    @attack_2_img.setter
    def attack_2_img(self, value):
        self._attack_2_img = value

    @property
    def jump_img(self):
        return self._jump_img

    @jump_img.setter
    def jump_img(self, value):
        self._jump_img = value

    @property
    def hit_img(self):
        return self._hit_img

    @hit_img.setter
    def hit_img(self, value):
        self._hit_img = value

    @property
    def death_img(self):
        return self._death_img

    @death_img.setter
    def death_img(self, value):
        self._death_img = value

    @property
    def jump(self):
        return self._jump

    @jump.setter
    def jump(self, value):
        self._jump = value

    @property
    def attacking(self):
        return self._attacking

    @attacking.setter
    def attacking(self, value):
        self._attacking = value

    @property
    def tipo_ataque(self):
        return self._tipo_ataque

    @tipo_ataque.setter
    def tipo_ataque(self, value):
        self._tipo_ataque = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def attack_cd(self):
        return self._attack_cd

    @attack_cd.setter
    def attack_cd(self, value):
        self._attack_cd = value

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

    @property
    def KO(self):
        return self._KO

    @KO.setter
    def KO(self, value):
        self._KO = value

    @property
    def sonido(self):
        return self._sonido

    @sonido.setter
    def sonido(self, value):
        self._sonido = value

    @property
    def hit_sound(self):
        return self._hit_sound

    @hit_sound.setter
    def hit_sound(self, value):
        self._hit_sound = value

    @property
    def hit_duration(self):
        return self._hit_duration

    @hit_duration.setter
    def hit_duration(self, value):
        self._hit_duration = value

    @property
    def attack_duration(self):
        return self._attack_duration

    @attack_duration.setter
    def attack_duration(self, value):
        self._attack_duration = value

    @property
    def attack_start_time(self):
        return self._attack_start_time

    @attack_start_time.setter
    def attack_start_time(self, value):
        self._attack_start_time = value

    @property
    def hit_start_time(self):
        return self._hit_start_time

    @hit_start_time.setter
    def hit_start_time(self, value):
        self._hit_start_time = value




        
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
        
