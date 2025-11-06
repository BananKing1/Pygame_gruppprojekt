import pygame

#button class
class Button():
	def __init__(self, x, y, image):
		
		self.image = image
		
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.removed=False

	def draw(self, screen):
		action = False
		mouse = pygame.mouse.get_pos()
		if not self.removed:

			if self.rect.collidepoint(mouse):
				if any(pygame.mouse.get_pressed()) and not self.clicked:
					self.clicked = True
					action = True

			if not any(pygame.mouse.get_pressed()):
				self.clicked = False

			
			screen.blit(self.image, (self.rect.x, self.rect.y))

			return action
	def remove(self):
		self.removed=True
