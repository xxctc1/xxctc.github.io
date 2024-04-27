import pygame
import sys
import random

# Inizializzazione di Pygame
pygame.init()
pygame.mixer.init()

# Caricamento della musica di sottofondo
pygame.mixer.music.load("C:/Users/julia/Downloads/Wii Music Main Menu Original Theme.mp3")

# Imposta il volume della musica (valore compreso tra 0 e 1)
pygame.mixer.music.set_volume(0.5)

# Avvia la riproduzione della musica di sottofondo in loop infinito
pygame.mixer.music.play(loops=-1)

# Definizione dei colori
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 25, 255)
GREEN = (0, 255, 0)

# Definizione della dimensione dello schermo
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Two-Player Game")

# Definizione della classe del personaggio
class Character(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.lives = 3
        self.name = name

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def shoot(self, direction):
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.kill()

# Definizione della classe del proiettile
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 30
        self.direction = direction

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0:
            self.kill()

# Definizione della classe degli ostacoli
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Aggiorna la posizione degli ostacoli
        pass  # Non è necessario fare nulla in questo caso
   

# Funzione per disegnare il testo delle vite rimaste
def draw_lives():
    font = pygame.font.Font(None, 36)
    duck_lives_text = font.render(f"Duck Lives: {duck.lives}", True, RED)
    bird_lives_text = font.render(f"Bird Lives: {bird.lives}", True, PURPLE)
    screen.blit(duck_lives_text, (SCREEN_WIDTH - 200, 10))
    screen.blit(bird_lives_text, (10, 10))

# Caricamento delle immagini dei personaggi
duck_image = pygame.image.load("C:/Users/julia/Downloads/Duck_Trophy_transparent.webp").convert_alpha()
bird_image = pygame.image.load("C:/Users/julia/Downloads/pngegg.png").convert_alpha()

# Ridimensionamento delle immagini dei personaggi
duck_image = pygame.transform.scale(duck_image, (120, 120))
bird_image = pygame.transform.scale(bird_image, (120, 120))

# Caricamento delle immagini degli ostacoli
obstacle_image = pygame.Surface((50, 50))
obstacle_image.fill(GREEN)

# Creazione dei gruppi di sprite per i personaggi e i proiettili e ostacoli
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Creazione dei personaggi
duck = Character(duck_image, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, "Duck")
bird = Character(bird_image, 50, 50, "Bird")

# Creazione degli ostacoli
def create_obstacles():
    for _ in range(10):
        obstacle = Obstacle(obstacle_image, random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50))
        obstacles.add(obstacle)

# Creazione degli ostacoli
create_obstacles()
all_sprites.add(obstacles)

# Aggiunta dei personaggi al gruppo degli sprite
all_sprites.add(duck, bird)
def determine_winner():
    if duck.lives <= 0:
        return "Bird"
    elif bird.lives <= 0:
        return "Duck"
    else:
        return None

# Definizione della schermata di Game Over
def show_game_over_screen(winner_name):
    game_over_font = pygame.font.Font(None, 64)
    game_over_text = game_over_font.render("Game Over", True, RED)
    winner_font = pygame.font.Font(None, 36)
    winner_text = winner_font.render(f"Winner: {winner_name}", True, RED)

    # Disegna la schermata di Game Over
    screen.fill(WHITE)  # Sostituisci con il tuo sfondo
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, 300))
    pygame.display.flip()    


# Loop del gioco
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                duck.shoot("left")
            elif event.key == pygame.K_SPACE:
                bird.shoot("right")

    winner_name = determine_winner()
    # Reimposta lo stato del gioco e le vite dei personaggi
    if winner_name:
        show_game_over_screen(winner_name)
        pygame.time.wait(3000)
        duck.lives = 3
        bird.lives = 3
        all_sprites.empty()
        bullets.empty()
        all_sprites.add(duck, bird)
        # Ricrea gli ostacoli
        obstacles.empty()
        create_obstacles()

        # Aggiunta degli ostacoli al gruppo degli sprite
        all_sprites.add(obstacles)
        
    # Alla fine del round (quando un personaggio perde tutte le vite)
    # Chiamare la funzione show_game_over_screen con il nome del personaggio vincitore
    # Esempio: sostituisci con il nome del vincitore effettivo
    
    # Movimento dei personaggi
    keys = pygame.key.get_pressed()
    bird.move(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
    duck.move(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])

    # Rilevamento delle collisioni tra personaggi/proiettili e ostacoli
    collision_list = pygame.sprite.spritecollide(duck, obstacles, False)
    for obstacle in collision_list:
         # Ferma il movimento del personaggio quando entra in collisione con un ostacolo
         duck.rect.x -= duck.speed
         duck.rect.y -= duck.speed

    collision_list = pygame.sprite.spritecollide(bird, obstacles, False)
    for obstacle in collision_list:
         # Ferma il movimento del personaggio quando entra in collisione con un ostacolo
         bird.rect.x -= bird.speed
         bird.rect.y -= bird.speed
 
    collision_list = pygame.sprite.groupcollide(bullets, obstacles, True, False)
    for bullet, obstacle in collision_list.items():
         # Rimuovi il proiettile quando entra in collisione con un ostacolo
         bullet.kill()

    # Limiti di movimento
    duck.rect.clamp_ip(screen.get_rect())
    bird.rect.clamp_ip(screen.get_rect())

    # Rilevamento delle collisioni tra proiettili e personaggi
    for bullet in bullets:
        if pygame.sprite.collide_rect(bullet, duck) and bullet.direction == "right":
            duck.hit() 
            bullet.kill()
        elif pygame.sprite.collide_rect(bullet, bird) and bullet.direction == "left":
            bird.hit()
            bullet.kill()

    # Aggiornamento dei proiettili
    bullets.update()

    # Aggiornamento della posizione degli ostacoli
    obstacles.update()

    # Pulizia dello schermo
    screen.fill(WHITE)

    # Disegno dei personaggi e dei proiettili
    all_sprites.draw(screen)
    bullets.draw(screen)

    # Disegno del testo delle vite rimaste
    draw_lives()
 
    # Aggiornamento dello schermo
    pygame.display.flip()

    # Limitazione della velocità di aggiornamento del gioco
    pygame.time.Clock().tick(60)

# Uscita dal gioco
pygame.quit()
sys.exit()