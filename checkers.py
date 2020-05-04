import pygame

#Rules used: https://www.thesprucecrafts.com/play-checkers-using-standard-rules-409287
#yelllow ones start
#at the moment the king pieces does not work 


#constants
yellow = (255, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 255, 0)
golden = (255, 215, 0)
red = (255,0,0)

#sets
boardSize = 600
size = boardSize // 8
radius = size // 2

screen = pygame.display.set_mode((boardSize, boardSize))
     

clk = pygame.time.Clock()

pygame.init()

class Board:    
    def __init__(self, size):
        self.size = size
        # checkerboard,
        # 1 : white squares
        # 0 : black squares
        self.squares = [
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1]
        ]

        self.pieces = [
            [0, "b", 0, "b", 0, "b", 0, "b"],
            ["b", 0, "b", 0, "b", 0, "b", 0],
            [0, "b", 0, "b", 0, "b", 0, "b"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["y", 0, "y", 0, "y", 0, "y", 0],
            [0, "y", 0, "y", 0, "y", 0, "y"],
            ["y", 0, "y", 0, "y", 0, "y", 0]
        ]   #initial

        self.bluePiecesRemaining = 12
        self.yellowPiecesRemaining = 12

    def draw(self):
        # draw the checkerboard according the array elements
        # 0: black square
        # 1: white square
        # 2: green square 
        # "y": yellow pieces
        # "b": blue pieces
        # "yk": yellow kings
        # "bk": blue kings
        for rowIndex, row in enumerate(self.squares):    
            for columnIndex, column in enumerate(row):
                x = columnIndex * size
                y = rowIndex * size
                color = black
                if column == 1:
                    color = white
                if column == 2:
                    color = green
                if column == "c":
                    color = red
                pygame.draw.rect(screen, color, (x, y, size, size))       


        #set the pieces on the board
        for rowIndex, row in enumerate(self.pieces):    
            for columnIndex, column in enumerate(row):
                x = columnIndex * size + size//2
                y = rowIndex * size + size//2
                if column == "b":
                    pygame.draw.circle(screen, blue, (x,y), radius)
                if column == "y":
                    pygame.draw.circle(screen, yellow, (x,y), radius)
                if column == "yk":
                    pygame.draw.circle(screen, yellow, (x,y), radius)
                    pygame.draw.circle(screen, golden, (x,y), radius//2)
                if column == "bk":
                    pygame.draw.circle(screen, blue, (x,y), radius)
                    pygame.draw.circle(screen, golden, (x,y), radius//2)

class Game:
    def __init__(self, board):
        self.board = board
        self.turn = 1
        #self.thereWasACapture = False
        self.moved = False
        self.moving = False
        self.multipleCapture = False

    @staticmethod
    def setValidMoves(moves, board):
        # set '2' in the valid board array positions 
        # draw() function sets a green rectangle 
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (board[i][j] == 2):
                    board[i][j] = 0
        for mv in range(len(moves)):
            board[moves[mv][0]] [moves[mv][1]] = 2

    @staticmethod
    def getArrayPieceIndex(pos):
        # convert the board index to the array index
        i = pos[1] // size
        j = pos[0] // size 
        return [i,j]
   
    @staticmethod
    def validCapturingMoves(current, pieces):
        #return a piece's capturing moves
        moves = []

        #blue pieces
        if pieces[current[0]][current[1]] == "b":
            
                #capturing moves
            if Game.isInBounds([current[0]+1, current[1]-1]):
                if pieces[current[0]+1][current[1]-1] == "y" or pieces[current[0]+1][current[1]-1] == "yk":
                    #a possible capture
                    if game.canCapture(current, [current[0]+1, current[1]-1], pieces):
                        #check the possibility
                        moves.append(game.indexAfterJump(current, [current[0]+1, current[1]-1]))
                    
            if Game.isInBounds([current[0]+1, current[1]+1]):
                #capturing move
                if pieces[current[0]+1][current[1]+1] == "y" or pieces[current[0]+1][current[1]+1] == "yk":
                    if game.canCapture(current, [current[0]+1, current[1]+1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]+1, current[1]+1]))    
        
        #blue kings
        if pieces[current[0]][current[1]] == "bk":           
            #forward capturing moves
            if Game.isInBounds([current[0]-1, current[1]+1]):
                #capturing move
                if pieces[current[0]-1][current[1]+1] == "y" or pieces[current[0]-1][current[1]+1] == "yk":
                    if game.canCapture(current, [current[0]-1, current[1]+1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]-1, current[1]+1]))
                
            if Game.isInBounds([current[0]-1, current[1]-1]):
               #capturing move
                if pieces[current[0]-1][current[1]-1] == "y" or pieces[current[0]-1][current[1]-1] == "yk":
                    if game.canCapture(current, [current[0]-1, current[1]-1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]-1, current[1]-1]))
             
            #backward capturing moves
            if Game.isInBounds([current[0]+1, current[1]-1]):
                #capturing move
                if pieces[current[0]+1][current[1]-1] == "y" or pieces[current[0]+1][current[1]-1] == "yk":
                    if game.canCapture(current, [current[0]+1, current[1]-1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]+1, current[1]-1]))
            
            if Game.isInBounds([current[0]+1, current[1]+1]):
                #capturing move
                if pieces[current[0]+1][current[1]+1] == "y" or pieces[current[0]+1][current[1]+1] == "yk":
                    if game.canCapture(current, [current[0]+1, current[1]+1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]+1, current[1]+1]))    
            
        #yellow pieces
        if pieces[current[0]][current[1]] == "y":
            #capturing moves
            if Game.isInBounds([current[0]-1, current[1]+1]):     
                #capturing move
                if pieces[current[0]-1][current[1]+1] == "b" or pieces[current[0]-1][current[1]+1] == "bk":
                    if game.canCapture(current, [current[0]-1, current[1]+1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]-1, current[1]+1]))
            if Game.isInBounds([current[0]-1, current[1]-1]):
               #capturing move
                if pieces[current[0]-1][current[1]-1] == "b" or pieces[current[0]-1][current[1]-1] == "bk":
                    if game.canCapture(current, [current[0]-1, current[1]-1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]-1, current[1]-1]))
        
        #yellow kings
        if pieces[current[0]][current[1]] == "yk":           
            #forward capturing moves
            if Game.isInBounds([current[0]-1, current[1]+1]):
                #capturing move
                if pieces[current[0]-1][current[1]+1] == "b" or pieces[current[0]-1][current[1]+1] == "bk":
                    if game.canCapture(current, [current[0]-1, current[1]+1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]-1, current[1]+1]))
                
            if Game.isInBounds([current[0]-1, current[1]-1]):
               #capturing move
                if pieces[current[0]-1][current[1]-1] == "b" or pieces[current[0]-1][current[1]-1] == "bk":
                    if game.canCapture(current, [current[0]-1, current[1]-1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]-1, current[1]-1]))
             
            #backward capturing moves
            if Game.isInBounds([current[0]+1, current[1]-1]):
                #capturing move
                if pieces[current[0]+1][current[1]-1] == "b" or pieces[current[0]+1][current[1]-1] == "bk":
                    if game.canCapture(current, [current[0]+1, current[1]-1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]+1, current[1]-1]))
            
            if Game.isInBounds([current[0]+1, current[1]+1]):
                #capturing move
                if pieces[current[0]+1][current[1]+1] == "b" or pieces[current[0]+1][current[1]+1] == "bk":
                    if game.canCapture(current, [current[0]+1, current[1]+1], pieces):
                        moves.append(game.indexAfterJump(current, [current[0]+1, current[1]+1]))    

        return moves

    @staticmethod
    def validSimpleMoves(current, pieces):
        #get a piece's valid moves
        
        moves = []

        if pieces[current[0]][current[1]] == "b":
            #if there are capturing moves, simple moves are not legal 
            #simple moves
            if Game.isInBounds([current[0]+1, current[1]-1]):
                #simple move
                if pieces[current[0]+1][current[1]-1] == 0:
                    #if index after move is available, save index
                    moves.append([current[0]+1, current[1]-1])
                    
            if Game.isInBounds([current[0]+1, current[1]+1]):
                #simple move
                if pieces[current[0]+1][current[1]+1] == 0:
                    moves.append([current[0]+1, current[1]+1])
                
        #blue kings
        if pieces[current[0]][current[1]] == "bk":
            """
            a king can move backward and forward, in practice it has the yellows and blues moves

            """
            #backward simple moves
            if Game.isInBounds([current[0]+1, current[1]-1]):
                #simple move
                if pieces[current[0]+1][current[1]-1] == 0:
                    moves.append([current[0]+1, current[1]-1])
                    
            if Game.isInBounds([current[0]+1, current[1]+1]):
                #simple move
                if pieces[current[0]+1][current[1]+1] == 0:
                    moves.append([current[0]+1, current[1]+1])
            
            #simple moves
            if Game.isInBounds([current[0]-1, current[1]+1]):
                #simple move
                if pieces[current[0]-1][current[1]+1] == 0:
                    moves.append([current[0]-1, current[1]+1])
                
            if Game.isInBounds([current[0]-1, current[1]-1]):
                #simple move
                if pieces[current[0]-1][current[1]-1] == 0:
                    moves.append([current[0]-1, current[1]-1])

        #yellow pieces
        if pieces[current[0]][current[1]] == "y":
            #simple moves
            if Game.isInBounds([current[0]-1, current[1]+1]):
                #simple move
                if pieces[current[0]-1][current[1]+1] == 0:
                    moves.append([current[0]-1, current[1]+1])
                    
            if Game.isInBounds([current[0]-1, current[1]-1]):
                #simple move
                if pieces[current[0]-1][current[1]-1] == 0:
                    moves.append([current[0]-1, current[1]-1])
            
        #yellow kings
        if pieces[current[0]][current[1]] == "yk":
            #forward simple moves
            if Game.isInBounds([current[0]-1, current[1]+1]):
                #simple move
                if pieces[current[0]-1][current[1]+1] == 0:
                    moves.append([current[0]-1, current[1]+1])
                    
            if Game.isInBounds([current[0]-1, current[1]-1]):
                #simple move
                if pieces[current[0]-1][current[1]-1] == 0:
                    moves.append([current[0]-1, current[1]-1])

            #backward simple moves
            if Game.isInBounds([current[0]+1, current[1]-1]):
                #simple move
                if pieces[current[0]+1][current[1]-1] == 0:
                    moves.append([current[0]+1, current[1]-1])
                    
                    
            if Game.isInBounds([current[0]+1, current[1]+1]):
                #simple move
                if pieces[current[0]+1][current[1]+1] == 0:
                    moves.append([current[0]+1, current[1]+1])

        return moves    

    @staticmethod
    def indexAfterJump(movingIndex, capturedIndex):
        #return a piece's index after capturing other one
        aux = []
        index = []
        for i in range(len(movingIndex)):
            aux.append(capturedIndex[i] - movingIndex[i])
        for j in range(len(aux)):
            index.append(capturedIndex[j] + aux[j])
        
        return index
        
    @staticmethod
    def canCapture(movingIndex, capturedIndex, pieces):
        #check if a piece at movingIndex can capture a piece at capturedIndex
        index = Game.indexAfterJump(movingIndex, capturedIndex)
        if Game.isInBounds(index):        
            if pieces[index[0]][index[1]] == 0:
                return True
            else:
                return False

    @staticmethod  
    def isInBounds(moveIndex):
        # check if index is in range
        if moveIndex[0] <= 7 and moveIndex[0] >= 0 and moveIndex[1] <= 7 and moveIndex[1] >= 0:
            return True
        else:
            return False

    @staticmethod
    def isCapturingMove(current, next, pieces):
        #check if the move is a capturing move, if so return true and remove the captured piece   
        if abs(current[0] - next[0]) == 2:
            capturedIndex = (current[0] + next[0]) // 2, (current[1] + next[1]) // 2
            pieces[capturedIndex[0]][capturedIndex[1]] = 0
            return True
        
        return False

    @staticmethod
    def captureAvailable(pieces,turn):
        #return true if any piece in it's turn can capture 
        moves = []
        if turn % 2 == 0:   #blue's turn 
            for i in range(len(pieces)):
                for j in range(len(pieces)):
                    #for each piece check if there are capturing moves
                    if pieces[i][j] == "b" or pieces[i][j] == "bk":
                        if len(Game.validCapturingMoves([i,j], pieces)) != 0:
                        #if capturing moves is not empty, update moves    
                            moves.append(Game.validCapturingMoves([i,j], pieces))

        else:   #yellows's turn 
            for i in range(len(pieces)):
                for j in range(len(pieces)):
                    if pieces[i][j] == "y" or pieces[i][j] == "yk":
                        if len(Game.validCapturingMoves([i,j], pieces)) != 0:
                            moves.append(Game.validCapturingMoves([i,j], pieces))
    
        # print("moves)")
        # print(moves)
        if len(moves) == 0:
            #if moves is empty there is no capturing moves
            return False
        else:
            return True

    @staticmethod
    def ableToMove(pieces, turn):
        #return true if any any piece in it's turn can move, capturing or simple
        moves = []
        if turn % 2 == 0:   #blue's turn 
            for i in range(len(pieces)):
                for j in range(len(pieces)):
                    #for each piece check if there are capturing moves
                    if pieces[i][j] == "b" or pieces[i][j] == "bk":
                        if len(Game.validCapturingMoves([i,j], pieces)) != 0:
                        #if capturing moves is not empty, update moves    
                            moves.append(Game.validCapturingMoves([i,j], pieces))
                        if len(Game.validSimpleMoves([i,j], pieces)) != 0:
                            #if simple moves is not empty, update moves
                            moves.append(Game.validSimpleMoves([i,j], pieces))

        else:   #yellows's turn 
            for i in range(len(pieces)):
                for j in range(len(pieces)):
                    if pieces[i][j] == "y" or pieces[i][j] == "yk":
                        if len(Game.validCapturingMoves([i,j], pieces)) != 0:
                            moves.append(Game.validCapturingMoves([i,j], pieces))
                        if len(Game.validSimpleMoves([i,j], pieces)) != 0:
                            moves.append(Game.validSimpleMoves([i,j], pieces))

        # print("moves)")
        # print(moves)
        if len(moves) == 0:
            #if moves is empty there is no capturing moves
            return False
        else:
            return True


    def showMoves(self,e):
        # show a piece's valids move  

        index = Game.getArrayPieceIndex(e.pos)
        print(index)
        if Game.captureAvailable(self.board.pieces, self.turn):
            moves = Game.validCapturingMoves(index, self.board.pieces)
        else:
            moves = Game.validSimpleMoves(index, self.board.pieces)
        # print(moves)
        
        if len(moves) == 0:
            #if no moves available, the sqaure becomes red
            self.board.squares[index[0]][index[1]] = "c"
        Game.setValidMoves(moves, self.board.squares)
        # print("showmoves")

    @staticmethod
    def becomeKing(current, next, pieces):
        #check if a piece becomes a king after moving
        #return "bk" tag for a blue king
        #return "yk" tag for a yellow king

        #yellow king
        if pieces[current[0]][current[1]] == "y":
            if next[0] == 0:
                return "yk" 
        #blue king
        elif pieces[current[0]][current[1]] == "b":
            if next[0] == 7:
                return "bk"
        
        return False


    def move(self,current, next):
        # check if 'next' is a valid move, then move
        currentIndex = Game.getArrayPieceIndex(current.pos)
        nextIndex = Game.getArrayPieceIndex(next.pos)
        if self.board.pieces[nextIndex[0]][nextIndex[1]] == 0 and self.board.squares[nextIndex[0]][nextIndex[1]] == 2:
            #simple moves
            
            if Game.becomeKing(currentIndex, nextIndex, self.board.pieces):
                #piece becomes a king
                self.board.pieces[nextIndex[0]][nextIndex[1]] = Game.becomeKing(currentIndex, nextIndex, self.board.pieces)

            else:
                aux = self.board.pieces[currentIndex[0]][currentIndex[1]]
                self.board.pieces[nextIndex[0]][nextIndex[1]] = aux
            
            self.board.pieces[currentIndex[0]][currentIndex[1]] = 0

            #self.moving = False
            self.turn += 1

            #for capturing moves, remove the captured piece and update the amount of pieces remaining
            if(Game.isCapturingMove(currentIndex, nextIndex, self.board.pieces)):
                #self.thereWasACapture = True
                if self.board.pieces[nextIndex[0]][nextIndex[1]] == "y" or self.board.pieces[nextIndex[0]][nextIndex[1]] == "yk":
                    self.board.bluePiecesRemaining -= 1

                elif self.board.pieces[nextIndex[0]][nextIndex[1]] == "b" or self.board.pieces[nextIndex[0]][nextIndex[1]] == "bk":
                    self.board.yellowPiecesRemaining -= 1

                # print (nextIndex)
                # print((Game.validCapturingMoves(nextIndex, self.board.pieces)))
                if len((Game.validCapturingMoves(nextIndex, self.board.pieces))) != 0: 
                    self.multipleCapture = True
                else: 
                    self.multipleCapture = False         

            # self.turn += 1
            #self.moving = False
            # self.moved = True

        #unselect the legal moves
        for i in range(len(self.board.squares)):
            for j in range(len(self.board.squares[i])):
                if self.board.squares[i][j] == 2 or self.board.squares[i][j] == "c":
                    self.board.squares[i][j] = 0 
                

    def checkTurn(self, e, turn):
        #check if it's the selected piece's turn
        index = Game.getArrayPieceIndex(e.pos)
        if self.getTurn(turn) == "yellow":
            if self.board.pieces[index[0]][index[1]] == "y" or self.board.pieces[index[0]][index[1]] =="yk":
                return True
        if self.getTurn(turn) == "blue":
            if self.board.pieces[index[0]][index[1]] == "b" or self.board.pieces[index[0]][index[1]] == "bk":
                return True

        return False

    def getTurn(self, turn):
        """
        Define:
            - yellows play at odd turns
            - blues play at even turns 
        """ 
        if turn % 2 == 0:
            return "blue"
        else:
            return "yellow"

    def gameOver(self):
        #if htere is a winner, return his tag: "BLUE" or "YELLOW"
        # # else return false
        if not Game.ableToMove(self.board.pieces, self.turn):
            if self.turn % 2 == 0:  #blue's turn, not able to move, yellow wins
                return "YELLOW"
            else:
                return "BLUE"

        else:
            return False


        # if self.board.yellowPiecesRemaining == 0:
        #     return "BLUE"
        # elif self.board.bluePiecesRemaining == 0:
        #     return "YELLOW"
        # else: 
        #     False 

    def winnerScreen(self, winner):
        if winner == "BLUE":
            color = blue
        else:
            color = yellow
        font = pygame.font.SysFont("arial", 72)
        text = font.render(str(winner) + " WINS", True, color, black)
        x = (boardSize - text.get_width()) // 2
        y = (boardSize - text.get_height()) // 2
        screen.blit(text, (x,y))
    

if __name__ == "__main__":
    board = Board(size)
    game = Game(board)
    multipleCapture = False
    # moving = False

#loop
while True:

    clk.tick(60) # set 60 frames per second 
    # Rules
    pygame.display.set_caption("%s's turn" % game.getTurn(game.turn))
    


    # Draw
    screen.fill(black)

    winner = game.gameOver()
    if not winner:
        board.draw()
    else:
        game.winnerScreen(winner)

    pygame.display.update()

    #events
    # MOUSEBUTTONDOWN: press mouse button  propriedades pos, button
    # MOUSEBUTTONUP: release mouse button
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if not game.moving:
                if game.checkTurn(e,game.turn):
                    #game.thereWasACapture = False
                    game.moving = True
                    game.showMoves(e)
                    posMoving = e
                    # print(game.moving)
                    # # print(e.pos)
                    # # aux = game.getPieceIndex(e.pos)
                    # aux2 = game.getArrayPieceIndex(e.pos)
                    # # print(Game.validMoves(aux2, game.board.pieces))
                    # # print(aux2)
                    # # print(game.board.squares)
                    # # print(game.validMoves(aux2, pieces.array))
            
            elif game.moving:
                game.move(posMoving, e)
                game.moving = False 
                # print("gamemoving", game.moving)
                # # print(game.multipleCapture)
                # print("hereeee")
                # print(Game.getArrayPieceIndex(e.pos))
                # print((Game.validCapturingMoves(Game.getArrayPieceIndex(e.pos), game.board.pieces)))
                if game.multipleCapture:
                    game.turn += 1

                #     game.showMoves(e)
                # elif game.moved:
                #     game.moving = False
                #     game.turn += 1
                # print("moved")
                # print(moving, game.turn)
                
                    
                # aux = game.getArrayPieceIndex(e.pos)
                # print(aux)
                # for i in range(len(game.board.squares)):
                #     print(game.board.squares[i])
                # print("------------------------------------------")

                # for i in range(len(game.board.pieces)):
                #     print(game.board.pieces[i])
            #     print(Board.getPieceIndex(e.pos))
            #     print(board.isValidMove(e))
            #     if board.isValidMove(e):
            #         board.move(posMoving, e)  
            #         moving = False  
            #         print (moving)     

