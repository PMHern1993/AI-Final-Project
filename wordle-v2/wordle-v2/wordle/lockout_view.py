import pygame
from .drawable import Drawable
from .util import find_center
from .colors import BLACK, WHITE


class Lockout(Drawable):

	font:pygame.font.Font = pygame.font.SysFont("System1", 40)

	def draw(self, window:pygame.Surface):
		if self.needs_update:
			self.view.fill(BLACK)
			v_w, v_h = find_center(*self.size)
			m1 = "You have already"
			m2 = "played today!"
			m3 = "Come back tomorrow!"
			m4 = "Press tab for Fun Mode!"

			m1_w, _ = find_center(*self.font.size(m1))
			m2_w, _ = find_center(*self.font.size(m2))
			m3_w, _ = find_center(*self.font.size(m3))
			m4_w, _ = find_center(*self.font.size(m4))

			m1_cx = v_w - m1_w
			m2_cx = v_w - m2_w
			m3_cx = v_w - m3_w
			m4_cx = v_w - m4_w

			f_text_obj = self.font.render(m1, True, WHITE)
			s_text_obj = self.font.render(m2, True, WHITE)
			t_text_obj = self.font.render(m3, True, WHITE)
			m4_text_obj = self.font.render(m4, True, WHITE)

			self.view.fill(BLACK)
			self.view.blit(f_text_obj, (m1_cx, v_h - 50))
			self.view.blit(s_text_obj, (m2_cx, v_h))
			self.view.blit(t_text_obj, (m3_cx, v_h + 50))
			self.view.blit(m4_text_obj, (m4_cx, v_h + 100))

			super().draw(window)


