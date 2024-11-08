import pygame
from .colors import *
from .util import find_center
from .clickable import Clickable



class OptionsButton(Clickable):
	
	def __init__(self, pos=..., size=...):
		super().__init__(pos, size)
		img = pygame.image.load("wordle\\resources\\gear.png")
		self.view = pygame.transform.scale(img, self.size)
	
	def handle_event(self, event: pygame.event.Event, offset: tuple[int, int] = ...):
		if event.type in self.accepted_events:
			self.actions[event.type]()




class SideViewButton(Clickable):


	def handle_event(self, event: pygame.event.Event, offset: tuple[int, int] = ...):
		if event.type not in self.accepted_events:
			print("Unaccepted event")
			return None
		self.actions[event.type]()

	def draw(self, window: pygame.Surface):
		if self.needs_update:
			x, y = self.pos
			w, h = self.size
			pygame.draw.rect(self.view, LIGHT_GRAY, (0, 0, *self.size))
			pygame.draw.rect(self.view, BLACK, (0, 0, *self.size), 2)

			if self.state == 0:#draw triangle pointing to the right
				pygame.draw.polygon(self.view, WHITE, [(4, 4), ((w - 4), (h/2)), (4, h - 4)])

			if self.state == 1:#draw triangle pointing to the left
				pygame.draw.polygon(self.view, WHITE, [(w - 4, 4), (4, h/2), (w - 4, w - 4)])
			
		window.blit(self.view, self.pos)


class ShareButton(Clickable):


	def handle_event(self, event: pygame.event.Event, offset: tuple[int, int] = ...):
		if event.type in self.accepted_events:
			self.actions[event.type]()

	def draw(self, window: pygame.Surface):
		if self.needs_update:
			self.view.fill(GRAY)
			pygame.draw.rect(self.view, BLACK, (*self.pos, *self.size), 2)
	
			b_cx, b_cy = find_center(*self.size)
			share_font = pygame.font.SysFont(None, self.size[1] - 10)
			share_msg = "Share"
			s_w, s_h = share_font.size(share_msg)
			s_cx, s_cy = find_center(s_w, s_h)
	
			sm_x = b_cx - s_cx
			sm_y = b_cy - s_cy
	
			sm_text_obj = share_font.render(share_msg, True, WHITE)
			self.view.blit(sm_text_obj, (sm_x, sm_y))
	
			super().draw(window)
