import pygame 
from pathlib import Path
from PIL import Image
import time
from Timer import smallClock
# Window setup
pygame.init()
pygame.mixer.init()
#Sound effect
moveSelfSound = pygame.mixer.Sound("SoundEffects/move-self.mp3")
captureSound = pygame.mixer.Sound("SoundEffects/capture.mp3")
screen = pygame.display.set_mode((800, 600))
run = True
pygame.display.set_caption("ZyChess")
castleMoveWhite = True
castleMoveBlack = True
#piece movements1
def Pion(x1, y1, x2, y2, White, board):
    if White:
        # Move forward by one square
        if y2 == y1 - 1 and x1 == x2 and board[y2][x2] is None:
            return True
        # Move forward by two squares from starting position
        if y1 == 6 and y2 == 4 and x1 == x2 and board[y2][x2] is None and board[y1-1][x1] is None:
            return True
        # Capture diagonally
        if y2 == y1 - 1 and (x2 == x1 - 1 or x2 == x1 + 1) and board[y2][x2] is not None and board[y2][x2] in pieces_of_black:
            return True
    else:
        # Move forward by one square
        if y2 == y1 + 1 and x1 == x2 and board[y2][x2] is None:
            return True
        # Move forward by two squares from starting position
        if y1 == 1 and y2 == 3 and x1 == x2 and board[y2][x2] is None and board[y1+1][x1] is None:
            return True
        # Capture diagonally
        if y2 == y1 + 1 and (x2 == x1 - 1 or x2 == x1 + 1) and board[y2][x2] is not None and board[y2][x2] in pieces_of_white:
            return True
    return False   
def Knight(x1, y1, x2, y2):
    # List of all possible knight moves
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    # Check if the move matches any of the knight's possible moves
    for dx, dy in knight_moves:
        if x2 == x1 + dx and y2 == y1 + dy:
            return True
    
    return False
def Rook(x1,y1,x2,y2):
    if ((x1==x2)or(y1==y2)):
        return True
def Bishop(x1,y1,x2,y2):
    for i in range(8):
        if((x2== x1+i and y2== y1+i)or(x2== x1-i and y2== y1-i)or(x2== x1+i and y2== y1-i)or(x2== x1-i and y2== y1+i)):
            return True 
def Queen(x1, y1, x2, y2):
    # Check for vertical, horizontal, or diagonal movement
    if Rook(x1, y1, x2, y2) or Bishop(x1, y1, x2, y2):
        return True
    return False
def King(x1, y1, x2, y2, White, Castle, board):
    if White:
        if Castle and y1 == 7 and (x2 == x1 + 2 or x2 == x1 - 2):
            if x2 == x1 + 2:  # Kingside castling
                if board[7][5] is None and board[7][6] is None and not is_king_in_check(board, (7, 4), True) and not is_king_in_check(board, (7, 5), True) and not is_king_in_check(board, (7, 6), True):
                    return True
            elif x2 == x1 - 2:  # Queenside castling
                if board[7][1] is None and board[7][2] is None and board[7][3] is None and not is_king_in_check(board, (7, 4), True) and not is_king_in_check(board, (7, 3), True) and not is_king_in_check(board, (7, 2), True):
                    return True
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            return True
    else:
        if Castle and y1 == 0 and (x2 == x1 + 2 or x2 == x1 - 2):
            if x2 == x1 + 2:  # Kingside castling
                if board[0][5] is None and board[0][6] is None and not is_king_in_check(board, (0, 4), False) and not is_king_in_check(board, (0, 5), False) and not is_king_in_check(board, (0, 6), False):
                    return True
            elif x2 == x1 - 2:  # Queenside castling
                if board[0][1] is None and board[0][2] is None and board[0][3] is None and not is_king_in_check(board, (0, 4), False) and not is_king_in_check(board, (0, 3), False) and not is_king_in_check(board, (0, 2), False):
                    return True
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            return True
    return False
def NotBlocked(x1, y1, x2, y2, board):
    if x1 == x2:  # Vertical movement
        step = 1 if y1 < y2 else -1
        for y in range(y1 + step, y2, step):
            if 0 <= y < 8 and board[y][x1] is not None:
                return False
    elif y1 == y2:  # Horizontal movement
        step = 1 if x1 < x2 else -1
        for x in range(x1 + step, x2, step):
            if 0 <= x < 8 and board[y1][x] is not None:
                return False
    else:  # Diagonal movement
        dx = 1 if x1 < x2 else -1
        dy = 1 if y1 < y2 else -1
        x, y = x1 + dx, y1 + dy
        while x != x2 and y != y2:
            if 0 <= x < 8 and 0 <= y < 8 and board[y][x] is not None:
                return False
            x += dx
            y += dy
    return True

#If Check method:
def is_king_in_check(board, king_position, is_white):
    enemy_pieces = pieces_of_black if is_white else pieces_of_white
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece in enemy_pieces:
                # Simulate move to see if it attacks the king
                if piece == pieces_of_black[0] or piece == pieces_of_white[0]:  # Bishop
                    if Bishop(j, i, king_position[1], king_position[0]) and NotBlocked(j, i, king_position[1], king_position[0], board):
                        return True
                if piece == pieces_of_black[1] or piece == pieces_of_white[1]:  # King
                    if King(j, i, king_position[1], king_position[0], not is_white,False, PLATEAU) and NotBlocked(j, i, king_position[1], king_position[0], board):
                        return True
                if piece == pieces_of_black[2] or piece == pieces_of_white[2]:  # Knight
                    if Knight(j, i, king_position[1], king_position[0]):
                        return True
                if piece == pieces_of_black[3] or piece == pieces_of_white[3]:  # Pawn
                    if Pion(j, i, king_position[1], king_position[0], not is_white, board)and NotBlocked(j, i, king_position[1], king_position[0], board):
                        return True
                if piece == pieces_of_black[4] or piece == pieces_of_white[4]:  # Queen
                    if Queen(j, i, king_position[1], king_position[0])and NotBlocked(j, i, king_position[1], king_position[0], board):
                        return True
                if piece == pieces_of_black[5] or piece == pieces_of_white[5]:  # Rook
                    if Rook(j, i, king_position[1], king_position[0])and NotBlocked(j, i, king_position[1], king_position[0], board):
                        return True
    return False
#If Checkmate method:
def is_checkmate(board, king_position, is_white):
    if not is_king_in_check(board, king_position, is_white):
        return False
    pieces = pieces_of_white if is_white else pieces_of_black
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece in pieces:
                # Generate all possible moves for this piece
                possible_moves = generate_possible_moves(piece, i, j, board, is_white)
                for move in possible_moves:
                    new_x, new_y = move
                    
                    # Simulate the move
                    temp_piece = board[new_y][new_x]
                    board[new_y][new_x] = board[i][j]
                    board[i][j] = None
                    
                    # Check if the king is still in check after the move
                    new_king_position = (new_y, new_x) if piece == pieces_of_white[1] or piece == pieces_of_black[1] else king_position
                    if not is_king_in_check(board, new_king_position, is_white):
                        # Undo the move
                        
                        board[i][j] = board[new_y][new_x]
                        board[new_y][new_x] = temp_piece
                        return False
                    
                    # Undo the move
                    board[i][j] = board[new_y][new_x]
                    board[new_y][new_x] = temp_piece 
    return True
def generate_possible_moves(piece, x, y, board, is_white):
    possible_moves = []

    def add_move_if_valid(new_x, new_y):
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            target = board[new_y][new_x]
            if target is None or (is_white and target in pieces_of_black) or (not is_white and target in pieces_of_white):
                possible_moves.append((new_x, new_y))

    if piece in [pieces_of_white[0], pieces_of_black[0]]:  # Pawn
        direction = -1 if is_white else 1
        # Single forward move
        if board[y + direction][x] is None:
            add_move_if_valid(x, y + direction)
            # Double forward move
            if (y == 6 and is_white) or (y == 1 and not is_white):
                if board[y + 2 * direction][x] is None:
                    add_move_if_valid(x, y + 2 * direction)
        # Diagonal captures
        for dx in [-1, 1]:
            if 0 <= x + dx < 8:
                target = board[y + direction][x + dx]
                if target and ((is_white and target in pieces_of_black) or (not is_white and target in pieces_of_white)):
                    add_move_if_valid(x + dx, y + direction)

    # Logic for other pieces remains similar but refactored as needed.

    return possible_moves
def is_stalemate(board, is_white):
    pieces = pieces_of_white if is_white else pieces_of_black

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece in pieces:
                # Generate all possible moves for this piece
                possible_moves = generate_possible_moves(piece, i, j, board, is_white)
                for move in possible_moves:
                    new_x, new_y = move
                    
                    # Simulate the move
                    temp_piece = board[new_y][new_x]
                    board[new_y][new_x] = board[i][j]
                    board[i][j] = None
                    
                    # Determine the king's position
                    king_position = None
                    for x in range(8):
                        for y in range(8):
                            if (is_white and board[x][y] == pieces_of_white[1]) or (not is_white and board[x][y] == pieces_of_black[1]):
                                king_position = (x, y)
                                break
                        if king_position:
                            break
                    
                    # Check if the king is in check after the move
                    if not is_king_in_check(board, king_position, is_white):
                        # Undo the move
                        board[i][j] = board[new_y][new_x]
                        board[new_y][new_x] = temp_piece
                        return False
                    
                    # Undo the move
                    board[i][j] = board[new_y][new_x]
                    board[new_y][new_x] = temp_piece

    # If no legal move is found and the king is not in check, it's a stalemate
    king_position = None
    for x in range(8):
        for y in range(8):
            if (is_white and board[x][y] == pieces_of_white[1]) or (not is_white and board[x][y] == pieces_of_black[1]):
                king_position = (x, y)
                break
        if king_position:
            break
    
    if not is_king_in_check(board, king_position, is_white):
        return True

    return False
#using all the possible moves to see if the king is still in check ( if its the case then its a checkmate)
# Object for image
class Piece:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.path = image_path

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
image = Image.open("benz.png")
resized_image = image.resize((410, 410))
resized_image.save("resized_example.png")
bg_image = pygame.image.load("resized_example.png")
#custom cursor:
custom_cursor1 = pygame.image.load("MouseSprites/regularMouse.png").convert_alpha()
custom_cursor2 = pygame.image.load("MouseSprites/mouseWithWhite.png").convert_alpha()
custom_cursor3 = pygame.image.load("MouseSprites/mouseWithBlack.png").convert_alpha()
#Menu Image:
menu_image = pygame.image.load("Menu/Player2 Menu.png").convert_alpha()
menu_Block = pygame.image.load("Menu/menuCube.png").convert_alpha()
menu_Block2 = pygame.image.load("Menu/menuBlock3.png").convert_alpha()
#Clock
clock_image = pygame.image.load("Clock/Clock.png").convert_alpha()

# Initialisation of Object (Pieces)
assets = [Path("Black Pieces"), Path("White Pieces")]
pieces_of_white = []
pieces_of_black = []
for asset in assets:
    if asset.name == "Black Pieces":
        for element in asset.iterdir():
            pathtoImage = "Black Pieces\\"+element.name
            pawn_Image = Image.open(pathtoImage)
            resizePawn= pawn_Image.resize((20, 42))
            resizePawn.save("pawn.png")
            piece = Piece("pawn.png")
            pieces_of_black.append(piece)

    if asset.name == "White Pieces":
        for element in asset.iterdir():
            pathtoImage = "White Pieces\\"+element.name
            pawn_Image = Image.open(pathtoImage)
            resizePawn = pawn_Image.resize((20, 42))
            resizePawn.save("pion.png")
            piece = Piece("pion.png")
            pieces_of_white.append(piece)

#board initialisation
PLATEAU = [[pieces_of_black[5],pieces_of_black[2],pieces_of_black[0],pieces_of_black[4],pieces_of_black[1],pieces_of_black[0],pieces_of_black[2],pieces_of_black[5]],
           [pieces_of_black[3],pieces_of_black[3],pieces_of_black[3],pieces_of_black[3],pieces_of_black[3],pieces_of_black[3],pieces_of_black[3],pieces_of_black[3]],
           [None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None],
           [pieces_of_white[3],pieces_of_white[3],pieces_of_white[3],pieces_of_white[3],pieces_of_white[3],pieces_of_white[3],pieces_of_white[3],pieces_of_white[3]],
           [pieces_of_white[5],pieces_of_white[2],pieces_of_white[0],pieces_of_white[4],pieces_of_white[1],pieces_of_white[0],pieces_of_white[2],pieces_of_white[5]]]
LOCALISATIONX = "ABCDEFGH";LOCALISATIONY = "87654321";hitboxList = [];line = [];posx = 21;posy = 21
for i in range(8): #hitBox
    for j in range(8):
        hitBox = pygame.Rect(posx, posy, 46, 46)
        
        line.append(hitBox)
        posx+=46
    hitboxList.append(line)
    posx =21
    posy +=46
    line =[]
 #replay of the game
turn = 1
TimerBlack = smallClock(600)
TimerWhite = smallClock(600)
logs = [] #logs of the game(mouse)
 #   #the action that it is being recorded
# Main game loop
'''Game loop HERE!!!!!!!!!!!!!!!!'''
while run:
    is_white = turn % 2 != 0
    #timer:
    #Black timer
    if is_white:
        SignalBlack = is_white
        TimerBlack.continueTimer(SignalBlack)
        timeBlack = TimerBlack.getTime()
        clock_1digit = pygame.image.load(f"Clock/Nums/{timeBlack[0]}.png").convert_alpha()
        clock_2digit = pygame.image.load(f"Clock/Nums/{timeBlack[1]}.png").convert_alpha()
        clock_3digit = pygame.image.load(f"Clock/Nums/{timeBlack[2]}.png").convert_alpha()
        clock_4digit = pygame.image.load(f"Clock/Nums/{timeBlack[3]}.png").convert_alpha()
    else:
        SignalWhite = is_white
        TimerWhite.continueTimer(SignalWhite)
        timeWhite = TimerWhite.getTime()
    #Clock:
    
    #Event Handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0] and len(logs) == 0: #mouse localisation where the left click was done first and if it was on a piece
            
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(hitboxList)):
                for j in range(len(hitboxList[i])):
                    if hitboxList[i][j].collidepoint(mouse_pos):
                        print("you're at j:",j ,",i:",i)
                        if PLATEAU[i][j] != None and ( turn%2 !=0  and PLATEAU[i][j] in pieces_of_white) or (turn%2==0 and PLATEAU[i][j] in pieces_of_black):
                            print("there is a piece")
                            hand = PLATEAU[i][j]
                            logs.append((i, j))
        if pygame.mouse.get_pressed()[0] and len(logs) == 1: #mouse localisation where the left click was done second 
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(hitboxList)):
                for j in range(len(hitboxList[i])):
                    if hitboxList[i][j].collidepoint(mouse_pos):
                        if PLATEAU[i][j] == None or (turn%2 !=0 and PLATEAU[i][j] in pieces_of_black) or (turn%2==0 and PLATEAU[i][j] in pieces_of_white):
                            newPosition = (i, j)
                            logs.append((i, j))       
            #check if you moved or not 
    #viseur of each piece 
    for i in range(8): #getting king position
        for j in range(8):
            if turn % 2 == 0 and PLATEAU[i][j] == pieces_of_black[2]:
                king_position = (i, j)
                break
            if turn % 2 != 0 and PLATEAU[i][j] == pieces_of_white[2]:
                king_position = (i, j)
                break
    is_white = turn % 2 != 0 #white turn or black turn
    is_Check = is_king_in_check(PLATEAU, king_position, is_white)
    #cursor change
    # Hide the default cursor
    pygame.mouse.set_visible(False)
    custom_cursor = custom_cursor1
    if len(logs) == 1: #if hand is full for mouse
        if is_white:
            custom_cursor = custom_cursor2
        else:
            custom_cursor = custom_cursor3
    #check and give the movement of the piece:
    if len(logs) == 2:#if the logs are full
        notBlocked = NotBlocked(logs[0][1], logs[0][0], logs[1][1], logs[1][0], PLATEAU)
        if hand == pieces_of_white[0]:#white
            protocol = Bishop(logs[0][1], logs[0][0], newPosition[1], newPosition[0])and notBlocked
            print("bishop")
        if hand == pieces_of_white[1]:
            protocol = King(logs[0][1], logs[0][0], newPosition[1], newPosition[0],True,castleMoveWhite,PLATEAU)and notBlocked
            if protocol and abs(logs[1][1] - logs[0][1]) == 2:  # Castling
                if logs[1][1] == logs[0][1] + 2:  # Kingside castling
                    PLATEAU[logs[0][0]][5] = PLATEAU[logs[0][0]][7]
                    PLATEAU[logs[0][0]][7] = None
                elif logs[1][1] == logs[0][1] - 2:  # Queenside castling
                    PLATEAU[logs[0][0]][3] = PLATEAU[logs[0][0]][0]
                    PLATEAU[logs[0][0]][0] = None
                castleMoveWhite = False
            print("king")
        if hand == pieces_of_white[2]:
            protocol = Knight(logs[0][1], logs[0][0], newPosition[1], newPosition[0])
            print("knight")
        if hand == pieces_of_white[3]:
            protocol = Pion(logs[0][1], logs[0][0], newPosition[1], newPosition[0], True, PLATEAU)and notBlocked
            print("pion")
        if hand == pieces_of_white[4]:
            protocol = Queen(logs[0][1], logs[0][0], newPosition[1], newPosition[0])and notBlocked
            print("queen")
        if hand == pieces_of_white[5]:
            protocol = Rook(logs[0][1], logs[0][0], newPosition[1], newPosition[0])and notBlocked
            print("rook")
        if hand == pieces_of_black[0]:#black
            protocol = Bishop(logs[0][1], logs[0][0], newPosition[1], newPosition[0])and notBlocked
            print("bishop")
        if hand == pieces_of_black[1]:
            protocol = King(logs[0][1], logs[0][0], newPosition[1], newPosition[0],False,castleMoveBlack,PLATEAU)and notBlocked
            if protocol and abs(logs[1][1] - logs[0][1]) == 2:  # Castling
                if logs[1][1] == logs[0][1] + 2:  # Kingside castling
                    PLATEAU[logs[0][0]][5] = PLATEAU[logs[0][0]][7]
                    PLATEAU[logs[0][0]][7] = None
                elif logs[1][1] == logs[0][1] - 2:  # Queenside castling
                    PLATEAU[logs[0][0]][3] = PLATEAU[logs[0][0]][0]
                    PLATEAU[logs[0][0]][0] = None
                castleMoveBlack = False
            print("king")
        if hand == pieces_of_black[2]:
            protocol = Knight(logs[0][1], logs[0][0], newPosition[1], newPosition[0])
            print("knight")
        if hand == pieces_of_black[3]:
            protocol = Pion(logs[0][1], logs[0][0], newPosition[1], newPosition[0], False, PLATEAU)and notBlocked
            print("pion")
        if hand == pieces_of_black[4]:
            protocol = Queen(logs[0][1], logs[0][0], newPosition[1], newPosition[0])and notBlocked
            print("queen")
        if hand == pieces_of_black[5]:
            protocol = Rook(logs[0][1], logs[0][0], newPosition[1], newPosition[0])and notBlocked
            print("rook")
        if protocol:#if the movement is valid
             # Simulate move
            temp_piece = PLATEAU[newPosition[0]][newPosition[1]]
            PLATEAU[newPosition[0]][newPosition[1]] = PLATEAU[logs[0][0]][logs[0][1]]
            PLATEAU[logs[0][0]][logs[0][1]] = None
            
            # Check if the king is still in check after the move
            for i in range(8): #getting king position
                for j in range(8):
                    if turn % 2 == 0 and PLATEAU[i][j] == pieces_of_black[1]:
                        king_position = (i, j)
                        break
                    if turn % 2 != 0 and PLATEAU[i][j] == pieces_of_white[1]:
                        king_position = (i, j)
                        break
            if not is_king_in_check(PLATEAU, king_position, is_white):
                # Move is valid
                moveSelfSound.play()
                turn += 1
                logs = []
            else:
                # Undo move
                PLATEAU[logs[0][0]][logs[0][1]] = PLATEAU[newPosition[0]][newPosition[1]]
                PLATEAU[newPosition[0]][newPosition[1]] = temp_piece
                print("Invalid move: King is in check")
                logs = []
        elif not protocol:
            print("Invalid move, because move not respected")
            logs = []
        else:
            print("Invalid move2")
            logs = []
    if is_checkmate(PLATEAU, king_position, is_white): #checkmate
        print("Checkmate!")
        run = False
    if is_stalemate(PLATEAU, king_position): #stalemate
        print("Stalemate!")
        run = False
    #Checking for promotion
    '''
    for i in range(8):
        if PLATEAU[0][i] == pieces_of_black[3]:
            
        if PLATEAU[7][i] == pieces_of_white[3]:
   '''         
    
    # Clear the screenz 
    screen.fill((0, 0, 0))
    # Redraw the background
    for line in hitboxList:
        for hitBox in line:
            pygame.draw.rect(screen,(255,0,0), hitBox, 2)
    #screen.blit(0, (0, 0))                            
    x = 0
    y = 13
    #board display:
    screen.blit(bg_image, (0, 0))
    screen.blit(menu_image, (410,0))
    screen.blit(menu_Block, (410, 262))
    screen.blit(menu_Block2, (0, 411))
    #clock display for opponent:
    screen.blit(clock_image, (600, 165))
    screen.blit(clock_1digit, (613, 178))
    screen.blit(clock_2digit, (645, 178))
    screen.blit(clock_3digit, (706, 178))
    screen.blit(clock_4digit, (738, 178))
    #plateau display:
    #0 if is_white else len(PLATEAU) - 1, len(PLATEAU) if is_white else -1, playerDisplay
    playerDisplay = 1 if turn % 2 != 0 else -1
    for i in range(len(PLATEAU)):
        x=24+12
        for j in range(len(PLATEAU[i])):
            if isinstance(PLATEAU[i][j], Piece):
                PLATEAU[i][j].draw(screen, x, y)
                x+=32+14
            else:
                x+=32+14
        y+=46    
    
    # Draw the custom cursor
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(custom_cursor, (mouse_pos[0], mouse_pos[1]))
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
