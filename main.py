import pygame
import math

pygame.init()

# SET - UP

#game dimension set-up
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

#planet dimension set-up
PLANET_MASS = 100
SATELLITE_MASS = 5
G = 5
FPS = 60
PLANET_RADIUS = 50
OBJ_SIZE = 5
VEL_SCALE = 150

#setting the images
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("earth.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
SATELLITE = pygame.transform.scale(pygame.image.load("satellite.png"), (PLANET_RADIUS / 2, PLANET_RADIUS / 2))

#setting the color
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    #draws the planet
    def draw(self):
        window.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS)) #draws at the center


class Satellite:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    #moves our objects
    def move(self, planet = None):
        # calcs distances between the two bodies and force of gravitational attraction
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (G * self.mass * planet.mass) / distance ** 2

        # calcs acceleration and angle theta
        acc = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        # calcs acceleration of each direction (x, y)
        acc_x = acc * math.cos(angle)
        acc_y = acc * math.sin(angle)

        # applies acceleration to velocity(wrong way tho)
        self.vel_x += acc_x
        self.vel_y += acc_y

        self.x += self.vel_x
        self.y += self.vel_y

    #draws our objects
    def draw(self):
        window.blit(SATELLITE, (int(self.x), int(self.y)))
        # pygame.draw.circle(window, RED,(int(self.x), int(self.y)), OBJ_SIZE) 

def create_satellite(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse

    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE

    # obj = Satellite(t_x, t_y, vel_x, vel_y, SATELLITE_MASS)
    obj = Satellite(m_x, m_y, vel_x, vel_y, SATELLITE_MASS)

    return obj


#MAIN LOOP

def main():

    running = True
   
    clock = pygame.time.Clock() #for FPS

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None


    while running:
      
        clock.tick(FPS)  #regulates 60 FPS
        mouse_pos = pygame.mouse.get_pos() #gets the mouse position

        #tracks the event occurring during the game
        for event in pygame.event.get():
            #whenever you wanna quit the game / exit the loop
            if event.type == pygame.QUIT:
                running = False

            # checks event for mouse click and sets its position
            if event.type == pygame.MOUSEBUTTONDOWN:

                if temp_obj_pos:
                    #preps to launch
                    t_x, t_y = temp_obj_pos
                    obj = create_satellite(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None #releases the satellite

                else:
                    temp_obj_pos = mouse_pos
        
        window.blit(BG, (0, 0)) #draws the bg to screen

        # draws where mouse was clicked
        if temp_obj_pos:
            pygame.draw.line(window, WHITE, temp_obj_pos, mouse_pos, 2) #draws line where mouse was clicked and dragged
            pygame.draw.circle(window, RED, temp_obj_pos, OBJ_SIZE) #draws circle where mouse was clicked

        # calls instance method draw for every object
        for obj in objects[:]:  # [:] makes copy of objects and uses it to iterate
                obj.draw()
                obj.move(planet)
                off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT #checks if satellite moves out of screen
                
                # when satellite collides with planet
                collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_RADIUS

                # removes objects when off-screen or collided
                if off_screen or collided:
                    objects.remove(obj)
              
        planet.draw()

        pygame.display.update()
    
    pygame.quit()



if __name__ == "__main__":
    main()