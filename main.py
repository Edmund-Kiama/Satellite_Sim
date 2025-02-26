import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Satellite Simulation Effect")

PLANET_MASS = 100
SATELLITE_MASS = 5
G = 9.8
FPS = 60
PLANET_RADIUS = 50
OBJ_SIZE = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("earth.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
SATELLITE = pygame.transform.scale(pygame.image.load("satellite.png"), (PLANET_RADIUS / 2, PLANET_RADIUS / 2))

WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        window.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS)) 


class Satellite:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.orbit = []

    def move(self, planet = None):

        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (G * self.mass * planet.mass) / distance ** 2

        acc = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acc_x = acc * math.cos(angle)
        acc_y = acc * math.sin(angle)

        self.vel_x += acc_x
        self.vel_y += acc_y

        self.x += self.vel_x
        self.y += self.vel_y

        self.orbit.append((self.x, self.y))


    def draw(self):
        if len(self.orbit) > 2 :
            updated_points = []

            for point in self.orbit:
                x, y  = point
                x = x + 10
                y = y + 10
                updated_points.append((x,y))
            
            pygame.draw.lines(window, WHITE, False, updated_points, 1)

        window.blit(SATELLITE, (int(self.x), int(self.y)))

def create_satellite(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse

    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE

    obj = Satellite(m_x, m_y, vel_x, vel_y, SATELLITE_MASS)

    return obj


def main():

    running = True
   
    clock = pygame.time.Clock() 

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None


    while running:
      
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if temp_obj_pos:
                    #preps to launch
                    t_x, t_y = temp_obj_pos
                    obj = create_satellite(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None #releases the satellite

                else:
                    temp_obj_pos = mouse_pos
        
        window.blit(BG, (0, 0))

        # draws where mouse was clicked
        if temp_obj_pos:
            pygame.draw.line(window, WHITE, temp_obj_pos, mouse_pos, 2) #draws line where mouse was clicked and dragged
            pygame.draw.circle(window, RED, temp_obj_pos, OBJ_SIZE) #draws circle where mouse was clicked

        for obj in objects[:]:  # [:] makes copy of objects and uses it to iterate
                obj.draw()
                obj.move(planet)
                off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT #checks if satellite moves out of screen
                
                collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_RADIUS

                if off_screen or collided:
                    objects.remove(obj)
              
        planet.draw()

        pygame.display.update()
    
    pygame.quit()



if __name__ == "__main__":
    main()