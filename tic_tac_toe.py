# figures_pygame.py
# -*- coding: utf-8 -*-

'''
Tres en raya (Tic tac toe)

Para 1 o 2 jugadores
'''

# Módulos
import pygame
import sys
import random

pygame.init()

# Constantes
ANCHO, ALTO = 600, 650
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tres en raya")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (150, 150, 150)
ROJO = (200, 0, 0)
AZUL = (0, 0, 200)

FUENTE = pygame.font.SysFont(None, 80)
FUENTE_MED = pygame.font.SysFont(None, 50)
FUENTE_PEQUE = pygame.font.SysFont(None, 40)

TAM_CELDA = ANCHO // 3
ANCHO_LINEA = 8

# Estado del juego
tablero = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]

jugador_actual = 1
juego_terminado = False
ganador = 0
modo = None   # "1P" o "2P"

# Puntuación (inicial)
puntos_p1 = 0
puntos_p2 = 0


# Tablero
def dibujar_tablero():
    VENTANA.fill(BLANCO)

    # Ubicación del marcador
    marcador = FUENTE_PEQUE.render(
        f"Jugador 1: {puntos_p1}   |   Jugador 2: {puntos_p2}",
        True, NEGRO
    )
    VENTANA.blit(marcador, (20, 10))

    # Líneas verticales
    pygame.draw.line(VENTANA, NEGRO, (TAM_CELDA, 50), (TAM_CELDA, ALTO), ANCHO_LINEA)
    pygame.draw.line(VENTANA, NEGRO, (2 * TAM_CELDA, 50), (2 * TAM_CELDA, ALTO), ANCHO_LINEA)

    # Líneas horizontales
    pygame.draw.line(VENTANA, NEGRO, (0, TAM_CELDA + 50), (ANCHO, TAM_CELDA + 50), ANCHO_LINEA)
    pygame.draw.line(VENTANA, NEGRO, (0, 2 * TAM_CELDA + 50), (ANCHO, 2 * TAM_CELDA + 50), ANCHO_LINEA)

    # Fichas
    for fila in range(3):
        for col in range(3):
            x = col * TAM_CELDA + TAM_CELDA // 2
            y = fila * TAM_CELDA + TAM_CELDA // 2 + 50

            if tablero[fila][col] == 1:
                dibujar_x(x, y)
            elif tablero[fila][col] == 2:
                dibujar_o(x, y)

# Dibujar X
def dibujar_x(x, y):
    offset = TAM_CELDA // 3
    pygame.draw.line(VENTANA, ROJO, (x - offset, y - offset), (x + offset, y + offset), ANCHO_LINEA)
    pygame.draw.line(VENTANA, ROJO, (x + offset, y - offset), (x - offset, y + offset), ANCHO_LINEA)

# Dibujar O
def dibujar_o(x, y):
    radio = TAM_CELDA // 3
    pygame.draw.circle(VENTANA, AZUL, (x, y), radio, ANCHO_LINEA)

# Comprobación del ganador
def comprobar_ganador():
    # Filas
    for fila in range(3):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] != 0:
            return tablero[fila][0]

    # Columnas
    for col in range(3):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] != 0:
            return tablero[0][col]

    # Diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != 0:
        return tablero[0][0]

    if tablero[0][2] == tablero[1][1] == tablero[2][0] != 0:
        return tablero[0][2]

    return 0

# Tablero lleno
def tablero_lleno():
    return all(0 not in fila for fila in tablero)

# Reiniciar
def reiniciar_tablero():
    global tablero, jugador_actual, juego_terminado, ganador
    tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    jugador_actual = 1
    juego_terminado = False
    ganador = 0

# Jugador-Ordenador-IA
def ia_juega():
    libres = [(f, c) for f in range(3) for c in range(3) if tablero[f][c] == 0]
    if libres:
        f, c = random.choice(libres)
        tablero[f][c] = 2

# Menú
def boton(texto, y):
    rect = pygame.Rect(150, y, 300, 80)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    color = GRIS_OSCURO if rect.collidepoint(mouse) else GRIS
    pygame.draw.rect(VENTANA, color, rect, border_radius=10)

    txt = FUENTE_MED.render(texto, True, NEGRO)
    VENTANA.blit(txt, txt.get_rect(center=rect.center))

    if rect.collidepoint(mouse) and click:
        pygame.time.wait(200)
        return True
    return False

# Inicio
def menu_inicial():
    while True:
        VENTANA.fill(BLANCO)
        titulo = FUENTE.render("Tres en Raya", True, NEGRO)
        VENTANA.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 120)))

        if boton("1 Jugador", 250):
            return "1P"
        if boton("2 Jugadores", 350):
            return "2P"
        if boton("Salir", 450):
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


# Principal
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    # Menú inicial
    if modo is None:
        reiniciar_tablero()
        puntos_p1 = 0
        puntos_p2 = 0
        modo = menu_inicial()
        continue

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar_tablero()  # mantiene el modo
            if evento.key == pygame.K_ESCAPE:
                modo = None  # volver al menú

        if evento.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
            x, y = pygame.mouse.get_pos()
            if y < 50:
                continue

            col = x // TAM_CELDA
            fila = (y - 50) // TAM_CELDA

            if tablero[fila][col] == 0:
                tablero[fila][col] = jugador_actual
                ganador = comprobar_ganador()

                if ganador != 0:
                    juego_terminado = True
                    if ganador == 1:
                        puntos_p1 += 1
                    else:
                        puntos_p2 += 1

                elif tablero_lleno():
                    juego_terminado = True

                else:
                    jugador_actual = 2 if jugador_actual == 1 else 1

                # Ordenador-IA juega
                if modo == "1P" and jugador_actual == 2 and not juego_terminado:
                    ia_juega()
                    ganador = comprobar_ganador()

                    if ganador != 0:
                        juego_terminado = True
                        puntos_p2 += 1

                    elif tablero_lleno():
                        juego_terminado = True

                    jugador_actual = 1

    # Dibujar tablero
    dibujar_tablero()

    # Mensaje final
    if juego_terminado:
        cuadro_ancho = 450
        cuadro_alto = 180
        cuadro_x = (ANCHO - cuadro_ancho) // 2
        cuadro_y = (ALTO - cuadro_alto) // 2

        pygame.draw.rect(VENTANA, GRIS, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), border_radius=15)
        pygame.draw.rect(VENTANA, GRIS_OSCURO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 4, border_radius=15)

        # Resultado
        if ganador == 1:
            msg = "¡Gana Jugador 1!"
        elif ganador == 2:
            msg = "¡Gana Jugador 2!"
        else:
            msg = "¡Empate!"

        texto = FUENTE.render(msg, True, NEGRO)
        VENTANA.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 20)))

        # Texto
        reinicio = FUENTE_MED.render("R = Reiniciar | ESC = Menú", True, NEGRO)
        VENTANA.blit(reinicio, reinicio.get_rect(center=(ANCHO // 2, ALTO // 2 + 50)))


    pygame.display.flip()
