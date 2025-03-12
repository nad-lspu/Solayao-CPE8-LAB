import pygame
import random

pygame.init()

width, height = 800, 400
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

ship_img = pygame.image.load("ship.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
bossing_img = pygame.image.load("bossing.png")

clock = pygame.time.Clock()
font = pygame.font.Font("PixemonTrialRegular-p7nLK.ttf", 28)


class Player:
   def __init__(self):
       self.image = pygame.transform.scale(ship_img, (80, 80))
       self.x = width // 2 - 25
       self.y = height - 70
       self.speed = 5
       self.health = 50

   def move(self, direction):
       if direction == "left" and self.x > 0:
           self.x -= self.speed
       if direction == "right" and self.x < width - 50:
           self.x += self.speed

   def draw(self):
       screen.blit(self.image, (self.x, self.y))
       health_text = font.render(f"Buhay Mo: {self.health}", True, green)
       screen.blit(health_text, (10, 40))

   def taken_damage(self):
       self.health -= 1

class Enemy:
   def __init__(self, x, y):
       self.image = pygame.transform.scale(enemy_img, (40, 40))
       self.x = x
       self.y = y
       self.speed = 3
       self.direction = 1

   def move(self):
       self.x += self.speed * self.direction
       if self.x >= width - 40 or self.x <= 0:
           self.direction *= -1
           self.y += 40

   def draw(self):
       screen.blit(self.image, (self.x, self.y))

class Bullet:
   def __init__(self, x, y, speed=-7):
       self.image = pygame.transform.scale(bullet_img, (40, 40))
       self.x = x + 20
       self.y = y
       self.speed = speed
       self.active = True

   def move(self):
       self.y += self.speed
       if self.y < 0 or self.y > height:
           self.active = False

   def draw(self):
       screen.blit(self.image, (self.x, self.y))

class Bossing:
   def __init__(self):
       self.image = pygame.transform.scale(bossing_img, (110, 110))
       self.x = width // 2 - 50
       self.y = 50
       self.speed = 2
       self.direction = 1
       self.health = 100
       self.bullets = []

   def move(self):
       self.x += self.speed * self.direction
       if self.x >= width - 100 or self.x <= 0:
           self.direction *= -1

   def fire(self):
       if random.randint(1, 15) == 1:
           self.bullets.append(Bullet(self.x + 45, self.y + 90, speed=5))

   def draw(self):
       screen.blit(self.image, (self.x, self.y))
       health_text = font.render(f" Buhay ni Bossing: {self.health}", True, red)
       screen.blit(health_text, (300, 10))

   def taken_damage(self):
       self.health -= 1

class SpaceInvaders:
   def __init__(self):
       self.player = Player()
       self.enemies = [Enemy(random.randint(50, width - 50), random.randint(50, 200)) for _ in range(5)]
       self.bullets = []
       self.enemy_count = 0
       self.bossing = None
       self.running = True


   def run(self):
       while self.running:
           screen.fill(black)
           self.handle_events()
           self.update()
           self.draw()

           if self.bossing and self.bossing.health <= 0:
               self.display_message("You Win!", f"Total Points: {self.enemy_count}")
               self.running = False

           if self.player.health <= 0:
               self.display_message("Patay ka HAHAHA!", f"Total Points: {self.enemy_count}")
               self.running = False

           pygame.display.update()
           clock.tick(60)


   def handle_events(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_LEFT] or keys[pygame.K_a]:
           self.player.move("left")
       if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
           self.player.move("right")
       if keys[pygame.K_SPACE]:
           self.bullets.append(Bullet(self.player.x, self.player.y))

       for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   self.running = False


   def update(self):
       for enemy in self.enemies:
           enemy.move()

           if self.player.x < enemy.x + 40 and self.player.x + 50 > enemy.x and self.player.y < enemy.y + 40 and self.player.y + 50 > enemy.y:
               self.player.taken_damage()
               self.enemies.remove(enemy)
               self.enemies.append(Enemy(random.randint(50, width - 50), random.randint(50, 200)))
               break


       for bullet in self.bullets:
           bullet.move()

       self.bullets = [b for b in self.bullets if b.active]
       for bullet in self.bullets:
           for enemy in self.enemies:
               if enemy.x < bullet.x + 40 and enemy.y < bullet.y < enemy.y + 40:
                   self.enemies.remove(enemy)
                   self.bullets.remove(bullet)
                   self.enemy_count += 1
                   self.enemies.append(Enemy(random.randint(50, width - 50), random.randint(50, 200)))
                   break

       if self.enemy_count >= 30:
           if not self.bossing:
               self.bossing = Bossing()

           self.bossing.move()
           self.bossing.fire()

           for bullet in self.bossing.bullets:
               bullet.move()
               if bullet.x < self.player.x + 50 and bullet.x + 10 > self.player.x and bullet.y > self.player.y:
                   self.player.taken_damage()
                   self.bossing.bullets.remove(bullet)

           for bullet in self.bullets:
               if self.bossing.x < bullet.x < self.bossing.x + 100 and self.bossing.y < bullet.y < self.bossing.y + 100:
                   self.bossing.taken_damage()
                   self.bullets.remove(bullet)


   def draw(self):
       self.player.draw()
       for enemy in self.enemies:
           enemy.draw()
       for bullet in self.bullets:
           bullet.draw()

       if self.bossing:
           self.bossing.draw()
           for bullet in self.bossing.bullets:
               bullet.draw()

       score_text = font.render(f"Enemies Killed: {self.enemy_count}", True, white)
       screen.blit(score_text, (10, 10))

   def display_message(self, message, subtext):
       screen.fill(black)
       text = font.render(message, True, white)
       subtext = font.render(subtext, True, white)
       screen.blit(text, (width // 2 - 100, height // 2 - 20))
       screen.blit(subtext, (width // 2 - 100, height // 2 + 20))
       pygame.display.update()
       pygame.time.delay(3000)


if __name__ == "__main__":
   game = SpaceInvaders()
   game.run()

   pygame.quit()

