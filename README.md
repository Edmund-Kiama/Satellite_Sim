# Satellite Simulation

## Overview
This project is a **gravitational slingshot effect simulator** built using **Python** and **Pygame**. It simulates the movement of satellites around a planet using basic gravitational physics. Users can click and drag to launch satellites, observing how gravity affects their trajectories.

## Features
- **Realistic Gravity Simulation:** Satellites are attracted to the central planet using Newton's law of gravitation.
- **Mouse-Based Launch System:** Click to place a satellite, drag to set velocity, and release to launch.
- **Collision & Off-Screen Handling:** Satellites disappear if they collide with the planet or move off-screen.
- **Custom Graphics:** Background, planet and satellite images for a more engaging simulation.

## Requirements
Ensure you have the following installed:

- Python 3.x
- Pygame

### Install Dependencies
````bash
pip install pygame
````

## How to Run the Simulation
````bash
python main.py
````

## Controls
- **Left Click & Hold:** Set the initial position of the satellite.
- **Drag Mouse:** Adjust the launch velocity.
- **Release Mouse:** Launch the satellite.
- **Close Window:** Exit the simulation.

## Code Structure
### 1. **Setup & Constants**
- Initializes Pygame.
- Defines screen size, physics constants, colors and image assets.

### 2. **Classes**
#### **Planet**
Represents the central body exerting gravitational force.
````python
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        window.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))
````
#### **Satellite**
Represents an orbiting object affected by gravity.
````python
class Satellite:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
````
#### **Physics Implementation**
Gravity is calculated using Newton's law of universal gravitation:
````math
F = \frac{G \cdot m_1 \cdot m_2}{r^2}
````
Where:
- \( F \) is the gravitational force
- \( G \) is the gravitational constant
- \( m_1 \) and \( m_2 \) are the masses of the objects
- \( r \) is the distance between the two objects

The acceleration experienced by the satellite is given by:
````math
a = \frac{F}{m}
````
The velocity components are updated as follows:
````python
acc_x = acc * math.cos(angle)
acc_y = acc * math.sin(angle)

self.vel_x += acc_x
self.vel_y += acc_y
````

### 3. **Creating a Satellite**
````python
def create_satellite(location, mouse):
    vel_x = (mouse[0] - location[0]) / VEL_SCALE
    vel_y = (mouse[1] - location[1]) / VEL_SCALE
    return Satellite(mouse[0], mouse[1], vel_x, vel_y, SATELLITE_MASS)
````

### 4. **Main Loop**
Handles events, updates positions and redraws objects every frame.
````python
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
````

## Future Improvements
- Implement different gravitational forces for multiple planets.
- Add satellite trails for better visualization.
- Introduce more accurate physics using numerical integration.

## Acknowledgments
- Built using **Python** and **Pygame**.
- Inspired by real-world orbital mechanics.

## License
This project is open-source and free to use.

