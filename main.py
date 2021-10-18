import random
import math
import time
import tkinter as tk


# Class for every Block
class Block:
    def __init__(self, wall, row, column):
        self.wall = wall
        self.row = row
        self.column = column
        self.parent = -1
        self.heuristic = 0
        self.g = 0
        self.visited = False

    def getF(self):
        return self.heuristic + self.g

    def setParent(self, parent):
        self.parent = parent

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def setVisited(self, visited):
        self.visited = visited


# Function to get the value of radio buttons of whether the user wants final path or step by step
def selection():
    return int(radioVal.get())


# Function to make the grid drawable
def setDraw():
    print("HII")
    root.bind("<Button-1>", lambda event: leftOnRoot(event))


# When root is left clicked after grid is generated draw is activated
def leftOnRoot(event):
    global draw
    if not draw and canDraw:
        print("Bye")
        for i in range(len(blockList)):
            for j in range(len(blockList[0])):
                labelsList[i][j].bind("<Enter>", lambda event, r=i, c=j: leftClickOnLabel(event, r, c))
        print("Bye2")
        draw = True
    else:
        print("FORBIDDEN")
        for i in range(len(blockList)):
            for j in range(len(blockList[0])):
                labelsList[i][j].unbind("<Enter>")
        draw = False


# Function that generates the grid
def generateGrid(rows, columns, randomGen):
    global labelsList, blockList, startChosen, goalChosen
    startChosen = False
    goalChosen = False
    randomGeneration = False
    for boxes in gridFrame.winfo_children():
        boxes.destroy()

    labelsList = [[1 for j in range(columns)] for i in range(rows)]
    blockList = [[1 for j in range(columns)] for i in range(rows)]

    for i in range(rows):
        for j in range(columns):
            frame = tk.Frame(gridFrame, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i, column=j)
            blockList[i][j] = Block(False, i, j)
            labelsList[i][j] = tk.Label(master=frame, text="", height=1, width=2, bg="white")
            labelsList[i][j].pack()
            # labelsList[i][j].bind("<Enter>", lambda event, r=i, c=j: leftClickOnLabel(event, r, c))
            labelsList[i][j].bind("<Button-3>", lambda event, r=i, c=j: rightClickOnLabel(event, r, c))

    setDraw()

    if randomGen:
        for i in range(rows):
            for j in range(columns):
                x = random.randint(0, 9)
                if x < 4:
                    leftClickOnLabel("ss", i, j)


# If the user wants to specify the grid's dimensions, the program will go to this function before generateGrid
def specifiedButtonHandler(randomGen = False):
    row = str(rowsInput.get(1.0, "end-1c"))
    column = str(columnsInput.get(1.0, "end-1c"))
    if not row.isdigit():
        print("Error: Enter a digit between 2 and 20")
    else:
        if int(row) < 2 or int(row) > 40:
            print("Error: Number isn't in the interval [2, 20]")
        else:
            if not column.isdigit():
                print("Error: Enter a digit between 2 and 20")
            else:
                if int(column) < 2 or int(column) > 40:
                    print("Error: Number isn't in the interval [2, 20]")
                else:
                    if not randomGen:
                        generateGrid(int(row), int(column), False)
                    else:
                        generateGrid(int(row), int(column), True)


# Function that calls specifiedButtonHandler that makes random walls (40% chance of getting a wall in a block)
def randomGenerationHandler():
    specifiedButtonHandler(True)


# Function that decides whether a block should turn into a wall or an empty block
def leftClickOnLabel(event, i, j):
    global startChosen, goalChosen
    # print(labelsList[i][j].cget("bg"))
    if labelsList[i][j].cget("bg") == "white":
        labelsList[i][j].config(bg="black")
        blockList[i][j].wall = True
    else:
        labelsList[i][j].config(bg="white")
        blockList[i][j].wall = False

    if labelsList[i][j].cget("text") == "S":
        labelsList[i][j].config(text="")
        startChosen = False
    if labelsList[i][j].cget("text") == "G":
        labelsList[i][j].config(text="")
        goalChosen = False

    root.update()
    print(blockList[i][j])


# Function that allows the user to set the start and goal by right clicking the block
def rightClickOnLabel(event, i, j):
    global startChosen, goalChosen, startLocation, goalLocation, startBlock, goalBlock

    if labelsList[i][j].cget("bg") == "black":
        print("Can't assign anything")
    elif labelsList[i][j].cget("text") == "S":
        labelsList[i][j].config(text="")
        startChosen = False
    elif labelsList[i][j].cget("text") == "G":
        labelsList[i][j].config(text="")
        goalChosen = False
    elif not startChosen:
        labelsList[i][j].config(text="S")
        startChosen = True
        startLocation = [i, j]
        startBlock = blockList[i][j]
    elif not goalChosen:
        labelsList[i][j].config(text="G")
        goalChosen = True
        goalLocation = [i, j]
        goalBlock = blockList[i][j]

    # print(startLocation)
    # print(startChosen)
    # print(goalLocation)
    # print(goalChosen)
    # print(blockList[i][j].wall)


# Function that executes after clicking start simulation button
def startButtonHandler():
    global canDraw
    canDraw = False
    stepByStep = False
    if selection() == 1:
        stepByStep = True
    leftOnRoot("ss")
    clearPathsAndParents()
    if startChosen and goalChosen:
        result = aStar()
        result[0].append(blockList[startLocation[0]][startLocation[1]])
        labelsList[startLocation[0]][startLocation[1]].config(text="S")
        labelsList[goalLocation[0]][goalLocation[1]].config(text="G")
        if not result:
            print("No path to goal")
        elif stepByStep:
            for x in result[1]:
                if isinstance(x, list):
                    for y in x:
                        labelsList[y.row][y.column].config(bg="yellow")
                    root.update()
                    time.sleep(0.005)
                else:
                    labelsList[x.row][x.column].config(bg="orange")

            for x in result[0]:
                labelsList[x.row][x.column].config(bg="cyan")
                root.update()
                time.sleep(0.005)
        else:
            for x in result[0]:
                labelsList[x.row][x.column].config(bg="cyan")
                root.update()
        canDraw = True


# Resets the grid when clicking start simulation button
def clearPathsAndParents():
    for i in range(len(blockList)):
        for j in range(len(blockList[0])):
            blockList[i][j].visited = False
            blockList[i][j].parent = -1
            if not blockList[i][j].wall:
                labelsList[i][j].config(bg="white")
    root.update()


# A* Algorithm
def aStar():
    timeStart = time.time()
    leastFlist = [blockList[startLocation[0]][startLocation[1]]]
    moves = []
    while leastFlist:
        currentBlock = getLeastF(leastFlist)
        currentBlock.visited = True
        moves.append(currentBlock)

        if currentBlock == blockList[goalLocation[0]][goalLocation[1]]:
            path = []
            while currentBlock.parent != -1:
                path.append(currentBlock)
                currentBlock = currentBlock.parent
            timeEnd1 = time.time()
            timeSpent.config(text="{:.4f}".format(timeEnd1 - timeStart))
            pathLength.config(text=str(len(path)))
            return [path, moves]

        neighborList = getNeighbor(currentBlock)
        moves.append(neighborList)
        for nBlock in neighborList:
            if not nBlock.visited:
                estimatedG = currentBlock.g + estimateDistance(currentBlock, nBlock)
                nBlock.heuristic = estimateDistance(nBlock, blockList[goalLocation[0]][goalLocation[1]])
                if estimatedG < nBlock.g or not leastFlist.__contains__(nBlock):
                    nBlock.g = estimatedG
                    nBlock.parent = currentBlock
                if not leastFlist.__contains__(nBlock):
                    leastFlist.append(nBlock)
    timeEnd2 = time.time()
    timeSpent.config(text="{:.4f}".format(timeEnd2 - timeStart))
    pathLength.config(text="0")
    return []


# Function that gets least F in queue (If multiple blocks have least F it returns least heuristic of them)
def getLeastF(queue):
    minIndex = 0
    leastFList = []
    for x in range(len(queue)):
        if queue[x].getF() < queue[minIndex].getF():
            minIndex = x
    for x in queue:
        if x.getF() == queue[minIndex].getF():
            leastFList.append(x)
    if len(leastFList) == 1:
        return queue.pop(minIndex)
    else:
        minH = 0
        for x in range(len(leastFList)):
            if leastFList[x].heuristic < leastFList[minH].heuristic:
                minH = x
        queue.remove(leastFList[minH])
        return leastFList[minH]


# Gets the euclidean distance between two blocks
def estimateDistance(blockA, blockB):
    # distance = int(math.fabs(blockA.row - blockB.row) + math.fabs(blockA.column - blockB.column))
    distance = math.sqrt((blockA.row - blockB.row)**2+(blockA.column - blockB.column)**2)
    return distance


# Returns the neighbors of a specific block (Unless neighbor is wall)
def getNeighbor(block):
    neighbors = []
    totalRows = len(blockList)
    totalColumns = len(blockList[0])
    row = block.row
    column = block.column
    if 0 <= row - 1:
        if not blockList[row-1][column].wall and blockList[row-1][column].parent == -1:
            neighbors.append(blockList[row-1][column])
    if row + 1 < totalRows:
        if not blockList[row+1][column].wall and blockList[row+1][column].parent == -1:
            neighbors.append(blockList[row+1][column])
    if 0 <= column - 1:
        if not blockList[row][column-1].wall and blockList[row][column-1].parent == -1:
            neighbors.append(blockList[row][column-1])
    if column + 1 < totalColumns:
        if not blockList[row][column+1].wall and blockList[row][column+1].parent == -1:
            neighbors.append(blockList[row][column+1])

    return neighbors


# Initializing an empty list of labels and blocks, and initializing variables for start and goal block and draw
labelsList = []
blockList = []
draw = False
canDraw = True
startChosen = False
goalChosen = False
startBlock = Block(False, -1, -1)
goalBlock = Block(False, -1, -1)
startLocation = [0, 0]
goalLocation = [0, 0]

# Making the window and the frames (All of the below is for the GUI)
root = tk.Tk()
root.title("A* Path Finder")
mainFrame = tk.Frame(root)
gridFrame = tk.Frame(mainFrame)
buttonsFrame = tk.Frame(mainFrame, height=100, width=700)
buttonsFrame.propagate(False)


# Adding the frames to the window
mainFrame.pack()
gridFrame.pack()
buttonsFrame.pack(side=tk.BOTTOM)

# Instructions for using various functions of the program
instructions1L = tk.Label(buttonsFrame, text="Left-click to draw a walls, Left-click again to stop")
instructions1L.grid(row=1, column=0, padx=8, pady=3)

instructions2L = tk.Label(buttonsFrame, text="Right-click a block to add the start/goal")
instructions2L.grid(row=0, column=0, padx=8, pady=3)

# Start simulation button
startButton = tk.Button(buttonsFrame, text="Start Simulation", command=startButtonHandler)
startButton.grid(row=0, column=2, padx=5, pady=3)

# Blank label to add space between two buttons
blankL = tk.Label(buttonsFrame, text="           ")
blankL.grid(row=0, column=3, padx=5, pady=3)

# Button for generating a random grid
randomGridButton = tk.Button(buttonsFrame, text="Generate a Random Grid", command=randomGenerationHandler)
randomGridButton.grid(row=0, column=4, padx=5, pady=3)

# Radio buttons for 2 options (Step by Step, Final Path)
radioVal = tk.IntVar()
R1 = tk.Radiobutton(buttonsFrame, text="Step by Step", variable=radioVal, value=1,command=selection)
R1.grid(row=1, column=1, padx=5, pady=3)

R2 = tk.Radiobutton(buttonsFrame, text="Final Path", variable=radioVal, value=2, command=selection)
R2.grid(row=1, column=2, padx=5, pady=3)

radioVal.set(2)     # Make (Final Path) the default option

# Button for specifying the dimensions of the grid
specifyGridButton = tk.Button(buttonsFrame, text="Specify Blank Grid", command=specifiedButtonHandler)
specifyGridButton.grid(row=1, column=4, padx=5, pady=3)

# rows and columns labels and inputs
rowsL = tk.Label(buttonsFrame, text="Rows(2 to 40): ")
rowsL.grid(row=1, column=5, padx=5, pady=3)

rowsInput = tk.Text(buttonsFrame, height=1, width=3)
rowsInput.grid(row=1, column=6, padx=5, pady=3)

columnsL = tk.Label(buttonsFrame, text="Columns(2 to 40): ")
columnsL.grid(row=1, column=7, padx=5, pady=3)

columnsInput = tk.Text(buttonsFrame, height=1, width=3)
columnsInput.grid(row=1, column=8, padx=5, pady=3)

# Time spent labels and Path length labels
timeLabel = tk.Label(buttonsFrame, text="Time: ")
timeLabel.grid(row=0, column=9, padx=8, pady=3)

timeSpent = tk.Label(buttonsFrame, text="0.0000")
timeSpent.grid(row=0, column=10, padx=8, pady=3)

pathLabel = tk.Label(buttonsFrame, text="Path length: ")
pathLabel.grid(row=1, column=9, padx=8, pady=3)

pathLength = tk.Label(buttonsFrame, text="")
pathLength.grid(row=1, column=10, padx=8, pady=3)


# This function keeps the GUI running until the user clicks the X button
root.mainloop()
