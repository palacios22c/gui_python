# figures_pygame.py
# -*- coding: utf-8 -*-

'''
Canvas simple

Figuras incluidas: un rectángulo, un círculo y dos triángulos
'''

# Módulos
import pygame
import sys

# Inicio
pygame.init()

# Valores elegidos para el tamaño
w, h = 250, 250

# Lista de colores
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
magenta = (255,0,255)
white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Figures')											# Título de la ventana
screen.fill(white)																# Color de fondo: blanco

pygame.draw.rect(screen, black, (w/4,h/4,w/2,h/2))								# Rectángulo negro
pygame.draw.circle(screen, yellow, (int(w/2), int(h/2)), int(min(w,h)/4))		# Círculo amarillo
pygame.draw.polygon(screen, green, [[w/4, h/4], [w/2, h/2], [w/4, h*3/4]])		# Triángulo verde
pygame.draw.polygon(screen, red, [[w*3/4, h/4], [w/2, h/2], [w*3/4, h*3/4]], 2)	# Triángulo con línea roja de grosor 2


pygame.display.update()

# Finalización
while (True):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
