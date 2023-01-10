import pygame
import os

pygame.init()
main_font = pygame.font.SysFont("cambria", 50)

#On crée une classe bouton, afin de pouvoir intéragir avec le joueur. Un bouton possède une position, une image, un texte, et des rectangles pygame permettant de l'afficher correctement
class button:
	def __init__(self, image = pygame.image.load(os.path.join('Images_cartes',"button.png")), x_pos= 450, y_pos = 350, text_input = 'Play', font = main_font, dimensions = (400, 150)):
		self.image = pygame.transform.scale( image , dimensions)
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_input = text_input
		self.text = font.render(self.text_input, True, "white")
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	#On affiche l'image du bouton et le texte associé sur la fenêtre donnée en argument
	def update(self, screen):
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	# On vérifie si le bouton est actionné (cela se fait de paire avec le suivi du mouvement et de l'actionnement de la souris)
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	#Lorsque la souris se situe sur le bouton (qu'il soit ou non cliqué), on change la couleur du texte pour le signaler
	def changeColor(self, position, font):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = font.render(self.text_input, True, "green")
		else:
			self.text = font.render(self.text_input, True, "white")

