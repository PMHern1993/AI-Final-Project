import pygame
from .colors import *
from .drawable import Drawable
from .button import ShareButton
from .util import find_center

class SideView(Drawable):

	def __init__(self, size):
		super().__init__(pos=(400,0),size=size)

		self.font = pygame.font.SysFont(None, 33)
		
		self.scoreboard = None
		button_w = 120
		x_pos = (self.size[0]/2) - (button_w/2)
		self.share_button = ShareButton((x_pos, 370), (120, 40))

		self.game_ended = False
		self.is_in_fun_mode = False
	
	def draw_golf_hist(self, offset_y=0):
		text_color = WHITE
		v_w, v_h = find_center(*self.size)
		num_holes = len(self.scoreboard["golf"])
		golf_hist_banner = f"Last {num_holes} holes:"
		ghb_w, ghb_h = self.font.size(golf_hist_banner)
		ghb_text_obj = self.font.render(golf_hist_banner, True, text_color)

		ghb_t_cx, _ = find_center(ghb_w, 2)
		ghb_x = v_w - ghb_t_cx

		hist_str = str(self.scoreboard["golf"])[1:-1]
		gh_w, _ = self.font.size(hist_str)
		gh_text_obj = self.font.render(hist_str, True, text_color)
		
		gh_t_cx, _ = find_center(gh_w, 2)
		gh_x = v_w - gh_t_cx

		self.view.blit(ghb_text_obj, (ghb_x, offset_y))
		self.view.blit(gh_text_obj, (gh_x, offset_y + ghb_h + 10))
	
	def draw_current_score(self, offset_y=0):
		text_color = WHITE
		v_w, v_h = find_center(*self.size)
		golf_score_banner = f"Current hole:"
		gsb_w, gsb_h = self.font.size(golf_score_banner)
		gsb_text_obj = self.font.render(golf_score_banner, True, text_color)

		gsb_t_cx, _ = find_center(gsb_w, 2)
		gsb_x = v_w - gsb_t_cx

		score_str = str(self.scoreboard["score"])
		gs_w, _ = self.font.size(score_str)
		gs_text_obj = self.font.render(score_str, True, text_color)
		
		gs_t_cx, _ = find_center(gs_w, 2)
		gs_x = v_w - gs_t_cx

		self.view.blit(gsb_text_obj, (gsb_x, offset_y))
		self.view.blit(gs_text_obj, (gs_x, offset_y + gsb_h + 10))
	
	def draw_streak(self, offset_y=0):
		text_color = WHITE
		v_w, v_h = find_center(*self.size)
		streak = self.scoreboard["streak"]
		streak_msg = f"Win Streak: {streak}"
		sm_w, sm_h = self.font.size(streak_msg)
		sm_text_obj = self.font.render(streak_msg, True, text_color)

		sm_t_cx, _ = find_center(sm_w, 2)
		sm_x = v_w - sm_t_cx

		self.view.blit(sm_text_obj, (sm_x, offset_y))

	
	def draw_warning(self, offset_y=0):
		text_color = WHITE
		v_w, v_h = find_center(*self.size)
		warning1_msg = "Stats are not recorded"
		warning2_msg = "in Fun Mode"
		w1m_w, _ = self.font.size(warning1_msg)
		w2m_w, _ = self.font.size(warning2_msg)
		w1m_text_obj = self.font.render(warning1_msg, True, text_color)
		w2m_text_obj = self.font.render(warning2_msg, True, text_color)

		w1m_t_cx, _ = find_center(w1m_w, 2)
		w1m_x = v_w - w1m_t_cx

		w2m_t_cx, _ = find_center(w2m_w, 2)
		w2m_x = v_w - w2m_t_cx

		self.view.blit(w1m_text_obj, (w1m_x, offset_y))
		self.view.blit(w2m_text_obj, (w2m_x, offset_y + 30))

	
	def handle_click(self, event:pygame.event.Event, offset=(0,0)):
		x, y = event.pos
		x -= offset[0]

		rect = pygame.Rect(*self.share_button.pos, *self.share_button.size)
		print(rect)
		
		if rect.collidepoint(x, y):
			if self.game_ended:
				self.share_button.handle_event(event, self.pos)

	def draw(self, window:pygame.Surface):
		self.view.fill(BLACK)

		
		offset = 30
		if self.is_in_fun_mode:
			self.draw_warning(offset)
		
		offset = 100
		self.draw_streak(offset)
		offset += 70
		self.draw_golf_hist(offset)
		offset += 100
		self.draw_current_score(offset)
		offset += 100
		if self.game_ended:
			self.share_button.draw(self.view)
		
		super().draw(window)

