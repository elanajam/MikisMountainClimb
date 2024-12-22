#################################################
#mikisMountainMarathon_TP1.py
#
# Your name: Elana Jasmine Mohamad Firdaus
# Your andrew id: elanajam
#################################################

from cmu_graphics import *
import random
import copy
from PIL import Image
import os, pathlib

#################################################
# Classes
#################################################

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 16
        self.dx = 3
        self.crX, self.crY = getPointInDir(self.x, self.y, 105, 40)
        self.clX, self.clY = getPointInDir(self.x, self.y, 255, 40)
    
    def draw(self, app):
        drawCircle(self.x, self.y, 30, fill='white')
        drawCircle(self.crX, self.crY, 25, fill='white')
        drawCircle(self.clX, self.clY, 25, fill='white')
    
    def onStep(self, app):
        self.x += self.dx
        self.crX += self.dx
        self.clX += self.dx

class Miki:
    def __init__(self, x, y, spriteStrip):
        self.x = x
        self.y = y
        self.r = 32
        self.spriteCenter = self.y + 16
        self.dy = 0
        self.ddy = 0.9
        self.isGripping = False
        self.sprites = [[], [], [], [], [], [], [], []]
        self.spriteCount = 0
        self.scale = 2
        self.spriteType = 0
        self.spriteDic = {0:8, #idle facing right
                          1:4, #walking right
                          2:2, #jumping right
                          3:2, #falling right
                          4:8, #idle facing left
                          5:4, #walking left
                          6:2, #jumping left
                          7:2} #falling left
        self.loadSprite(spriteStrip)
    
    #below function was taken and adapted from Mohamed Shikfa
    def openImage(self, fileName):
        pilImage = Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        newWidth = pilImage.width * self.scale
        newHeight = pilImage.height * self.scale
        pilImage = pilImage.resize((newWidth, newHeight))
        return CMUImage(pilImage)
    
    def loadSprite(self, spriteStrip):
        spritestrip = self.openImage(spriteStrip)
        pilImage = spritestrip.image
        
        for i in range(8):
            for j in range(self.spriteDic[i]):
                sprite = pilImage.crop((32 * j * self.scale, #x-top
                                        32 * i * self.scale, #y-top
                                        (32 * self.scale) + 32 * j * self.scale, #x-bottom
                                        (32 * self.scale) + 32 * i * self.scale)) #y-bottom
            
                self.sprites[i].append(CMUImage(sprite))
    
    def draw(self, app):

        currentSprite = self.sprites[self.spriteType][self.spriteCount]
        drawImage(currentSprite, self.x, self.y, align='center')
        
    #function below is from lectures_demos_qatar/week12/oopy_jump.py
    def onStep(self, app):
        self.dy += self.ddy
        self.y += self.dy
        
        if self.y + self.r > app.ground:
            self.y = app.ground - self.r
            self.dy = 0
        
        #below is taken and adapted from Mohamed Shikfa
        spriteLength = self.spriteDic[self.spriteType]
        self.spriteCount += 1
        self.spriteCount %= spriteLength

    #checks in miki is on the ground        
    def onGround(self, app):
        return self.y + self.r == app.ground
    
    #below function is taken from lectures_demos_qatar/week12/oopy_jump.py
    def isColliding(self, other):
        d = distance(self.x, self.y, other.x, other.y)
        if d <= self.r + other.r:
            return True
        else:
            return False
        
    def inSnow(self, other):
        d = distance(self.x, self.y, other.x, other.y)
        if d <= 13:
            return True
        else:
            return False
    
    #checks if miki is in the wind  
    def inWind(self, other):
        if self.y >= other.y - 10 and self.y <= other.y + 10:
            return True
        else:
            return False    
    
class RockGrip:
    
    def __init__(self, x, y, rockImage):
        self.x = x
        self.y = y
        self.scale = 5
        self.image = self.openImage(rockImage)
        
    #below function was taken and adapted from Mohamed Shikfa
    def openImage(self, fileName):
        pilImage = Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        newWidth = pilImage.width // self.scale
        newHeight = pilImage.height // self.scale
        pilImage = pilImage.resize((newWidth, newHeight))
        self.width = newWidth
        self.height = newHeight
        return CMUImage(pilImage)
        
    def draw(self, app):
        drawImage(self.image, self.x, self.y, align='center')
        
class Coin:
    
    def __init__(self, x, y, coinImage):
        self.x = x
        self.y = y
        self.scale = 3
        self.image = self.openImage(coinImage)
        
    def openImage(self, fileName):
        pilImage = Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        newWidth = pilImage.width // self.scale
        newHeight = pilImage.height // self.scale
        pilImage = pilImage.resize((newWidth, newHeight))
        self.width = newWidth
        self.height = newHeight
        self.r = self.height//2
        return CMUImage(pilImage)        
        
    def draw(self, app):
        drawImage(self.image, self.x, self.y, align='center')
        
class Heart:
    def __init__(self, x, y, rockImage):
        self.x = x
        self.y = y
        self.scale = 5
        self.image = self.openImage(rockImage)
        
    def openImage(self, fileName):
        pilImage = Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        newWidth = pilImage.width // self.scale
        newHeight = pilImage.height // self.scale
        pilImage = pilImage.resize((newWidth, newHeight))
        return CMUImage(pilImage)
        
    def draw(self, app):
        drawImage(self.image, self.x, self.y, align='center')
       
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 30
        self.dy = 1
        self.ddy = 0.1
        
    def draw(self, app): #draws snowball
        drawCircle(self.x, self.y, self.r, fill='white', border='black',
                   borderWidth=2)
        
    def onStep(self):
        self.dy += self.ddy
        self.y += self.dy
        
class WindGust:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([-1, 1])
        self.force = 3
    
    def draw(self, app):
        drawRect(self.x, self.y, app.width, 20, fill='skyBlue', opacity=50,
                 align='center')
        if self.direction == -1:
            drawLine(app.mountTopLeftX, self.y, 
                     app.mountTopRightX, self.y,
                     fill='skyBlue', lineWidth = 2, arrowStart = True,
                     arrowEnd = False)

        elif self.direction == 1:
            drawLine(app.mountTopLeftX, self.y, 
                     app.mountTopRightX, self.y,
                     fill='skyBlue', lineWidth = 2, arrowStart = False,
                     arrowEnd = True)

#################################################
# Controllers
#################################################

def restartAll(app):
    app.steps = 0
    app.margin = 8
    app.mountTopLeftX = app.width/app.margin
    app.mountTopRightX = app.width - app.mountTopLeftX
    app.coverPage = True
    app.menuPage = False
    app.shopPage = False
    app.tutorialPage = False
    app.gamePage = False
    app.totalCoins = 0
    app.powerUps = {
        'highJump': 10, #jump higher than usual
        'shield': 5, #protects from snowballs and wind gusts
        'rockPlacer': 20 #place a rock within reach
        }
    app.inventory = {
        'highJump': 5,
        'shield': 5,
        'rockPlacer': 5
        }
    app.highestScore = loadHighestScore("scoreHistory.txt")

def replayGame(app):
    app.clouds = []
    app.clouds.append(Cloud(0, random.randint(50, 400)))
    app.miki = Miki(app.width//2, app.height-32, 'images/kitty.png')
    app.rocks = [[], [], []]
    app.coins = [[], [], []]
    app.coinPosition = copy.copy(app.coins)
    app.obstacles = []
    app.wind = []
    app.ground = app.height
    app.lives = 4
    app.hearts = [Heart(50, 30, "images/heart.png"),
                  Heart(50, 80, "images/heart.png"),
                  Heart(50, 130, "images/heart.png"),
                  Heart(50, 180, "images/heart.png")]
    app.isGameOver = False
    app.firstMove = False
    app.respawnX = None
    app.respawnY = None
    app.score = 0
    app.shield = False
    app.shieldTimer = 0
    app.testCoin = Coin(50, 512, "images/coin.png")
    app.highestScore = 0
    app.windGustActive = False
    app.windGustTime = 0
    app.RockPlacer = False
    app.tempRockPlacer = []
    app.tempRockTimer = 0
    app.highJump = False
    app.highJumpTimer = 0
    
def onAppStart(app):
    restartAll(app)
    replayGame(app)

def onKeyPress(app, key):
    if 'r' == key: #resets the whole application
        restartAll(app)

    elif 'p' == key and app.isGameOver == True: #resets the game only
        app.totalCoins += app.score
        print(f'total coins: {app.totalCoins}')
        replayGame(app)

    elif 'm' == key and app.isGameOver == True: #return to the menu
        app.totalCoins += app.score
        print(f'total coins: {app.totalCoins}')
        app.coverPage = False
        app.menuPage = True
        app.shopPage = False
        app.tutorialPage = False
        app.gamePage = False

    #activate the high jump power up
    elif '1' == key and app.inventory['highJump'] >= 1:
        app.highJump = True
    
    #activate the shield power up
    elif '2' == key and app.inventory['shield'] >= 1:
            app.shield = True
            app.inventory['shield'] -= 1
    
    #activate the rock power up        
    elif '3' == key and app.inventory['rockPlacer'] >= 1:
        app.rockPlacer = True
        rockType = random.choice(["images/crimp.png",
                                  "images/footholder.png", "images/jug.png",
                                  "images/pinch.png",
                                  "images/undercling.png",
                                  "images/sidepull.png"])
        app.tempRockPlacer.append(RockGrip(app.miki.x, app.miki.y, rockType))
        app.inventory['rockPlacer'] -= 1

    elif 'a' == key:
        print(len(app.rocks[0]))
        
def onKeyHold(app, keys):
    if app.isGameOver == False:
        if "right" in keys and app.miki.x + 25 <= app.mountTopRightX:
            app.miki.x += 4

        if "left" in keys and app.miki.x - 25 >= app.mountTopLeftX:
            app.miki.x -= 4

        if "up" in keys and app.miki.onGround(app) and len(app.rocks[0]) >= 4 \
        and app.miki.y - app.miki.r >= 0:
            if app.highJump == False:
                app.miki.dy = -15
                app.firstMove = True
            elif app.highJump == True:
                app.miki.dy = -20
                app.firstMove = True
         
def onMousePress(app, mouseX, mouseY):

    #transition from cover page to menu page
    if mouseX > 242 and mouseX < 558 and mouseY > 232 \
        and mouseY < 368 and app.coverPage == True:
        app.coverPage = False
        app.menuPage = True
        app.shopPage = False
        app.tutorialPage = False

    #transition from menu page to tutorial page
    elif mouseX > 301 and mouseX < 461 and mouseY > 59 \
        and mouseY < 134 and app.menuPage == True:
        app.coverPage = False
        app.menuPage = False
        app.shopPage = False
        app.tutorialPage = True

    #transition from menu page to shop page
    elif mouseX > 303 and mouseX < 462 and mouseY > 158 \
        and mouseY < 233 and app.menuPage == True:
        app.coverPage = False
        app.menuPage = False
        app.shopPage = True
        app.tutorialPage = False
        
    #transition from menu page to game page
    elif mouseX > 302 and mouseX < 462 and mouseY > 256 \
        and mouseY < 331 and app.menuPage == True:
        app.coverPage = False
        app.menuPage = False
        app.shopPage = False
        app.tutorialPage = False
        app.gamePage = True
        replayGame(app)

    #transition from shop page to menu page
    elif mouseX > 10 and mouseX < 78 and mouseY > 9 \
        and mouseY < 75 and app.shopPage == True:
        app.coverPage = False
        app.menuPage = True
        app.shopPage = False
        app.tutorialPage = False
        app.gamePage = False

    #transition from tutorial page to menu page
    elif mouseX > 10 and mouseX < 78 and mouseY > 9 \
        and mouseY < 75 and app.tutorialPage == True:
        app.coverPage = False
        app.menuPage = True
        app.shopPage = False
        app.tutorialPage = False
        app.gamePage = False

    #purchasing highJump
    elif mouseX > 106 and mouseX < 213 and mouseY > 427 \
        and mouseY < 479 and app.shopPage == True:
        if app.totalCoins >= app.powerUps['highJump']:
            app.inventory['highJump'] += 1
            app.totalCoins -= app.powerUps['highJump']
        else:
            print('not enough coins!')
        
    #purchasing shield
    elif mouseX > 347 and mouseX < 453 and mouseY > 426 \
        and mouseY < 479 and app.shopPage == True:
        if app.totalCoins >= app.powerUps['shield']:
            app.inventory['shield'] += 1
            app.totalCoins -= app.powerUps['shield']
        else:
            print('not enough coins!')

    #purchsing rockPlacer
    elif mouseX > 587 and mouseX < 694 and mouseY > 428 \
        and mouseY < 480 and app.shopPage == True:
        if app.totalCoins >= app.powerUps['rockPlacer']:
            app.inventory['rockPlacer'] += 1
            app.totalCoins -= app.powerUps['rockPlacer']
        else:
            print('not enough coins!')  

#the function below was adapted from lecture_demos_qatar/week08/sets-example.py
#this function reads the txt file that keeps the highest score ever
def loadHighestScore(filename):
    with open(filename, "r") as number:
        theScore = number.read()
    return int(theScore)

#################################################
# Visuals
#################################################

#the function below is what I wrote during the F24 Exam 1 free response question        
def drawBricks(app, x, y):
    brickWidth, brickHeight = 60, 30
    startY = y
    
    for row in range(0, 20, 2):
        
        for col in range(10):
            startX = x
            drawRect(startX + col*brickWidth, startY + row*brickHeight,
                     brickWidth, brickHeight,
                     fill=None, border='peru', borderWidth=2)
            
    for row in range(1, 21, 2):
        
        for col in range(9):
            startX = x + (brickWidth//2)
            drawRect(startX + col * brickWidth, startY + row*brickHeight,
                     brickWidth, brickHeight, fill=None, border='peru',
                     borderWidth=2)
            
    for row in range(1, 21, 2):
        drawRect(x, startY + row*brickHeight, brickWidth//2, brickHeight,
                 fill=None, border='peru', borderWidth=2)

    for row in range(1, 21, 2):
        drawRect(670, startY + row*brickHeight, brickWidth//2, brickHeight,
                 fill=None, border='peru', borderWidth=2)
        
def redrawAll(app):
    #draw cover page
    if app.coverPage == True:
        drawImage("images/cover.png", 0, 0)
        drawRect(app.width//2, app.height//2, app.width//2, 140,
                 fill=None, align='center')
    
    #draw menu page
    if app.menuPage == True:
        drawImage("images/menu.png", 0, 0)
        drawLabel(f"{loadHighestScore('scoreHistory.txt')}", 375, 513, size=20)

    #draw shop page
    if app.shopPage == True:
        drawImage("images/shop.png", 0, 0)
        drawLabel(f'{app.totalCoins}', 648, 42, size=20, align='left')
    
    #draw tutorial page
    if app.tutorialPage == True:
        drawImage("images/tutorial.png", 0, 0)
    
    #draw game page
    if app.gamePage == True:
        #draw the background: sky, clouds, and wall
        drawRect(0, 0, app.width, app.height,
                 fill=gradient('deepSkyBlue', 'skyBlue', 'lightSkyBlue',
                               start='top'))
        
        for clouds in app.clouds:
            clouds.draw(app)
        
        drawRect(app.mountTopLeftX, 0, 6 * app.mountTopLeftX, app.height,
                 fill=gradient('saddleBrown', 'sienna', start='top-left'))
            
        #brick texture in wall
        drawBricks(app, 100, 0)
        
        for c in range(3):
            for rock in app.rocks[c]:
                rock.draw(app)
            for coin in app.coins[c]:
                coin.draw(app)
        for rock in app.tempRockPlacer:
            rock.draw(app)

        for w in app.wind:
            w.draw(app)
        
        app.miki.draw(app)
        
        if app.shield == True:
            drawCircle(app.miki.x, app.miki.y + 16, 22, fill='purple', 
                       opacity=50, border='pink', borderWidth=2,
                       align='center')
            
        for obstacle in app.obstacles:
            obstacle.draw(app)
            
        for h in app.hearts:
            h.draw(app)
            
        app.testCoin.draw(app)

        #drawing the inventory
        drawImage("images/inventory.png", 0, 280)
        drawLabel(f"{app.inventory['highJump']}", 63, 326, 
                  size=18, align='left')
        drawLabel(f"{app.inventory['shield']}", 63, 380, 
                  size=18, align='left')
        drawLabel(f"{app.inventory['rockPlacer']}", 63, 438, 
                  size=18, align='left')
        
        drawLabel(f'{app.score}', 50, app.height-50, size=20)
        
        if app.isGameOver == True:
            drawRect(0, 0, app.width, app.height, fill='black', opacity=25)
            drawLabel('Game Over!',
                      400, 250, size=20,
                      fill='pink', font='arial', bold=True)
            drawLabel('Press p to play again', 400, 300, size=20,
                      fill='pink', font='arial', bold=True)
            drawLabel('Press m to go back to main menu', 400, 350,
                      size=20, fill='pink', font='arial', bold=True)

def mikiOnRock(app, x, y, width, height):
    rx = x
    ry = y
    rWidth = width
    rHeight = height
    
    if (app.miki.x >= rx - rWidth//2) and (app.miki.x <= rx + rWidth//2) and \
    (app.miki.y >= ry - rHeight//2) and (app.miki.y <= ry + rHeight//2):
        return True
    
    return False

# Controller
def onStep(app):
    if app.isGameOver == True:
        if app.score > app.highestScore:
            app.highestScore = app.score
            with open("scoreHistory.txt", "w") as number:
                number.write(str(app.highestScore))


        return
    
    if app.gamePage == True:
        app.steps += 1
    
        #SECTION 1: CLOUDS (new clouds and moving them)
        if app.steps % 120 == 0:
            app.clouds.append(Cloud(0, random.randint(50, 400)))
        
        for cloud in app.clouds:
            cloud.onStep(app)
            
            if cloud.clX > app.width:
                app.clouds.pop(0)
            
        app.miki.onStep(app)
    
        #SECTION 2: NEW ROCK GRIPS
        
        #every 2 seconds, add new rock and coin on the wall, in each coloum
        if app.steps % 60 == 0:
            for c in range(3):
                n = 2 * (c + 1)
                lowerBound = (n - 1) * 100
                upperBound = (n + 1) * 100
                rockX = random.randint(lowerBound, upperBound)
                rockType = random.choice(["images/crimp.png",
                                        "images/footholder.png", "images/jug.png",
                                        "images/pinch.png",
                                        "images/undercling.png",
                                        "images/sidepull.png"])
                app.rocks[c].append(RockGrip(rockX, 0, rockType))
                app.coins[c].append(Coin(rockX, -35, "images/coin.png"))


        #SECTION 3: OBSTACLES
        
        #add obstacles every 10 seconds
        if app.steps % 150 == 0:
            obsX = random.randint(app.mountTopLeftX + 20, app.mountTopRightX - 20)
            app.obstacles.append(Obstacle(obsX, 0))
            
        for obstacle in app.obstacles:
            obstacle.onStep()
            if obstacle.y >= app.height:
                app.obstacles.pop(0)
    
        #SECTION 4: ROCK LOGICS
        #shift rocks/coins down every step, and remove from list if outside window
        for col in range(3):
            
            for rock in app.rocks[col]:
                #shift the rocks/coins down every step
                rock.y += 2
            
                #remove rock if reaches bottom of screen
                if rock.y - rock.height//2 > app.height:
                    app.rocks[col].pop(0)
                    
            for coin in app.coins[col]:
                coin.y += 2
                
                if coin.y - coin.height//2 > app.height:
                    app.coins[col].pop(0)
            
        foundGrip = False
        
        for col in range(3):
            
            for rock in app.rocks[col]:
                
                if mikiOnRock(app, rock.x, rock.y, rock.width, rock.height):
                    app.ground = app.miki.y + app.miki.r
                    foundGrip = True
                    break
                
            if foundGrip:
                app.respawnX = app.miki.x
                app.respawnY = app.miki.y
                break
        
        for rock in app.tempRockPlacer:
            if mikiOnRock(app, rock.x, rock.y, rock.width, rock.height):
                app.ground = app.miki.y + app.miki.r
                foundGrip = True
                break

        if foundGrip == False:
            app.ground = app.height

            
        #SECTION 5: COLLISION WITH OBSTACLES AND COINS
        if app.shield == False:
            for o in app.obstacles:
                if app.miki.isColliding(o):
                    app.obstacles.pop(0)
                    app.lives -= 1
                    app.hearts.pop()
                    print('OUCH!', app.lives, 'left')

                if o.y + o.r >= app.height:
                    app.obstacles.pop(0)
        
        for col in range(3):
            removeCoins = []      
            for coin in app.coins[col]:
                if app.miki.isColliding(coin):
                    removeCoins.append(coin)
                    app.score += 1

            for coin in removeCoins:
                app.coins[col].remove(coin)
            
        
        #SECTION 6: FALLING OFF THE ROCKS
                
        #if miki fall off a rock and touches the bottom, he looses a life
        
        #he should spawn back on the lowest rock
        if app.firstMove == True:
            if app.miki.y + app.miki.r == app.height:
                
                if app.respawnX == None and app.respawnY == None:
                    app.miki.x = app.rocks[1][1].x
                    app.miki.y = app.rocks[1][1].y
                elif app.respawnX != None and app.respawnY != None:
                    app.miki.x = app.respawnX
                    app.miki.y = app.respawnY
                    
                app.lives -= 1
                app.hearts.pop()

        #prevents miki from jumping higher than the screen height
        if app.miki.y <= 0:
            app.miki.y = 0
            
        #SECTION 7: WIND GUSTS
        #wind stream appear every 10 seconds
        if app.steps % 300 == 0:
            windY = random.randint(50, app.height - 50)
            app.wind.append(WindGust(400, windY))
            app.windGustActive = True
            
        if app.shield == False:
            for w in app.wind:
                if app.miki.inWind(w):
                    app.miki.x += (w.direction * w.force)
    
        #wind stream dissapears every 5 seconds
        if app.windGustActive == True:
            app.windGustTime += 1

            if app.windGustTime % 150 == 0:
                app.wind.pop(0)
                app.windGustActive = False
        
        #SECTION 8: DEALING WITH TEMPORARY ROCKS
        if len(app.tempRockPlacer) >= 1:
            app.tempRockTimer += 1
            if app.tempRockTimer % 120 == 0:
                app.tempRockPlacer.pop(0)

        #SECTION 9: SHIELD TIMER 5 seconds
        if app.shield == True:
            app.shieldTimer += 1
            if app.shieldTimer % 150 == 0:
                app.shield = False

        #SECTION 10: HIGHJUMP TIMER 5 seconds
        if app.highJump == True:
            app.highJumpTimer += 1
            if app.highJumpTimer % 150 == 0:
                app.highJump = False

        #check for game over status
        if app.lives == 0:
            app.isGameOver = True

        if len(app.rocks[0]) == 6 and app.firstMove == False:
             app.isGameOver = True

runApp(width=800, height=600)