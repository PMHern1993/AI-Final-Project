import pygame
from .drawable import Drawable


class Clickable(Drawable):

	
	def __init__(self, pos=(0,0), size=(0,0)):
		super().__init__(pos, size)
		self.accepted_events = (pygame.MOUSEBUTTONDOWN,)
		test = lambda:"Test"
		self.actions = {event_type:test for event_type in self.accepted_events}
		self.state = 0
	
	def set_state(self, state):
		self.state = state
	
	def set_action(self, action, event_type):
		self.actions[event_type] = action
	
	def handle_event(self, event:pygame.event.Event, offset:tuple[int, int]=(0,0)):
		raise NotImplementedError()
		
			
	





