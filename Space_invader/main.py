import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
background = pygame.image.load('background.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-ship.png')
playerX = 370
playerY = 480
playerX_change=0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5


for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('alien.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(4)
	enemyY_change.append(20)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x,y):
	screen.blit(playerImg,(x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i],(x,y))

def fireBullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX,enemyY, bulletX, bulletY):
	distance = math.sqrt(math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2))
	if distance < 27:
		return True
	else:
		return False
running = True
while running:
	screen.fill((0, 0, 0))
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key ==  pygame.K_LEFT:
				playerX_change -= 5
			if event.key ==  pygame.K_RIGHT:
				playerX_change += 5
			if event.key ==  pygame.K_SPACE:
				if bullet_state == "ready":
					bulletX = playerX
					fireBullet(bulletX,bulletY)
		if event.type == pygame.KEYUP:
			if event.key ==  pygame.K_LEFT or pygame.K_RIGHT:
				playerX_change = 0

	playerX += playerX_change

#Boundary player
	if playerX <= 0:
		playerX = 0
	elif playerX > 736:
		playerX = 736

	

#Boundary enemy
	for i in range(num_of_enemies):
		# game Over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 3
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] > 736:
			enemyX_change[i] = -3
			enemyY[i] += enemyY_change[i]

		# isCollision
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosionSound = mixer.Sound("explosion.wav")
			explosionSound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)

		enemy(enemyX[i], enemyY[i],i)

# bullet movement
	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"

	if bullet_state == "fire":
		fireBullet(bulletX,bulletY)
		bulletY -= bulletY_change


	player(playerX,playerY)
	show_score(textX, testY)
	pygame.display.update()



