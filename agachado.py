import pygame
import random
import sys

import pygame.display

# Constant
PASO_X = 10
JUMP_HEIGHT = 100
JUMP_STEPS = 100
COLISION_DIST = 45

class Personaje:
    def __init__(self, id, nombre, x, y, estado="Vivo"):
        self.id = id
        self.nombre = nombre
        self.posicionX = x
        self.posicionY = y
        self.estado = estado

    def mover(self, dx=0, dy=0):
        self.posicionX += dx
        self.posicionY += dy

class Jugador(Personaje):
    def __init__(self, id, nombre, x=0, y=0):
        super().__init__(id, nombre, x, y)
        self.vidas = 3
        self.monedas = 0
        self.puntos = 0
        self.tiempo = 300
        self.dispara = False
        self.tamanio = 50
        self.imagen_actual = None
        self.saltando = False
        self.altura_salto = 0
        self.velocidad_salto =0
        self.gravedad = 1
        self.suelo = True
        self.direccion = "derecha"
        self.estado = False
        self.tiempo_estado = 700
        self.duracion = 15000
        self.imagen_original = None
        

class Enemigo(Personaje):
    def __init__(self, id, nombre, x=0, y=0):
        super().__init__(id, nombre, x, y)
        self.direccion = -1

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MARIO FROM TEMU")
        self.ancho, self.alto = 800, 600
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        self.reloj = pygame.time.Clock()

        self.imgs = self.load_images()

        self.players = []
        self.enemigos = []
        self.hongos = []

        self.spawn_interval = 5000  # tiempo de aparación
        self.last_spawn_time = pygame.time.get_ticks()

        self.font = pygame.font.SysFont("Arial", 18)
        self.game_over_flag = False

        self.jugador = Jugador(1, "Jugador1", self.ancho // 2, self.alto // 1.245)
        self.jugador.imagen_actual = self.imgs["der_inicial"]
        self.players.append(self.jugador)

        self.spawn_hongos()

    def load_images(self):
        try:
            imgs = {
                "fondo": pygame.transform.scale(pygame.image.load("assets/fondo.png"), (self.ancho, self.alto)),
                "izquierda": pygame.transform.scale(pygame.image.load("assets/2i.png"), (50, 50)),
                "derecha": pygame.transform.scale(pygame.image.load("assets/2.png"), (50, 50)),
                "arriba": pygame.transform.scale(pygame.image.load("assets/5.png"), (50, 50)),
                "arriba_izq": pygame.transform.scale(pygame.image.load("assets/5i.png"), (50, 50)),
                "abajo": pygame.transform.scale(pygame.image.load("assets/4.png"), (50,50)),
                "abajo_izq": pygame.transform.scale(pygame.image.load("assets/4i.png"), (50,50)),
                "der_inicial": pygame.transform.scale(pygame.image.load("assets/1.png"), (50,50)),
                "izq_inicial": pygame.transform.scale(pygame.image.load("assets/1i.png"), (50,50)),
                "hongo": pygame.transform.scale(pygame.image.load("assets/hongo_rojo.png"), (30, 30)),
                "hongoVida": pygame.transform.scale(pygame.image.load("assets/hongo_verde.png"), (30, 30)),
                "enemy1": pygame.transform.scale(pygame.image.load("assets/enemy1.png"), (50,50)),
                "enemy0": pygame.transform.scale(pygame.image.load("assets/enemy0.png"), (50, 50)),
                "star": pygame.transform.scale(pygame.image.load("assets/estrella.png"), (40,40)),
                "coin": pygame.transform.scale(pygame.image.load("assets/coin.png"), (30, 30))
            }
            return imgs
        except Exception as e:
            print("Error al cargar imágenes:", e)
            sys.exit()

    def incremento_imgs(self, tamano):
        self.imgs["der_inicial"] = pygame.transform.scale(pygame.image.load("assets/1.png"), (tamano, tamano))
        self.imgs["izq_inicial"] = pygame.transform.scale(pygame.image.load("assets/1i.png"), (tamano, tamano))
        self.imgs["derecha"] = pygame.transform.scale(pygame.image.load("assets/2.png"), (tamano, tamano))
        self.imgs["izquierda"] = pygame.transform.scale(pygame.image.load("assets/2i.png"), (tamano, tamano))
        self.imgs["arriba"] = pygame.transform.scale(pygame.image.load("assets/5.png"), (tamano, tamano))
        self.imgs["arriba_izq"] = pygame.transform.scale(pygame.image.load("assets/5i.png"), (tamano, tamano))
        self.imgs["abajo"] = pygame.transform.scale(pygame.image.load("assets/4.png"), (tamano, tamano))
        self.imgs["abajo_izq"] = pygame.transform.scale(pygame.image.load("assets/4i.png"), (tamano, tamano))
    
    def spawn_hongos(self):
        y = self.jugador.posicionY
        for tipo in ["hongo", "hongoVida"]:
            x = random.randint(50, self.ancho - 50)
            self.hongos.append({"tipo": tipo, "x": x, "y": y})

    def spawn_enemy(self):
        y = self.alto // 1.295

        enemigo = Enemigo(len(self.enemigos) + 2, "Enemigo", self.ancho, y)
        self.enemigos.append(enemigo)

    def check_collisions(self):
        jugador = self.jugador
        for enemigo in self.enemigos[:]: #COLISION CON EL ENEMIGO
            dx = abs(jugador.posicionX - enemigo.posicionX)
            dy = abs(jugador.posicionY - enemigo.posicionY)
            if dx < COLISION_DIST and dy < COLISION_DIST:
                if jugador.estado: #ESTADO Y ENEMIGO
                    self.enemigos.remove(enemigo)
                else:
                    if not jugador.saltando:
                        jugador.vidas -= 1
                        if jugador.vidas <= 0:
                            self.game_over_flag = True
                        self.enemigos.remove(enemigo)


        for hongo in self.hongos[:]: # COLISON CON HONGOS
            dx = abs(jugador.posicionX - hongo["x"])
            dy = abs(jugador.posicionY - hongo["y"])
            if dx < COLISION_DIST and dy < COLISION_DIST:
                if hongo["tipo"] == "hongoVida":
                    jugador.vidas += 1
                elif hongo["tipo"] == "hongo":
                    if not jugador.estado:
                        jugador.tamanio = 80
                        jugador.estado = True
                        jugador.tiempo_estado = pygame.time.get_ticks()
                        self.incremento_imgs(jugador.tamanio)

                        if jugador.direccion == "derecha":
                            jugador.imagen_original = self.imgs["der_inicial"]
                        else:
                            jugador.imagen_original = self.imgs["izq_inicial"]                        
                self.hongos.remove(hongo)

    def draw_text(self, text, x, y):
        render = self.font.render(text, True, (0, 0, 0))
        self.ventana.blit(render, (x, y))

    def draw(self):
        self.ventana.blit(self.imgs["fondo"],(0,0))

# DIBUJAR AL JUGADOR
        jugador = self.jugador
        self.ventana.blit(jugador.imagen_actual, (jugador.posicionX, jugador.posicionY))

#DIBUJAR ENEMY
        for enemigo in self.enemigos:
            self.ventana.blit(self.imgs["enemy1"], (enemigo.posicionX, enemigo.posicionY))

#DIBUJAR HONGOS
        for hongo in self.hongos:
            self.ventana.blit(self.imgs[hongo["tipo"]], (hongo["x"], hongo["y"]))

#STATS
        self.draw_text(f"Vidas: {jugador.vidas}", 10, 10)
        self.draw_text(f"Puntos: {jugador.puntos}", 10, 30)
        self.draw_text(f"Tamaño: {jugador.tamanio}", 10, 50)
        self.draw_text(f"Posición: {jugador.posicionX, jugador.posicionY}", 10, 70)

        if self.game_over_flag:
            over_text = pygame.font.SysFont("Arial", 48).render("GAME OVER", True, (255, 0, 0))
            self.ventana.blit(over_text, (self.ancho // 2 - 120, self.alto // 2 - 50))

        pygame.display.flip()

    def update(self):
        keys = pygame.key.get_pressed()
        jugador = self.jugador
        jugador.velocidad_salto += jugador.gravedad
        jugador.mover(dy=jugador.velocidad_salto)
        suelo_coordy = self.get_suelo_y()


        if keys[pygame.K_RIGHT]:
                jugador.imagen_actual = self.imgs["derecha"]
                jugador.direccion = "derecha"
                jugador.mover(dx=PASO_X)
        elif keys[pygame.K_LEFT]:
                jugador.imagen_actual = self.imgs["izquierda"]
                jugador.direccion = "izquierda"
                jugador.mover(dx=-PASO_X)
        elif keys[pygame.K_DOWN]: #
            jugador.suelo = True
            if jugador.direccion == "derecha":
                jugador.imagen_actual = self.imgs["abajo"]
            elif jugador.direccion == "izquierda":
                jugador.imagen_actual = self.imgs["abajo_izq"]
        elif keys[pygame.K_UP] and jugador.suelo: # SALTO DEL JUGADOR
            jugador.velocidad_salto = -15
            jugador.suelo = False
            if jugador. direccion == "derecha":
                jugador.imagen_actual = self.imgs["arriba"]
            else:
                jugador.imagen_actual = self.imgs ["arriba_izq"]

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] and jugador.suelo:
            if jugador.estado:  #
                if jugador.direccion == "derecha":
                    jugador.imagen_original = self.imgs["der_inicial"]
                    jugador.imagen_actual = pygame.transform.scale(jugador.imagen_original, (80, 80))
                elif jugador.direccion == "izquierda":
                    jugador.imagen_original = self.imgs["izq_inicial"]
                    jugador.imagen_actual = pygame.transform.scale(jugador.imagen_original, (80, 80))
            else:  #SINO
                if jugador.direccion == "derecha":
                    jugador.imagen_actual = self.imgs["der_inicial"]
                elif jugador.direccion == "izquierda":
                    jugador.imagen_actual = self.imgs["izq_inicial"]

        if not jugador.suelo:
            jugador.velocidad_salto += jugador.gravedad
            jugador.mover(dy=jugador.velocidad_salto)

            if jugador.posicionY >= suelo_coordy:
                jugador.posicionY = suelo_coordy
                jugador.velocidad_salto = 0
                jugador.suelo = True
        else:
            jugador.posicionY = suelo_coordy
        
        # MOVER ENEMY
        for enemigo in self.enemigos:
            enemigo.mover(dx=3 * enemigo.direccion)
            if enemigo.posicionX < 0 or enemigo.posicionX > self.ancho:
                enemigo.direccion *= -1

        # COMPROBARLAS COLISIONES
        self.check_collisions()

        # enemigos por tiempo suelo coordy
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.last_spawn_time > self.spawn_interval:
            if len(self.enemigos) < 2:
                self.spawn_enemy()
            self.last_spawn_time = tiempo_actual

        if jugador.posicionX <= -100:
            jugador.posicionX = self.ancho
        elif jugador.posicionX >= self.ancho + 50:
            jugador.posicionX = -50


        if jugador.estado:
            tiempo = pygame.time.get_ticks()
            if tiempo - jugador.tiempo_estado > jugador.duracion:
                jugador.estado = False
                jugador.tamanio = 50
                self.incremento_imgs(jugador.tamanio)
                if jugador.direccion == "derecha":
                    jugador.imagen_actual = self.imgs["der_inicial"]
                else:
                    jugador.imagen_actual = self.imgs["izq_inicial"]
    
    def get_suelo_y(self):
        return self.alto // 1.3 - (self.jugador.tamanio - 50)

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.flip()

            if not self.game_over_flag:
                self.update()
            self.draw()
            self.reloj.tick(30)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = Game()
    juego.run()
