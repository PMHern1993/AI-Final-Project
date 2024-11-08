import pygame

class Drawable:

	def __init__(self, pos=(0,0), size=(0,0)):
		self.pos = pos
		self.size = size
		self.view = pygame.Surface(self.size)
		self.needs_update = True
	
	def set_pos(self, pos):
		self.pos = pos
		self.needs_update = True
	
	def set_size(self, size):
		self.size = size
		self.view = pygame.Surface(self.size)
		self.needs_update = True
	
	def center(self):
		w, h = self.size
		return (w/2, h/2)
	
	def center_in(self, view:"Drawable"):
		v_cx, v_cy = view.center()
		s_cx, s_cy = self.center()
		x = v_cx - s_cx
		y = v_cy - s_cy
		self.pos = (x, y)

	def draw(self, window:pygame.Surface):
		if self.needs_update:
			#self.needs_update = False
			window.blit(self.view, self.pos)



