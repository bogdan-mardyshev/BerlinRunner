from settings import *
import os
import random
#add class for main character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and scale individual frames for the running animation
        # I use .convert_alpha() for transparency optimization
        self.run_frames = [] #list of pictures for animations
        frame1_original = pygame.image.load(os.path.join("Assets", "character2.png")).convert_alpha()#import 1 image of character from os directory
        frame1_scaled = pygame.transform.scale(frame1_original, (100, 150)) #scale image 1
        self.run_frames.append(frame1_scaled) #add 1 image to list

        frame2_original = pygame.image.load(os.path.join("Assets", "character3.png")).convert_alpha()  # import 2 image of character from os directory
        frame2_scaled = pygame.transform.scale(frame2_original, (100, 150))  # scale image 2
        self.run_frames.append(frame2_scaled)  # add 2 image to list

        frame3_original = pygame.image.load(os.path.join("Assets", "character4.png")).convert_alpha()  # import 2 image of character from os directory
        frame3_scaled = pygame.transform.scale(frame3_original, (100, 150))  # scale image 2
        self.run_frames.append(frame3_scaled)

        frame4_original = pygame.image.load(os.path.join("Assets", "character5.png")).convert_alpha()  # import 2 image of character from os directory
        frame4_scaled = pygame.transform.scale(frame4_original, (100, 150))  # scale image 2
        self.run_frames.append(frame4_scaled)

        frame6_original = pygame.image.load(os.path.join("Assets", "character6.png")).convert_alpha()  # import 2 image of character from os directory
        frame6_scaled = pygame.transform.scale(frame6_original, (100, 150))  # scale image 2
        self.run_frames.append(frame6_scaled)

        # Image for crouching (smaller height)
        self.crouch_image = pygame.transform.scale(frame1_original, (100, 90))

        #Settings of Animations
        self.frame_index = 0
        self.image = self.run_frames[self.frame_index] # Set initial image
        # Rect defines the position and hitbox of the sprite
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 60)) #set position of character

        #create physics
        self.gravity = 0
        self.jump_power = -16 # Negative value moves up in Pygame
        self.weight = 0.8 #Gravity force applied per frame
        # State variable: are we ducking now?
        self.is_crouching = False # State flag

        # Mask for Pixel-Perfect Collision (ignores transparent pixels)
        self.mask = pygame.mask.from_surface(self.image)

        #Audio
        if os.path.exists(os.path.join("Assets", "jump.wav")):
            self.jump_sound = pygame.mixer.Sound(os.path.join("Assets", "jump.wav"))
            self.jump_sound.set_volume(0.5)
        else:
            self.jump_sound = None

    def animation_state(self):
        """Handles switching images based on state (Running or Crouching)."""
        if self.is_crouching:
            # Remember where your feet were (don't fall through)
            old_bottom = self.rect.midbottom #Save feet position
            # Post a picture of a squat
            self.image = self.crouch_image
            #Update mask and rect for the smaller image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(midbottom=old_bottom)
            # 2. Jumping (Display static frame when in air)
        elif self.rect.bottom < HEIGHT - 60:
            self.image = self.run_frames[0]
            self.mask = pygame.mask.from_surface(self.image)
        #Running state (Cycle through frames)
        else:
            # Remember the position of the legs before changing the frame
            old_bottom = self.rect.midbottom
            self.frame_index += 0.15 # Controls animation speed
            if self.frame_index >= len(self.run_frames):
                self.frame_index = 0
            self.image = self.run_frames[int(self.frame_index)]
            #Restoring the hitbox
            self.rect = self.image.get_rect(midbottom=old_bottom)
            # Update hitbox and mask
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(midbottom=old_bottom)

    def player_input(self):
        """Handles keyboard input for Jumping and Crouching."""
        keys = pygame.key.get_pressed() # Get a list of all pressed buttons
        # Jump mechanic
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
           #Only allow jump if player is on the ground
            if self.rect.bottom >= HEIGHT - 60 :
                self.gravity = self.jump_power # Apply upward force
                if self.jump_sound:
                    self.jump_sound.play()
            #Squat mechanic
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # Only allow crouch on the ground
            if self.rect.bottom >= HEIGHT - 60:
                self.is_crouching = True
        else:
            self.is_crouching = False


    def apply_gravity(self):
        """Simulates physics by constantly pulling the player down."""
        self.gravity += self.weight
        self.rect.y += self.gravity
        # Floor collision check
        if self.rect.bottom >= HEIGHT - 60:
            self.rect.bottom = HEIGHT - 60
            self.gravity = 0 # Stop falling

    def update(self):
        #Main update loop called every frame
       self.player_input()
       self.apply_gravity()
       self.animation_state()

       #Add Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        img = pygame.image.load(os.path.join("Assets", "enemy2.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (90, 120))
        # Random spawn position off-screen
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH + 100, WIDTH + 300), HEIGHT - 60))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4
        self.triggered = False # Flag for "Chase Mode"

    def update(self, speed):
        # Enemy Logic: Run faster if triggered
        if self.triggered:
            # Move faster than the world speed to catch the player
            self.rect.x -= (speed + 8)
        else:
            # Move with the world speed
            self.rect.x -= speed
        # Trigger logic: If close to player (x < 600), start running
        if self.rect.x < 600 and not self.triggered:
            self.triggered = True
        # Despawn if off-screen to the left
        if self.rect.right < -100:
            self.kill()
#Static Obstacles (Trash & Scooter)
class Trash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img1 = pygame.image.load(os.path.join("Assets", "trash.png")).convert_alpha()
        self.image = pygame.transform.scale(img1, (200, 90))

        self.rect = self.image.get_rect(midbottom = (random.randint(WIDTH + 20, WIDTH + 200), HEIGHT - 60))

        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < -100:
            self.kill() # Remove from memory

class Scooter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img1 = pygame.image.load(os.path.join("Assets", "e-scooter.png")).convert_alpha()
        self.image = pygame.transform.scale(img1, (120, 60))
        self.rect = self.image.get_rect(midbottom = (random.randint(WIDTH + 20, WIDTH + 200), HEIGHT - 60))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < -100:
            self.kill() # Remove from memory

#Flying Obstacle (Dove)
class Dove(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fly_frames = []  # list of pictures for animations
        # Load frames for flying animation
        img1 = pygame.image.load(os.path.join("Assets", "dove1.png")).convert_alpha()#import 1 image of dove from os directory
        img1 = pygame.transform.scale(img1, (80, 50))
        self.fly_frames.append(img1)#add 1 image to list

        img2 = pygame.image.load(os.path.join("Assets", "dove2.png")).convert_alpha()#import 2 image of dove from os directory
        img2 = pygame.transform.scale(img2, (80, 50))
        self.fly_frames.append(img2)#add 2 image to list

        self.frame_index = 0
        self.image = self.fly_frames[self.frame_index] #first frame
        # Random height (Head level or Jump level)
        y_pos = random.choice([HEIGHT - 70, HEIGHT - 160])
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH + 50, WIDTH + 200), y_pos)) #set position of dove

        self.speed = 7
        self.mask = pygame.mask.from_surface(self.image)

    def animation_state(self):
        # Fast wing animation
        self.frame_index += 0.2
        if self.frame_index >= len(self.fly_frames):
            self.frame_index = 0
        self.image = self.fly_frames[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed):
        self.animation_state()
        # Doves fly faster than the background (+2 speed)
        self.rect.x -= (speed + 2)

        if self.rect.right < -100:
            self.kill()

#Collectible (Bottle)
class Bottle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        img = pygame.image.load(os.path.join("Assets", "bottle1.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (100, 80))
        self.mask = pygame.mask.from_surface(self.image)


        # Bottles can appear on the ground or in the air
        y_pos = random.choice([HEIGHT - 60, HEIGHT - 120])
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH + 50, WIDTH + 300), y_pos))


    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < -100:
            self.kill()

