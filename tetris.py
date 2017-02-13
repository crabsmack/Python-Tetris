#tetris.py

from Tkinter import *
import random
import copy

def tetrisMousePressed(canvas, event):
    pass

#calls appropriate function for each key press
def tetrisKeyPressed(canvas, event):
    if (event.keysym == "r"):
            tetrisInit(canvas)
    if canvas.data.isGameOver == False:
        if (event.keysym == "Up"):
            rotateFallingPiece(canvas)
        elif (event.keysym == "Down"):
            moveFallingPiece(canvas,+1, 0)
        elif (event.keysym == "Left"):
            moveFallingPiece(canvas,0,-1)
        elif (event.keysym == "Right"):
            moveFallingPiece(canvas,0,+1)
        tetrisRedrawAll(canvas)

#updates the game for every time unit
def tetrisTimerFired(canvas):
    if canvas.data.isGameOver == False:
        tetrisRedrawAll(canvas)
        if not(moveFallingPiece(canvas,1,0)):
            placeFallingPiece(canvas)
            removeFullRows(canvas)
            newFallingPiece(canvas)
            tetrisRedrawAll(canvas)
            if not(fallingPieceIsLegal(canvas)):
                canvas.data.isGameOver = True
                tetrisRedrawAll(canvas)
    delay = 250 # milliseconds
    def tetrisReTimer():
        tetrisTimerFired(canvas)
    canvas.after(delay, tetrisReTimer) # pause, then call tetrisTimerFired again

def tetrisRedrawAll(canvas):
    canvas.delete(ALL)
    drawGame(canvas)
    drawScore(canvas)

def drawScore(canvas):
    score,margin,cWidth,cHeight = canvas.data.score,canvas.data.margin,canvas.data.cWidth,canvas.data.cHeight
    canvas.create_text(cWidth/2, margin/2,text='Score: %s'%canvas.data.score, fill ='black', font= 'Times 10 bold')

def drawGame(canvas):
    rows,cols,cellSize,margin = canvas.data.rows,canvas.data.cols,canvas.data.cellSize,canvas.data.margin
    canvas.create_rectangle(0,0,canvas.data.cWidth,canvas.data.cHeight, fill ='grey40')
    drawBoard(canvas)
    drawFallingPiece(canvas)

def drawBoard(canvas):
    for col in xrange(canvas.data.cols):
        for row in xrange(canvas.data.rows):
            drawCell(canvas,row,col,canvas.data.board[row][col])
    if canvas.data.isGameOver == True:
        canvas.create_text(canvas.data.cWidth/2, canvas.data.cHeight/2,text='GAME OVER', fill ='white', font= 'Times 36 bold')

def drawCell(canvas,row,col,color):
    cellSize,margin = canvas.data.cellSize,canvas.data.margin
    canvas.create_rectangle(cellSize*col+margin,cellSize*row+margin,cellSize*(col+1)+margin,cellSize*(row+1)+margin,fill = color,width = 4)

#removes full rows and increases the score
def removeFullRows(canvas):
    rows,cols,board,emptyColor = canvas.data.rows, canvas.data.cols,canvas.data.board,canvas.data.emptyColor
    fullRows = 0
    newRow = rows-1
    for oldRow in xrange(rows-1,0,-1):
        if emptyColor in board[oldRow]:
            board[newRow] = copy.deepcopy(board[oldRow])
            newRow-=1
        else:
            fullRows+=1
    for fullRow in xrange(fullRows):
        board[fullRow] = [emptyColor]*cols
    canvas.data.score += int(fullRows**2.0)
    tetrisRedrawAll(canvas)

#creates a new falling piece
def newFallingPiece(canvas):
    randIndex = random.randint(0,len(canvas.data.tetrisPieces)-1)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[randIndex]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[randIndex]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2

def drawFallingPiece(canvas):
    piece, color, row, col = canvas.data.fallingPiece,canvas.data.fallingPieceColor,canvas.data.fallingPieceRow,canvas.data.fallingPieceCol
    for pieceRow in xrange(len(piece)):
        for pieceCol in xrange(len(piece[0])):
            if piece[pieceRow][pieceCol] == True:
                drawCell(canvas,row+pieceRow,col+pieceCol,color)

def moveFallingPiece(canvas,drow,dcol):
    canvas.data.fallingPieceRow+= drow
    canvas.data.fallingPieceCol+= dcol
    if not(fallingPieceIsLegal(canvas)):
        canvas.data.fallingPieceRow-= drow
        canvas.data.fallingPieceCol-= dcol
        return False
    return True

def rotateFallingPiece(canvas):
    fallingPiece,fallingPieceRow,fallingPieceCol = canvas.data.fallingPiece,canvas.data.fallingPieceRow,canvas.data.fallingPieceCol
    oldCenterRow,oldCenterCol = fallingPieceCenter(canvas)
    newFallingPiece= []
    rows,cols = len(fallingPiece), len(fallingPiece[0])
    for col in xrange(cols):
        newFallingPiece+= [getColumnList(fallingPiece,cols-col-1)]
    canvas.data.fallingPiece = newFallingPiece
    newCenterRow,newCenterCol = fallingPieceCenter(canvas)
    canvas.data.fallingPieceRow += (oldCenterRow-newCenterRow)
    canvas.data.fallingPieceCol += (oldCenterCol-newCenterCol)
    if not(fallingPieceIsLegal(canvas)):
        canvas.data.fallingPiece,canvas.data.fallingPieceRow,canvas.data.fallingPieceCol = fallingPiece,fallingPieceRow,fallingPieceCol

def getColumnList(list, col):
    colList = []
    for row in xrange(len(list)):
        colList+= [list[row][col]]
    return colList

#determines the center of the piece so as to appropriately rotate
def fallingPieceCenter(canvas):
    row = canvas.data.fallingPieceRow + len(canvas.data.fallingPiece)/2
    col = canvas.data.fallingPieceCol + len(canvas.data.fallingPiece[0])/2
    return (row,col)

def placeFallingPiece(canvas):
    piece, color, row, col, board = canvas.data.fallingPiece,canvas.data.fallingPieceColor,canvas.data.fallingPieceRow,canvas.data.fallingPieceCol, canvas.data.board
    for pieceRow in xrange(len(piece)):
        for pieceCol in xrange(len(piece[0])):
            if piece[pieceRow][pieceCol] == True:
                board[row+pieceRow][col+pieceCol] = color

def fallingPieceIsLegal(canvas):
    piece,board = canvas.data.fallingPiece,canvas.data.board
    fallingPieceRow,fallingPieceCol = canvas.data.fallingPieceRow, canvas.data.fallingPieceCol
    rows, cols, emptyColor = canvas.data.rows,canvas.data.cols,canvas.data.emptyColor
    for pieceRow in xrange(len(piece)):
        for pieceCol in xrange(len(piece[0])):
            if piece[pieceRow][pieceCol] == True:
                if pieceRow+fallingPieceRow < 0 or pieceCol+fallingPieceCol < 0:
                    return False
                if pieceRow+fallingPieceRow >= rows or pieceCol+fallingPieceCol >= cols:
                    return False
                if board[pieceRow+fallingPieceRow][pieceCol+fallingPieceCol] != emptyColor:
                    return False

    return True

def loadBoard(canvas):
    board = []
    for row in xrange(canvas.data.rows):
        board+= [[canvas.data.emptyColor]*canvas.data.cols]
    canvas.data.board= board

def tetrisInit(canvas):
    canvas.data.isGameOver = False
    canvas.data.emptyColor = 'blue'
    canvas.data.score = 0
    tetrisInitTetrominos(canvas)
    newFallingPiece(canvas)
    loadBoard(canvas)

def tetrisInitTetrominos(canvas):
    #Seven "standard" pieces (tetrominoes)
    iPiece = [  [True,  True,   True,   True]   ]
    jPiece = [  [True,  False,  False],
                [True,  True,   True]   ]
    lPiece = [  [False, False,  True],
                [True,  True,   True]   ]
    oPiece = [  [True,  True],
                [True,  True]   ]
    sPiece = [  [False, True,   True],
                [True,  True,   False]  ]
    tPiece = [  [False, True,   False],
                [True,  True,   True]   ]
    zPiece = [  [True,  True,   False],
                [False, True,   True]   ]
    canvas.data.tetrisPieces = [iPiece,jPiece,lPiece,oPiece,sPiece,tPiece,zPiece]
    canvas.data.tetrisPieceColors = ["red","yellow","magenta","pink","cyan","green","orange"]
    newFallingPiece(canvas)


def tetrisRun(rows, cols):
    # create the root and the canvas
    root = Tk()
    cellSize = 30
    margin = 20
    cWidth = margin*2+cellSize*cols
    cHeight = margin*2+cellSize*rows
    canvas = Canvas(root, width=cWidth, height=cHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Set up canvas data and call tetrisInit
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows, canvas.data.cols = rows,cols
    canvas.data.cellSize,canvas.data.margin= cellSize,margin
    canvas.data.cWidth,canvas.data.cHeight = cWidth,cHeight
    tetrisInit(canvas)
    # set up events
    root.bind("<Button-1>", lambda event: tetrisMousePressed(canvas, event))
    root.bind("<Key>", lambda event: tetrisKeyPressed(canvas, event))
    tetrisTimerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window)

tetrisRun(15,10)