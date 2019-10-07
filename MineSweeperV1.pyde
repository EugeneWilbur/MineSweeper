import random
import time

#Grid size
SIZE = 30
#Number of bombs
BOMBS = 120
#Width of each cell in the grid.
WIDTH = 20

#A list of the x and y that has to be added to the curretn cell to check its neighbourhood.
neighbourHood = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1,-1), (0,-1), (-1,-1)]
neighbourHoodBombs = 0

class Button:
    def __init__(self, type, state):
        self.type = type
        self.state = state

class Timer:
    def __init__(self):
        self.startTime = time.time()
        
    def restart(self):
        self.startTime = time.time()
        
    def getTime(self):
        return time.time() - self.startTime    
        
        

#Class for each cell (or square) in the grid.
class Cell:
    def __init__(self, bomb, vis, flagged, hood, x, y):
        self.bomb = bomb #Do I contain a bomb
        self.visible = vis #Can they see me
        self.flagged = flagged #Am I flagged (cannot be clicked and revealed until unflagged).
        self.hood = hood #How many bombs are around me
        self.x = x #Where am I
        self.y = y
    
    def newGame(self):
        self.bomb = False
        self.visible = False
        self.flagged = False
        self.hood = 0
        
 #all cells initialised to no bomb, no vision, not flagged, 0 neighbourhood bomb count and their x, y position
grid = [[Cell(False, False, False, 0, j, i) for i in range(SIZE)] for j in range(SIZE)] # start all cells with no bombs.
gameTimer = Timer()
resetButton = Button("reset", False)
countSet = 0

def main():
    loop()
    global countSet 
    countSet = 0
    for row in grid:
        for cell in row:
            cell.newGame()
    gameTimer.restart()

            
    #randomly places BOMB number of bombs
    for i in range(BOMBS):
        j = random.randint(0, SIZE -1)
        k = random.randint(0, SIZE -1)
        if grid[j][k].bomb == False: 
            grid[j][k].bomb = True
        else:
            i-=1      
    #finds what each cells neighbourhood bomb number is.
    for row in grid:
        for currentCell in row:
            neighbourHoodBombs = 0
            for (i,j) in neighbourHood:
                if 0 <= currentCell.x+i < SIZE and 0 <= currentCell.y+j < SIZE:
                    if grid[currentCell.x+i][currentCell.y+j].bomb == True:
                        neighbourHoodBombs += 1
            currentCell.hood = neighbourHoodBombs

#function for when a single bomb has been clicked on. (reveals all bombs).
def bombBlown():
    for i in grid:
        for currentCell in i:
            if currentCell.flagged:
                currentCell.flagged = False
            if currentCell.bomb:
                currentCell.visible = True
        
#draw function: constantly loops and draws the current state of the objects. 
#(This is an inbuild processing function, althought all the code inside has been developed by me)
def draw():
    fill(222,222,222)
    rect(0, 0, WIDTH * SIZE, 40)
    if resetButton.state:
        fill(190,190,190)
        rect((WIDTH * SIZE /2) - SIZE/2, 5, 30, 30)
        resetButton.state = False
    else:
        fill(211,211,211)
        rect((WIDTH * SIZE /2) - SIZE/2, 5, 30, 30)
    x = 0
    for i in grid:
        y = 40
        for currentCell in i:
            if currentCell.bomb and currentCell.visible and currentCell.flagged != True:
                bombBlown()
                fill(160,160,160)
                rect(x,y,WIDTH,WIDTH)
                fill(0)
                ellipse(x + WIDTH * 0.5,y + WIDTH * 0.5, WIDTH * 0.5, WIDTH * 0.5)
                fill(255,255,255)
                ellipse(x + WIDTH * 0.5, y + WIDTH * 0.4, 3, 3)
                global countSet 
                countSet += 1
                if countSet > 100:
                    noLoop()
            elif currentCell.visible and currentCell.flagged != True:
                fill(160,160,160)
                rect(x,y,WIDTH,WIDTH)
                if currentCell.hood > 0:
                    fill(0)
                    textAlign(CENTER)
                    textSize(WIDTH/2)
                    text(currentCell.hood, x + WIDTH * 0.5, y + WIDTH - 10)
            elif currentCell.flagged:
                beginShape()
                vertex(currentCell.x * WIDTH, (currentCell.y * WIDTH) + 40)
                vertex((currentCell.x + 1) * WIDTH, ((currentCell.y + 1) * WIDTH) + 40)
                endShape()
            else:
                fill(211,211,211)
                rect(x, y, WIDTH, WIDTH)
            y+=WIDTH
        x+=WIDTH
    fill(255,0,0)        
    textSize(16)
    text(int(gameTimer.getTime()),(WIDTH * SIZE) - SIZE, 27)



#Reveals the current neighbourhood
def revealHood(currentCell):
    for (i,j) in neighbourHood:
        if  0 <= currentCell.x+i < SIZE and 0 <=currentCell.y+j < SIZE:
            if grid[currentCell.x+i][currentCell.y+j].bomb != True and grid[currentCell.x+i][currentCell.y+j].visible != True and currentCell.bomb != True:
                getVision(grid[currentCell.x+i][currentCell.y+j])

#gives vision of a sinlge cell unless it is flagged. 
#If it has no bombs in its neighbourhood it calls the above revealHood function.
def getVision(currentCell):
    if currentCell.flagged != True:
        currentCell.visible = True
        if currentCell.hood == 0:
            revealHood(currentCell)
   
#flags right clicked cells, doenst allow them to be revealed when clicked on. Right clicking again will unflag.
def flagCell(currentCell):
    if currentCell.flagged != True and currentCell.visible != True:
        currentCell.flagged = True
    elif currentCell.flagged:
        currentCell.visible = False
        currentCell.flagged = False

#function for tracking mouse click (Processing function)            
def mousePressed():
    x = mouseX/WIDTH
    y = mouseY/WIDTH
    y -= 2
    if y < 0:
        menuClick(x, y)
    elif mouseButton == LEFT:
        getVision(grid[x][y])
    else:
        flagCell(grid[x][y])

def menuClick(x, y):
    if x >= 14 and x <= 15  and y >= -2 and y <= -1:
        #new game
        resetButton.state = True
        main()
    
#setup, starting function for processing. Mainly for window size.
def setup():
    size(SIZE * WIDTH + 1, SIZE * WIDTH + 41)
    
if __name__ == '__main__':
    main()
