import pygame, math
from wasphealth import WaspHealthBar
from Gust import Gust


class Wasp():
    def __init__(self, image, speed = [0,0], pos = [0,0]):
        self.image = pygame.image.load("rsc/Wasp/Wasp.png")
        self.rect = self.image.get_rect()
        self.speedx = speed[0]
        self.speedy = speed[0]
        self.speed = [self.speedx, self.speedy]
        self.maxSpeed = 5
        self.place(pos)
        self.didBounceX = False
        self.didBounceY = False
        self.radius = (int(self.rect.height/2.0 + self.rect.width/2.0)/2) - 1
        self.living = True
        self.healthbar = WaspHealthBar(self)
        self.life = True 
        self.maxLife = True
        self.damage = 5
        self.health = 80
        self.didHit = False
        self.maxHealth = 80
        self.detectionRadius = 100
        
    def place(self, pos):
        self.rect.center = pos
        
    def distToPoint(self, pt):
        x1 = self.rect.center[0]
        x2 = pt[0]
        y1 = self.rect.center[1]
        y2 = pt[1]
        return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        
    def update(self, width, height, player):
        self.didBounceX = False
        self.didBounceY = False
        self.speed = [self.speedx, self.speedy]
        self.move(player)
        self.collideWall(width, height)
        self.healthbar.update()
        self.image.blit(self.healthbar.image, self.healthbar.rect)
        
    def move(self, player):
        if player != None:
            self.detect(player)
        self.rect = self.rect.move(self.speed)

    def detect(self,player):
        if self.distToPoint(player.rect.center) < self.detectionRadius:
            pX = player.rect.center[0]
            pY = player.rect.center[1]
            zX = self.rect.center[0]
            zY = self.rect.center[1]
           
            if pX > zX:
                self.speed[0] = self.maxSpeed
            elif pX < zX:
                self.speed[0] = -self.maxSpeed
            else:
                self.speed[0] = 0
       
            if pY > zY:
                self.speed[1] = self.maxSpeed
            elif pY < zY:
                self.speed[1] = -self.maxSpeed
            else:
                self.speed[1] = 0
        
    def collideWall(self, width, height):
        if not self.didBounceX:
            if self.rect.left < 0 or self.rect.right > width:
               self.speedx = -self.speedx
               self.didBounceX = True
               #print "hit xWall"
        if not self.didBounceY:
            if self.rect.top < 0 or self.rect.bottom > height:
               self.speedy = -self.speedy
               self.didBounceY = True
               #print "hit xWall"
               
    def attack(self, atk):
        if atk == "stinger" and self.stingerCoolDown == 0:
            self.stingering = True
            self.stingerCoolDown = self.stingerCoolDownMax
            return [Stinger(self)]
        return []
        
    def collideWasp(self, other):
        if self != other:
            if self.rect.right > other.rect.left and self.rect.left < other.rect.right:
                if self.rect.bottom > other.rect.top and self.rect.top < other.rect.bottom:
                    if (self.radius + other.radius) > self.distance(other.rect.center):
                        if not self.didBounceX:
                            self.speedx = -self.speedx
                            self.didBouncex = True
                        if not self.didBounceY:
                            self.speedy = -self.speedy
                            self.didBounceY = True
                            #print "hit wasp"
                        if not self.didHit:
                            self.speed[0] = self.speed[0] * -1
                            self.speed[1] = self.speed[1] * -1
                            self.move(None)
                            self.move(None)
                            self.didHit = True
                        return True
            return False
    
    '''def collideGust(self, other):
        if self != other:
            if self.rect.right > other.rect.left and self.rect.left < other.rect.right:
                if self.rect.bottom > other.rect.top and self.rect.top < other.rect.bottom:
                    if (self.radius + other.radius) > self.distance(other.rect.center):
                        self.living = False'''
                            
    def collidePlayer(self, other):
        if self != other:
            if self.rect.right > other.rect.left and self.rect.left < other.rect.right:
                if self.rect.bottom > other.rect.top and self.rect.top < other.rect.bottom:
                    if (self.radius + other.radius) > self.distance(other.rect.center):
                        pass
                        #self.living = False

    def collideGust(self, attack):
        if (self.rect.right > attack.rect.left and self.rect.left < attack.rect.right):
            if (self.rect.bottom > attack.rect.top and self.rect.top < attack.rect.bottom):
                if (self.distToPoint(attack.rect.center) < self.radius + attack.radius):
                    self.life -= attack.damage
                    self.healthbar.update()
                print "Hit", self.life
                if self.life <= 0:
                    self.health -= attack.damage
                    self.healthbar.update()
                    print "Hit Done", self.health
                    if self.health <= 0:
                        self.living = False
                        
    def collideSpray(self, attack):
        if (self.rect.right > attack.rect.left and self.rect.left < attack.rect.right):
            if (self.rect.bottom > attack.rect.top and self.rect.top < attack.rect.bottom):
                if (self.distToPoint(attack.rect.center) < self.radius + attack.radius):
                    self.life -= attack.damage
                    self.healthbar.update()
                print "Hit", self.life
                if self.life <= 0:
                    self.health -= attack.damage
                    self.healthbar.update()
                    print "Hit Done", self.health
                    if self.health <= 0:
                        self.living = False
                        
    def collideStinger(self, other):
        if self != other:
            if self.rect.right > other.rect.left and self.rect.left < other.rect.right:
                if self.rect.bottom > other.rect.top and self.rect.top < other.rect.bottom:
                    if (self.radius + other.radius) > self.distance(other.rect.center):
                        self.living = False
    
    def distance(self, pt):
        x1 = self.rect.center[0]
        y1 = self.rect.center[1]
        x2 = pt[0]
        y2 = pt[1]
        return math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
        
 
if __name__ == "__main__":
     
    pygame.init()

    clock = pygame.time.Clock()

    width = 800
    height = 600
    fullscreen = 0
    altFlag = False
    size = width, height
    screen = pygame.display.set_mode(size)

    bgColor = r, g, b = 0, 0, 0           
    #player = Player([375,300])
    
    wasp = Wasp("rsc/Wasp/Wasp.png", [1, 2], [100, 125])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        #wasp.update(width, height, player)
        
        screen.fill(bgColor)
        screen.blit(wasp.image, wasp.rect)
        pygame.display.flip()
        clock.tick(60) 
        def distance(self, pt):
            x1 = self.rect.center[0]
            y1 = self.rect.center[1]
            x2 = pt[0]
            y2 = pt[1]
            return math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
        
    
    
