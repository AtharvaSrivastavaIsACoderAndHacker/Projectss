# This Weather app is not optimized in terms of Time Complexity and Space/Resource Complexity ! Just a practice project, not  for daily use as it uses avg  140 MB ram and a good chunk of cpu, like 0.1 to 0.2 GHz !
# So don't judge me in  terms of Time/Space Complexity !


import pygame
import random
import geocoder
import threading
import requests
import time


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


class RainDrop:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(-600, 0)
        self.speed = random.randint(10, 30)

    def update(self):
        if self.y > 600:
            splash_particles = [SplashParticle(self.x, 600) for _ in range(3)]
            splashes.extend(splash_particles)
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, 800)
        else:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.line(screen, (180, 180, 255), (self.x, self.y), (self.x, self.y + 10), 1)
        
class SplashParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.3, 1.3)
        self.vy = random.uniform(-3, 5)
        self.life = 35

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 3

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 200, 255), (int(self.x), int(self.y)), 1)

class Fog:
    def __init__(self):
        self.fog_surface = pygame.Surface((random.randint(50,150), random.randint(10,30)), pygame.SRCALPHA)
        self.fog_surface.fill((255, 255, 255, 100))
        self.x_offset = random.randint(0, 800)
        self.y_offset = random.randint(0,25)
        self.direction = random.randint(-1,1)

    def update(self):
        self.x_offset += random.uniform(0.001,0.1)*self.direction
        if self.x_offset > 800:
            self.x_offset = 0
        self.y_offset += random.uniform(0.002,0.01)*self.direction

    def draw(self, screen):
        screen.blit(self.fog_surface, (self.x_offset, self.y_offset))


def rain():
    rainBool = True
    for drop in raindrops:
        drop.update()
        drop.draw(screen)
    for fog in fogs:
        fog.update()
        fog.draw(screen)
    for splash in splashes[:]:
        splash.update()
        splash.draw(screen)
        if splash.life <= 0:
            splashes.remove(splash)
    return rainBool

def clear():
    screen.blit(bliss, (0,0))
    return True

def cloudy():
    screen.blit(bliss, (0,0))
    for fog in fogs:
        fog.update()
        fog.draw(screen)
    return True

def foggMist():
    screen.blit(fog, (0,0))
    return True

def snoww():
    screen.blit(snow, (0,0))
    return True


def weatherDislay(head, tem, location):    
    headd = fontt.render(head, True, (255,255,255))
    screen.blit(headd, (140, 170)) 
    temm = fonttt.render(tem, True, (255,255,255))
    screen.blit(temm, (140, 300)) 
    loc = fontttt.render(location, True, (255,255,255))
    screen.blit(loc, (140, 350))
     
def loadAssets(assetContainer):
    assetContainer.append(pygame.mixer.Sound("sounds\\rain.mp3"))
    assetContainer.append(pygame.mixer.Sound("sounds\\clear.mp3") )
    assetContainer.append(pygame.transform.scale(pygame.image.load("images\\bliss.png").convert_alpha(), (800, 600)))
    assetContainer.append(pygame.transform.scale(pygame.image.load("images\\fog.jpg").convert_alpha(), (800, 600)))
    assetContainer.append(pygame.transform.scale(pygame.image.load("images\\snow.jpg").convert_alpha(), (800, 600)))
    assetContainer.append(pygame.mixer.Sound("sounds\\wind.mp3") )
    global assetsLoaded
    assetsLoaded = True

def loadLocation():
    loc = geocoder.ip('me')
    weatherInfo[0] = loc.city
    weatherInfo[1] = loc.latlng
    global locationLoaded
    locationLoaded = True
    location_ready.set()

def fetchWeatherData(): 
    global weatherInfo
    try:
        location_ready.wait()
        lat, lon = weatherInfo[1]

        url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
        response = requests.get(url)
        data = response.json()
        
        if 'current_weather' in data:
            temp = f"{data['current_weather']['temperature']}°C"
            weather = data['current_weather']['weathercode']
            weather_conditions = {
                0: "Clear",
                1: "Cloudy",
                2: "Cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Fog",
                51: "Drizzle",
                53: "Drizzle",
                55: "Drizzle",
                56: "Drizzle",
                57: "Drizzle",
                61: "Rain",
                63: "Rain",
                65: "Rain",
                66: "Rain",
                67: "Rain",
                71: "Snow",
                73: "Snow",
                75: "Snow",
                77: "Snow",
                80: "Showers",
                81: "Showers",
                82: "Showers",
                85: "Showers",
                86: "Showers",
                95: "Thunderstorm",
                96: "Thunderstorm",
                99: "Thunderstorm",
            }
            weather_desc = weather_conditions.get(weather, "Unknown")
            weatherInfo[2] = temp
            weatherInfo[3] = weather_desc
    except Exception as e:
        print(f"Error fetching weather: {e}")

def startThreads():
    t1 = threading.Thread(target=loadAssets, args=(assetContainer,))
    t2 = threading.Thread(target=loadLocation)
    t3 = threading.Thread(target=fetchWeatherData)
    t1.start()
    t2.start()
    t3.start()
    
    
fogs = [Fog() for _ in range(10)]
raindrops = [RainDrop() for _ in range(200)]
splashes = []
clearBool = False
cloudyBool = False
clearPlaying = False
rainBool = False
rain_playing = False
windBlowing = False
font = pygame.font.Font(None, 50)
fontt = pygame.font.Font(None, 180)
fonttt = pygame.font.Font(None, 60)
fontttt = pygame.font.Font(None, 30)


assetContainer = []
weatherInfo = ["Locating...", "LatLong", "Loading...", "Loading..."]  # [city, lat/lng, temp, weather]
assetsLoaded = False
locationLoaded = False
location_ready = threading.Event()
start = time.time()
end = time.time()
startThreads()


waitCount = 0
running = True


while running:
    if not assetsLoaded:
        screen.fill((0, 0, 0))
        txt = font.render(f"Loading ", True, (255, 255, 255))
        if waitCount//10 == 1:
            txt = font.render(f"Loading .", True, (255, 255, 255))
        elif waitCount//10 == 2:
            txt = font.render(f"Loading ..", True, (255, 255, 255))
        elif waitCount//10 == 3:
            txt = font.render(f"Loading ...", True, (255, 255, 255))
        screen.blit(txt, (300, 280))
        pygame.display.flip()
        clock.tick(60)
        waitCount +=1
        if waitCount>40:
            waitCount = 0
        continue
    else:
        
        if (end-start > 600):
            clearBool = False
            cloudyBool = False
            clearPlaying = False
            rainBool = False
            rain_playing = False
            windBlowing = False
            assetsLoaded = False
            locationLoaded = False
            startThreads()
            start = time.time()
            continue
            
        rain_sound = assetContainer[0]
        clear_sound = assetContainer[1] 
        bliss = assetContainer[2]
        fog = assetContainer[3]
        snow = assetContainer[4]
        wind = assetContainer[5]
    
        screen.fill((30, 30, 40))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    

        w = weatherInfo[3].lower()
        if("cloudy" in w or "overcast" in w):
            cloudyBool = cloudy()
        elif("clear" in w):
            clearBool = clear()
        elif("fog" in w):
            windBlowing = foggMist()
        elif("drizzle" in w or "rain" in w or "shower" in w or "thunderstorm" in w):
            rainBool = rain()
        elif("snow" in w):
            windBlowing = snoww()
        
        
        
        weatherDislay(f"{weatherInfo[3]}", f"{weatherInfo[2]}", f"{weatherInfo[0]}")
        
        
        
        if rainBool and not rain_playing:
            rain_sound.play(loops=-1, maxtime=0)
            rain_playing = True
        elif not rainBool and rain_playing:
            rain_sound.stop()
            rain_playing = False
            
        if windBlowing:
            wind.play(loops=-1, maxtime=0)
        elif not windBlowing:
            wind.stop()
            
        if (clearBool or cloudyBool) and not clearPlaying:
            clear_sound.play(loops=-1, maxtime=0)
            clearPlaying = True
        elif (not clearBool and not cloudyBool) and clearPlaying:
            clear_sound.stop()
            clearPlaying = False

        pygame.display.flip()
        clock.tick(60)
        end = time.time()

pygame.quit()