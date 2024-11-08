from tkinter import font
import pygame
from .drawable import Drawable
from .colors import BLACK, YELLOW, GREEN, GRAY, WHITE
from .util import find_center

class Key(Drawable):

	font:pygame.font.Font = pygame.font.SysFont("System1", 25)

	def __init__(self, letter:str, size=(30,40)):
		self.size = size
		super().__init__(size=self.size)
		self.pos = (0,0)
		self.state = -1
		self.letter = letter
		self.colors = [BLACK, YELLOW, GREEN, GRAY]
		self.bg_color = GRAY
		self.text_color = WHITE
	
	def set_state(self, state):
		self.state = state
		self.bg_color = self.colors[self.state]
		self.text_color = WHITE
		if self.state == 0:
			self.text_color = GRAY
		self.needs_update = True
			



	def draw(self, window:pygame.Surface):
		if self.needs_update:
			#self.bbox = pygame.draw.rect(self, self.bg_color, (0,0,*self.size),0,4)
			pygame.draw.rect(self.view, self.bg_color, (0,0,*self.size),0,4)

			text_obj = self.font.render(self.letter, True, self.text_color)

			#center char in card
			font_size = self.font.size(self.letter)

			key_cx, key_cy = self.center()
			font_cx, font_cy = find_center(*font_size)

			font_x = key_cx - font_cx
			font_y = key_cy - font_cy

			#drax to card
			self.view.blit(text_obj, (font_x, font_y))

			#resets needs_update and draws view to window arg
			#See Drawable for super method
			super().draw(window)
	

	
	def __str__(self):
		return self.letter

