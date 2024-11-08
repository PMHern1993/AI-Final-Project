import pygame
from .colors import GRAY, YELLOW, GREEN, BLACK, WHITE
from .util import find_center
from .drawable import Drawable

#pygame.font.init()

class Card(Drawable):

	font:pygame.font.Font = pygame.font.SysFont(None, 60)

	def __init__(self):
		self.size = (60,60)
		super().__init__(size=self.size)
		self.bg_color = BLACK
		self.used = False
		self.state = -1
		self.text = ""
		self.colors = [GRAY, YELLOW, GREEN, BLACK]
		self.needs_update = True
		
		
	
	def fill(self):
		self.view.fill(self.colors[self.state])
		if not self.used:
			pygame.draw.rect(self.view, GRAY, (0, 0, *self.size), 2)
		self.needs_update = True
	
	
	def set_text(self, text:str):
		#set instance var
		self.text = text
		self.needs_update = True
	
	def set_state(self, state):
		self.state = state
		self.needs_update = True

	def reset(self):
		self.state = -1
		self.text = ""
		self.used = False
		self.needs_update = True
		

	def draw(self, window:pygame.Surface):
		#clear card
		if self.needs_update:
			self.fill()

			#render text
			text_obj = self.font.render(self.text, True, WHITE)

			#center cyar in card
			font_size = self.font.size(self.text)

			card_cx, card_cy = self.center()
			font_cx, font_cy = find_center(*font_size)

			font_x = card_cx - font_cx
			font_y = card_cy - font_cy

			self.view.blit(text_obj, (font_x, font_y))

			#resets needs_update and draws view to window arg
			#See Drawable for super method
			super().draw(window)

