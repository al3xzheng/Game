import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load("Graphics/player.png").convert_alpha(), 0.4)
        self.rect = self.image.get_rect(center = (100,100))

    def playerInput (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
             self.rect.y -=5
        if keys[pygame.K_a]:
             self.rect.x -=5
        if keys[pygame.K_s]:
             self.rect.y +=5
        if keys[pygame.K_d]:
             self.rect.x +=5
    
    def update (self):
        self.playerInput()

pygame.init()
pygame.display.set_caption("Game Name") #This names our game
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN|pygame.NOFRAME) #Makes our game fill an entire screen
w, h = screen.get_size()
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(Player())

# def startKey():
#     startKey = "play"
#     start_surf = pygame.font.SysFont("Arial", 50).render(f'{startKey}',False,(64,64,64))
#     start_rect = start_surf.get_rect(center = (w/2,h/2))
#     screen.blit(start_surf, start_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   #uninitializes pygame when you press x on the screen
            pygame.sys.exit() #exits the while loop to end the script
    
    screen.fill("Red")
    player.draw(screen)
    player.update()

    pygame.display.update() #displays surface that we blit
    clock.tick(60) #frames per second

