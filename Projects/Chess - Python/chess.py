import time
import pygame
from os import system
from pygame.locals import *
import copy
import threading
pygame.init()
pygame.mixer.init()  # Initialize the mixer module
gameWindow = pygame.display.set_mode((770, 770))
pygame.display.set_caption("Chess By AtharvaSrivastava")
font = pygame.font.Font(None, 30)
window_x, window_y = pygame.display.get_window_size()

system("cls")

def generate_square_positions(start_x, start_y, square_size):
    positions = []
    for row in range(8):
        for col in range(8):
            x = start_x + col * square_size
            y = start_y + row * square_size
            positions.append((x, y))
    return positions

def drawBoard(whiteSquare, blackSquare):
    positions = generate_square_positions(25, 25, 90)
    for index, (x, y) in enumerate(positions):
        if (index // 8 + index % 8) % 2 == 0:
            gameWindow.blit(blackSquare, (x, y))
        else:
            gameWindow.blit(whiteSquare, (x, y))
    return positions

def getCurrentMouseBlock(row_positions):
    mouseX, mouseY = pygame.mouse.get_pos()
    for i, (x, y) in enumerate(row_positions):
        if x <= mouseX < x + 90 and y <= mouseY < y + 90:
            return i
    return None

def refrainFromCancellingFellowGutti(gutti,newPos,isWhite,wGP,bGP):
    if isWhite:
        if newPos in list(wGP.values()):
            return False         
    if not isWhite:
        if newPos in list(bGP.values()):
            return False  
    return True       

def moveGutti(gutti, isWhite, whiteGuttiPosition, blackGuttiPosition, newPos):
    if isWhite:
        whiteGuttiPosition[gutti] = newPos
        return whiteGuttiPosition        
    else:
        blackGuttiPosition[gutti] = newPos 
        return blackGuttiPosition  
    
def moveGuttiForComputer(gutti,whiteGuttiPosition,blackGuttiPosition,oldPos,newPos,row_positions,ocBls,wG,bG):
    whiteKilledBlack = False
    isWhite = True
    tempBG = None
    tempBGPos = None
    played = False
    wGG = copy.copy(wG)
    wGPP = copy.deepcopy(whiteGuttiPosition)
    condd = refrainFromCancellingFellowGutti(gutti,newPos,isWhite,whiteGuttiPosition,blackGuttiPosition)
    refrainn = refrainPiecesFromMovingOutOfTheirReach(gutti,oldPos,newPos,row_positions,ocBls,isWhite)
    refrainnn = refrainPiecesFromJumpingOver(gutti,oldPos,newPos,row_positions,ocBls)
    if (condd and refrainn) and refrainnn:
        whiteGuttiPosition[gutti] = newPos
        played = True
        if ocBls.count(newPos) == 1:
            whiteKilledBlack = True
            deadGutti = list(blackGuttiPosition.keys())[list(blackGuttiPosition.values()).index(newPos)]
            tempBG = bG
            tempBGPos = blackGuttiPosition
            del bG[deadGutti]
            del blackGuttiPosition[deadGutti]
        validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,ocBls,False,whiteGuttiPosition,blackGuttiPosition)
        validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,ocBls,True,whiteGuttiPosition,blackGuttiPosition)
        wIC, bIC = check(whiteGuttiPosition,blackGuttiPosition,validTargetsForWhiteTeam,validTargetsForBlackTeam)   
        if wIC:
            whiteGuttiPosition[gutti] = oldPos
            if ocBls.count(newPos) == 1:
                bG = tempBG     
                blackGuttiPosition = tempBGPos
                whiteKilledBlack = False
                wG = copy.copy(wGG)
                whiteGuttiPosition = copy.deepcopy(wGPP)
    return whiteGuttiPosition,whiteKilledBlack ,newPos,wG,bG, played

def is_valid_king_move(oldPos, newPos):
    old_row, old_col = divmod(oldPos, 8)
    new_row, new_col = divmod(newPos, 8)

    row_diff = abs(new_row - old_row)
    col_diff = abs(new_col - old_col)

    return max(row_diff, col_diff) == 1

def refrainPiecesFromMovingOutOfTheirReach(gutti,oldPos,newPos,rowPositions,occupiedBlocks,isWhite):
    if oldPos is not None:
        # Pawn
        if gutti.startswith("pawn"):
            if isWhite:
                forward_move = 8
                double_forward_move = 16
                start_row = range(8, 16)
                capture_moves = [7, 9]
                direction_check = lambda old, new: old < new
            else:
                forward_move = -8
                double_forward_move = -16
                start_row = range(48, 56)
                capture_moves = [-7, -9]
                direction_check = lambda old, new: old > new
            def is_same_row_or_adjacent_col(oldPos, newPos):
                return (oldPos // 8 == newPos // 8) or (abs((oldPos % 8) - (newPos % 8)) == 1)
            def is_valid_capture_position(oldPos, newPos):
                if (oldPos % 8 == 0 and (newPos % 8) == 7) or ((oldPos % 8) == 7 and (newPos % 8) == 0):
                    return False
                return True
            if direction_check(oldPos, newPos):
                if (newPos - oldPos) == forward_move and newPos not in occupiedBlocks:
                    return True
                elif oldPos in start_row and (newPos - oldPos) == double_forward_move:
                    if newPos not in occupiedBlocks and (oldPos + forward_move) not in occupiedBlocks:
                        return True
                elif (newPos - oldPos) in capture_moves and newPos in occupiedBlocks:
                    if is_valid_capture_position(oldPos, newPos):
                        return True
            
                
        # Bishop
        if gutti.startswith("bishop") or gutti.startswith("queen"):
            oldRow, oldCol = divmod(oldPos, 8)
            newRow, newCol = divmod(newPos, 8)
            if abs(oldRow - newRow) == abs(oldCol - newCol):
                if 0 <= newCol < 8 and 0 <= newRow < 8:
                    return True
                     
        # Rook
        if gutti.startswith("rook") or gutti.startswith("queen"):
            if (abs(oldPos-newPos) % 8 == 0):
                return True          
            elif (oldPos>=0 and oldPos<=7) and (newPos>=0 and newPos<=7):
                return True          
            elif (oldPos>=8 and oldPos<=15) and (newPos>=8 and newPos<=15):
                return True          
            elif (oldPos>=16 and oldPos<=23) and (newPos>=16 and newPos<=23):
                return True          
            elif (oldPos>=24 and oldPos<=31) and (newPos>=24 and newPos<=31):
                return True          
            elif (oldPos>=32 and oldPos<=39) and (newPos>=32 and newPos<=39):
                return True          
            elif (oldPos>=40 and oldPos<=47) and (newPos>=40 and newPos<=47):
                return True          
            elif (oldPos>=48 and oldPos<=55) and (newPos>=48 and newPos<=55):
                return True          
            elif (oldPos>=56 and oldPos<=63) and (newPos>=56 and newPos<=63):
                return True          
        
        
        if gutti.startswith("knight"):
            knight_moves = [15, 17, -15, -17, 6, -6, 10, -10]
            if abs(newPos % 8 - oldPos % 8) <= 2 and abs(newPos - oldPos) in knight_moves:
                return True
        
        
        # Queen
        # Done
        
        # King
        if gutti.startswith("king"):
            if is_valid_king_move(oldPos, newPos):
                return True

            
    return False
    
def refrainPiecesFromJumpingOver(gutti,oldPos,newPos,rowPositions,occupiedBlocks):
    if oldPos is not None:
        # King and Knight
        if gutti.startswith("king") or gutti.startswith("knight"):
            return True
        
        # Pawn
        if gutti.startswith("pawn"):
                if abs(oldPos-newPos) == 8:
                    if(occupiedBlocks.count(newPos)==0):
                        return True
                elif ((abs(oldPos-newPos) == 7) and (occupiedBlocks.count(newPos)==1)):
                    return True
                elif ((abs(oldPos-newPos) == 9) and (occupiedBlocks.count(newPos)==1)):
                    return True
                elif (oldPos >= 48 and oldPos <= 55) or (oldPos >= 8 and oldPos <= 15):
                    if (abs(oldPos-newPos) == 16) or (abs(oldPos-newPos) == 8):
                        return True
                
        # Bishop
        if gutti.startswith("bishop"):
            step = 0
            if abs(oldPos - newPos) % 7 == 0:
                step = 7
            elif abs(oldPos - newPos) % 9 == 0:
                step = 9
            if step == 0:
                return False

            current_pos = oldPos
            while True:
                if newPos > oldPos:
                    current_pos += step
                else:
                    current_pos -= step
                    
                if current_pos == newPos:
                    break
                old_row = oldPos // 8
                current_row = current_pos // 8
                if abs(old_row - current_row) != abs((current_pos - oldPos) // step):
                    return False
                if current_pos in occupiedBlocks:
                    return False
            return True
                 
        # Rook
        if gutti.startswith("rook"):
            if oldPos // 8 == newPos // 8:
                step = 1 if newPos > oldPos else -1
                for pos in range(oldPos + step, newPos, step):
                    if pos in occupiedBlocks:
                        return False
            elif oldPos % 8 == newPos % 8:
                step = 8 if newPos > oldPos else -8
                for pos in range(oldPos + step, newPos, step):
                    if pos in occupiedBlocks:
                        return False
            else:
                return False
            return True        
        
        # Queen
        if gutti.startswith("queen"):
            if oldPos // 8 == newPos // 8:
                step = 1 if newPos > oldPos else -1
                for pos in range(oldPos + step, newPos, step):
                    if pos in occupiedBlocks:
                        return False
            elif oldPos % 8 == newPos % 8:
                step = 8 if newPos > oldPos else -8
                for pos in range(oldPos + step, newPos, step):
                    if pos in occupiedBlocks:
                        return False
            elif abs(oldPos - newPos) % 9 == 0:
                step = 9 if newPos > oldPos else -9
                for pos in range(oldPos + step, newPos, step):
                    if pos in occupiedBlocks:
                        return False
            elif abs(oldPos - newPos) % 7 == 0:
                step = 7 if newPos > oldPos else -7
                for pos in range(oldPos + step, newPos, step):
                    if pos in occupiedBlocks:
                        return False
            else:
                return False

            return True
                   
    return False
    
def listOccupiedBlocks(wGPos, bGPos):
    return list(wGPos.values()) + list(bGPos.values())
    #  heheheheheeh

def moveGuttiOnMouseClicks(event,whiteGuttiPosition, blackGuttiPosition, row_positions, selected_piece, isWhitePiece, piece_selected,ij,ocBls,wG,bG):
    blackKilledWhite = False
    temp = None
    wGG = copy.copy(wG)
    wGPP = copy.deepcopy(whiteGuttiPosition)
    deadGutti = None
    played = False
    if not event == None:
        if event.type == MOUSEMOTION and piece_selected:
            current_block = getCurrentMouseBlock(row_positions)
            mouseX, mouseY = pygame.mouse.get_pos()
            if current_block is not None:
                img = pygame.transform.scale(bG[selected_piece], (int(bG[selected_piece].get_width() * 1.2), int(bG[selected_piece].get_height() * 1.2)))
                gameWindow.blit(img,  (mouseX-45,mouseY-45))
            pygame.display.update()
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            
            current_block = getCurrentMouseBlock(row_positions)
            if current_block is not None:
                if not piece_selected:
                    # Select piece
                    if current_block in blackGuttiPosition.values():
                        selected_piece = list(blackGuttiPosition.keys())[list(blackGuttiPosition.values()).index(current_block)]
                        isWhitePiece = False
                        piece_selected = True
                        ij = current_block
                else:
                    # Move piece
                    if not isWhitePiece:
                        oldPos = blackGuttiPosition[selected_piece]
                        condd = refrainFromCancellingFellowGutti(selected_piece,current_block,False,whiteGuttiPosition,blackGuttiPosition)
                        refrainn = refrainPiecesFromMovingOutOfTheirReach(selected_piece,ij,current_block,row_positions,ocBls,False)
                        refrainnn = refrainPiecesFromJumpingOver(selected_piece,ij,current_block,row_positions,ocBls)
                        if (condd and refrainn) and (refrainnn):
                            tempBlockValue = blackGuttiPosition[selected_piece]
                            blackGuttiPosition = moveGutti(selected_piece, False, whiteGuttiPosition, blackGuttiPosition, current_block)
                            ocBls.remove(tempBlockValue)
                            if ocBls.count(current_block) == 1:
                                blackKilledWhite = True
                                deadGutti = list(whiteGuttiPosition.keys())[list(whiteGuttiPosition.values()).index(current_block)]
                                del wG[deadGutti]
                                del whiteGuttiPosition[deadGutti]
                                ocBls.append(current_block)
                                temp = current_block
                            else:
                                ocBls.append(current_block)
                            validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,ocBls,False,whiteGuttiPosition,blackGuttiPosition)
                            validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,ocBls,True,whiteGuttiPosition,blackGuttiPosition)
                            wIC, bIC = check(whiteGuttiPosition,blackGuttiPosition,validTargetsForWhiteTeam,validTargetsForBlackTeam)   

                            if bIC:
                                wG = copy.copy(wGG)
                                whiteGuttiPosition = copy.deepcopy(wGPP)
                                blackKilledWhite = False
                                blackGuttiPosition = moveGutti(selected_piece, False, whiteGuttiPosition, blackGuttiPosition, ij) 
                                ocBls.remove(current_block) 
                                ocBls.append(tempBlockValue) 
                            played = True if blackGuttiPosition[selected_piece]!=oldPos else False
                        else:
                            played = False
                    selected_piece = None
                    piece_selected = False
    return whiteGuttiPosition, blackGuttiPosition, selected_piece, isWhitePiece, piece_selected,played,ij,blackKilledWhite,temp,wG,bG

def placeAllPieces(wG, bG, wGPos, bGPos, rowPos):
    for guttiA in wG:
        gameWindow.blit(wG[guttiA], rowPos[wGPos[guttiA]])
    for guttiB in bG:
        gameWindow.blit(bG[guttiB], rowPos[bGPos[guttiB]])
        
def evaluateValidMovesForAPiece(gutti,row_positions,occupied_blocks,isWhite,wGP,bGP):
    piecePosition = wGP[gutti] if isWhite else bGP[gutti]
    validMoves = []
    if isWhite:
        for i in range(64):
            cond = refrainFromCancellingFellowGutti(gutti,i,isWhite,wGP,bGP)
            refrain = refrainPiecesFromMovingOutOfTheirReach(gutti,piecePosition,i,row_positions,occupied_blocks,True)
            refrainn = refrainPiecesFromJumpingOver(gutti,piecePosition,i,row_positions,occupied_blocks)
            if (cond and refrain) and refrainn:
                validMoves.append(i)
    if not isWhite:
        for i in range(64):
            cond = refrainFromCancellingFellowGutti(gutti,i,isWhite,wGP,bGP)
            refrain = refrainPiecesFromMovingOutOfTheirReach(gutti,piecePosition,i,row_positions,occupied_blocks,False)
            refrainn = refrainPiecesFromJumpingOver(gutti,piecePosition,i,row_positions,occupied_blocks)
            if (cond and refrain) and refrainn:
                validMoves.append(i)
    return validMoves

def intToPos(position, board_size=8):
    return divmod(position, board_size)

def getPieceType(piece):
    if "rook" in piece:
        return "rook"
    elif "knight" in piece:
        return "knight"
    elif "bishop" in piece:
        return "bishop"
    elif "queen" in piece:
        return "queen"
    elif "king" in piece:
        return "king"
    elif "pawn" in piece:
        return "pawn"
    return None

def findLineOfAttack(kingPos, attackerPos, attackerType, board_size=8):
    if isinstance(kingPos, int):
        kingPos = divmod(kingPos, board_size)
    if isinstance(attackerPos, int):
        attackerPos = divmod(attackerPos, board_size)

    if attackerType == "knight":
        return []

    attackPath = []
    rowDiff = attackerPos[0] - kingPos[0]
    colDiff = attackerPos[1] - kingPos[1]
    rowStep = rowDiff // max(abs(rowDiff), 1) if rowDiff != 0 else 0
    colStep = colDiff // max(abs(colDiff), 1) if colDiff != 0 else 0

    currentPos = attackerPos
    while currentPos != kingPos:
        attackPath.append(currentPos[0] * board_size + currentPos[1])  
        currentPos = (currentPos[0] - rowStep, currentPos[1] - colStep)
    attackPath.append(kingPos[0] * board_size + kingPos[1])  
    return attackPath

def evaluateValidMovesForAPieceWithKingSafetyRestrictions(gutti,row_positions,occupied_blocks,isWhite,wGP,bGP):
    wGPP = copy.deepcopy(wGP)
    bGPP = copy.deepcopy(bGP)
    occBls = copy.copy(occupied_blocks)
    validMoves = evaluateValidMovesForAPiece(gutti,row_positions,occupied_blocks,isWhite,wGPP,bGPP)
    finalValidMoves = []
    if isWhite:
        for move in validMoves:
            wGPP = copy.deepcopy(wGP)
            bGPP = copy.deepcopy(bGP)
            oldPos = wGPP[gutti]
            wGPP[gutti] = move
            occBls.remove(oldPos)
            occBls.append(move)
            if occupied_blocks.count(move) == 1:
                deadGutti = list(bGPP.keys())[list(bGPP.values()).index(move)]
                if not(deadGutti == "king"):
                    del bGPP[deadGutti]
            wGPP[gutti] = move
            validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,occBls,False,wGPP,bGPP)
            validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,occBls,True,wGPP,bGPP)
            wIC, bIC = check(wGPP,bGPP,validTargetsForWhiteTeam,validTargetsForBlackTeam)   
            if wIC:
                wGPP[gutti] = oldPos
            else:
                wGPP[gutti] = oldPos
                finalValidMoves.append(move)
            occBls.remove(move)
            occBls.append(oldPos)
                
    if not isWhite:
        for move in validMoves:
            wGPP = copy.deepcopy(wGP)
            bGPP = copy.deepcopy(bGP)
            oldPos = bGPP[gutti]
            bGPP[gutti] = move
            occBls.remove(oldPos)
            occBls.append(move)
            if occupied_blocks.count(move) == 1:
                deadGutti = None
                try:
                    deadGutti = list(wGPP.keys())[list(wGPP.values()).index(move)]
                except ValueError as e:
                    pass
                if not(deadGutti == "king"):
                    del wGPP[deadGutti]
            bGPP[gutti] = move
            validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,occBls,False,wGPP,bGPP)
            validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,occBls,True,wGPP,bGPP)
            wIC, bIC = check(wGPP,bGPP,validTargetsForWhiteTeam,validTargetsForBlackTeam)   
            if bIC:
                bGPP[gutti] = oldPos
            else:
                wGPP[gutti] = oldPos
                finalValidMoves.append(move)
            occBls.remove(move)
            occBls.append(oldPos)
                
    return finalValidMoves

def evaluateValidTargetsForATeam(row_positions,occupied_blocks,isWhite,wGP,bGP):
    validMoves = []
    if isWhite:
        for gutti in list(wGP.keys()):
            for enemyGuttiPosition in list(bGP.values()):
                cond = refrainFromCancellingFellowGutti(gutti,enemyGuttiPosition,isWhite,wGP,bGP)
                refrain = refrainPiecesFromMovingOutOfTheirReach(gutti,wGP[gutti],enemyGuttiPosition,row_positions,occupied_blocks,isWhite)
                refrainn = refrainPiecesFromJumpingOver(gutti,wGP[gutti],enemyGuttiPosition,row_positions,occupied_blocks)
                if (cond and refrain) and refrainn:
                    validMoves.append(enemyGuttiPosition)
    if not isWhite:
        for gutti in list(bGP.keys()):
            for enemyGuttiPosition in list(wGP.values()):
                cond = refrainFromCancellingFellowGutti(gutti,enemyGuttiPosition,isWhite,wGP,bGP)
                refrain = refrainPiecesFromMovingOutOfTheirReach(gutti,bGP[gutti],enemyGuttiPosition,row_positions,occupied_blocks,isWhite)
                refrainn = refrainPiecesFromJumpingOver(gutti,bGP[gutti],enemyGuttiPosition,row_positions,occupied_blocks)
                if (cond and refrain) and refrainn:
                    validMoves.append(enemyGuttiPosition)
    return validMoves

def evaluateValidTargetsForATeamWithKingSafetyRestrictions(row_positions,occupied_blocks,isWhite,wGP,bGP):
    wGPP = copy.deepcopy(wGP)
    bGPP = copy.deepcopy(bGP)
    validMoves = evaluateValidTargetsForATeam(row_positions,occupied_blocks,isWhite,wGPP,bGPP)
    finalValidMoves = []
    if isWhite:
        for gutti in list(wGPP.keys()):
            for move in validMoves:
                oldPos = wGPP[gutti]
                wGPP[gutti] = move
                if occupied_blocks.count(move) == 1 and not(gutti == "king"):
                    deadGutti = list(bGPP.keys())[list(bGPP.values()).index(move)]
                    if not(deadGutti == "king"):
                        del bGPP[deadGutti]
                validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,occupied_blocks,False,wGPP,bGPP)
                validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,occupied_blocks,True,wGPP,bGPP)
                wIC, bIC = check(wGPP,bGPP,validTargetsForWhiteTeam,validTargetsForBlackTeam)   
                if wIC:
                    wGPP[gutti] = oldPos
                else:
                    wGPP[gutti] = oldPos
                    finalValidMoves.append(move)
                wGPP = copy.deepcopy(wGP)
                bGPP = copy.deepcopy(bGP)

    if not isWhite:
        for gutti in list(bGPP.keys()):
            for move in validMoves:
                oldPos = bGPP[gutti]
                bGPP[gutti] = move
                if occupied_blocks.count(move) == 1 and not(gutti == "king"):
                    deadGutti = list(wGPP.keys())[list(wGPP.values()).index(move)]
                    if not(deadGutti == "king"):
                        del wGPP[deadGutti]
                validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,occupied_blocks,False,wGPP,bGPP)
                validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,occupied_blocks,True,wGPP,bGPP)
                wIC, bIC = check(wGPP,bGPP,validTargetsForWhiteTeam,validTargetsForBlackTeam)   
                if bIC:
                    bGPP[gutti] = oldPos
                else:
                    bGPP[gutti] = oldPos
                    finalValidMoves.append(move)
                wGPP = copy.deepcopy(wGP)
                bGPP = copy.deepcopy(bGP)

    return validMoves
       
def check(wGP,bGP,vTFWT,vTFBT):
    whiteInCheck, blackInCheck = False, False
    if wGP["king"] in vTFBT:
        whiteInCheck = True
    if bGP["king"] in vTFWT:
        blackInCheck = True
    return whiteInCheck, blackInCheck
     
def colourCheckedKingsSquare(pos):
    translucent_color = (255, 0, 0, 128)
    translucent_surface = pygame.Surface((90,90), pygame.SRCALPHA)
    translucent_surface.fill(translucent_color)
    gameWindow.blit(translucent_surface, pos) 
    
def isCheckmate(whiteGuttiPosition, blackGuttiPosition,possibleWhite, possibleBlack, rowPositions,occupied_blocks):
    wKPos = whiteGuttiPosition["king"]
    bKPos = blackGuttiPosition["king"]
    whiteHasMoves = any(possibleWhite[0][key] for key in possibleWhite[0])
    blackHasMoves = any(possibleBlack[0][key] for key in possibleBlack[0])
    validTargetsForWhiteTeam = evaluateValidTargetsForATeam(rowPositions,occupied_blocks,True,whiteGuttiPosition,blackGuttiPosition)
    validTargetsForBlackTeam = evaluateValidTargetsForATeam(rowPositions,occupied_blocks,False,whiteGuttiPosition,blackGuttiPosition)
    wCM = False
    bCM = False

    if wKPos in validTargetsForBlackTeam:
        if(not whiteHasMoves):
            wCM = True
    if bKPos in validTargetsForWhiteTeam:
        if(not blackHasMoves):
            bCM = True
    return wCM, bCM

def getAllPossibleMovesForTeam(isWhite, whiteGuttiPosition, blackGuttiPosition, row_positions):
    possibleMoves = {}
    occupiedBlocks = listOccupiedBlocks(whiteGuttiPosition, blackGuttiPosition)
    if isWhite:
        for gutti in whiteGuttiPosition:
            # w = copy.deepcopy(whiteGuttiPosition)
            validMoves = evaluateValidMovesForAPieceWithKingSafetyRestrictions(gutti, row_positions, occupiedBlocks, isWhite, whiteGuttiPosition, blackGuttiPosition)
            # whiteGuttiPosition = copy.deepcopy(w)            
            possibleMoves[gutti] = validMoves

    elif not isWhite:
        for gutti in blackGuttiPosition:
            # b = copy.deepcopy(blackGuttiPosition)
            validMoves = evaluateValidMovesForAPieceWithKingSafetyRestrictions(gutti, row_positions, occupiedBlocks, isWhite, whiteGuttiPosition, blackGuttiPosition)
            # blackGuttiPosition = copy.deepcopy(b) 
            possibleMoves[gutti] = validMoves
            
    return possibleMoves

def calculateMovesInBackground(isWhite, whiteGuttiPosition, blackGuttiPosition, row_positions, result):
    result[0] = getAllPossibleMovesForTeam(isWhite, whiteGuttiPosition, blackGuttiPosition, row_positions)

def checkIfPawnReachedEnd(whiteGuttiPosition, blackGuttiPosition):
    for gutti in whiteGuttiPosition.keys():
        if gutti.startswith("pawn") and (whiteGuttiPosition[gutti]>=56 and whiteGuttiPosition[gutti]<=63):
            return True, gutti
    for gutti in blackGuttiPosition.keys():
        if gutti.startswith("pawn") and (blackGuttiPosition[gutti]>=0 and blackGuttiPosition[gutti]<=7):
            return False, gutti
    return None, None

def generateUniqueKey(base_key, existing_keys):
    count = 1
    new_key = f"{base_key}{count}"
    while new_key in existing_keys:
        count += 1
        new_key = f"{base_key}{count}"
    return new_key

def pawnPromotion(whiteGuttiPosition, blackGuttiPosition, row_positions,wG,bG, aiPiece, aiSelecPiece):
    isWhite, gutti = checkIfPawnReachedEnd(whiteGuttiPosition, blackGuttiPosition)
    promotedAI = False
    if isWhite is not None and gutti is not None:
    
        if  isWhite and aiPiece is not  None: 
            poss = [27,28,35,36]
            promotion_pieces = list(wGPro.keys())[4:8]
            old_pos = (whiteGuttiPosition[gutti] if isWhite else blackGuttiPosition[gutti])
            del wG[gutti]
            del whiteGuttiPosition[gutti]
            wG[aiSelecPiece] = wGPro[aiSelecPiece]
            wG[aiPiece] = wGPro[aiSelecPiece]
            whiteGuttiPosition[aiPiece] = old_pos
            promotedAI = True
        if not isWhite:
            poss = [27,28,35,36]
            promotion_pieces = list(wGPro.keys() if isWhite else bGPro.keys())[4:8]
            pygame.draw.rect(gameWindow, (0,0,0), pygame.Rect(row_positions[27][0]-10,row_positions[27][1]-10,200,200)) 
            pygame.draw.rect(gameWindow, (255,255,255), pygame.Rect(row_positions[27][0],row_positions[27][1],180,180))
            for i,j in enumerate(range(0,4)):
                key = promotion_pieces[i]
                gameWindow.blit(wGPro[key] if isWhite else bGPro[key], row_positions[poss[i]]) 
                poss.append(key)
            mouse = getCurrentMouseBlock(row_positions)
            if mouse in [27,28,35,36]:
                event = None                            
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        selected_piece = promotion_pieces[[27, 28, 35, 36].index(mouse)]
                        old_pos = (whiteGuttiPosition[gutti] if isWhite else blackGuttiPosition[gutti])
                        
                        existing_keys = wG.keys() if isWhite else bG.keys()
                        new_key = generateUniqueKey(selected_piece, existing_keys)
                        
                        if isWhite:
                            del wG[gutti]
                            del whiteGuttiPosition[gutti]
                            wG[selected_piece] = wG[selected_piece]
                            wG[new_key] = wG[selected_piece]
                            whiteGuttiPosition[new_key] = old_pos
                        else:
                            del bG[gutti]
                            del blackGuttiPosition[gutti]
                            bG[selected_piece] = bG[selected_piece] 
                            bG[new_key] = bG[selected_piece] 
                            blackGuttiPosition[new_key] = old_pos 
    return whiteGuttiPosition,blackGuttiPosition, wG, bG, promotedAI

def draw_gradient_border(surface, board_rect, isWhiteTurn):
    glow_color = (255, 255, 255) if isWhiteTurn else (130, 130, 130)    
    for i in range(25):
        alpha = int(255 * (1 - i / 25))
        color = (*glow_color, alpha)
        gradient_layer = pygame.Surface((770 + 2 * 25, 770 + 2 * 25), pygame.SRCALPHA)
        pygame.draw.rect(gradient_layer, color, 
                         (25 - i, 25 - i, board_rect.width + 2 * i, board_rect.height + 2 * i),1)
        surface.blit(gradient_layer, (board_rect.x - 25, board_rect.y - 25))

def undoo(bSGutti, bSGuttiPositions,wG, bG, wGP, bGP, wGPos, bGPos):
    if len(bSGutti) > 1 and len(bSGuttiPositions) > 1:
        wG, bG = copy.copy(bSGutti[-2]) 
        wGP, bGP = copy.deepcopy(bSGuttiPositions[-2])  
        
        bSGutti.pop()
        bSGuttiPositions.pop()
        
        prev_wG, prev_bG = bSGutti[-1]  
        prev_wGP, prev_bGP = bSGuttiPositions[-1]
        
        wG = {piece: wG[piece] for piece in wG if piece in prev_wG}
        bG = {piece: bG[piece] for piece in bG if piece in prev_bG}

        wGPos = {piece: wGPos[piece] for piece in wGPos if piece in prev_wGP}
        bGPos = {piece: bGPos[piece] for piece in bGPos if piece in prev_bGP}

    return bSGutti, bSGuttiPositions, wG, bG, wGP, bGP

def index_to_uci(index):
    file = chr((index % 8) + ord('a'))
    rank = 8 - (index // 8)
    return f"{file}{rank}" 

def calculateMoveForComputer(possibleMovesForWhite, possibleMovesForBlack, occupiedBlocks, wGP, bGP):
    moveScores = []
    whiteMoves = possibleMovesForWhite[0]
    blackMoves = possibleMovesForBlack[0]

    allMoves = [(piece, dest) for piece, dests in whiteMoves.items() for dest in dests]
    blackAttackSquares = set(pos for dests in blackMoves.values() for pos in dests)

    for piece, dest in allMoves:
        score = 0

        if dest in occupiedBlocks:
            if dest in blackAttackSquares:
                score += 0.5
            else:
                score += 1
        
        if dest in {27, 28, 35, 36}: # center control
            score += 0.25
        
        if piece.startswith(("knight", "bishop")) and wGP.get(piece, 0) < 16:
            score += 0.25

        if dest % 8 in {0, 7}:
            score -= 0.25  # discourage moving to edges unless necessary


        if piece.startswith("knight") and wGP.get(piece, 0) < 16 and dest >= 16:
            score += 2

        current_pos = wGP.get(piece)
        if current_pos in blackAttackSquares:
            if piece.startswith("pawn"):
                score -= 1.5
            elif piece.startswith(("knight", "bishop")):
                score -= 2.5
            elif piece.startswith(("rook", "queen")):
                score -= 3.5
        
        black_king_pos = bGP.get("king")
        if dest == black_king_pos:
            score += 5
            attackers = 0
            for p, moves in possibleMovesForWhite[0].items():
                if black_king_pos in moves:
                    attackers += 1

            if attackers >= 2:
                score += 1

            king_escape_moves = possibleMovesForBlack[0].get("king", [])
            king_safe_moves = [
                move for move in king_escape_moves if move not in set(pos for dests in whiteMoves.values() for pos in dests)
            ]
            block_or_capture_possible = False
            for black_piece, moves in possibleMovesForBlack[0].items():
                if black_piece == "king":
                    continue
                if dest in moves:
                    block_or_capture_possible = True
                    break

            if not king_safe_moves and not block_or_capture_possible:
                score += 10
  
        if piece.startswith("pawn"):
            current_rank = wGP[piece] // 8
            target_rank = dest // 8
            if target_rank > current_rank:
                score += 0.1 * (target_rank - current_rank)  # reward pushing forward
            
        if len(whiteMoves.get(piece, [])) <= 1:
            score -= 0.5
            
        attacked_squares = [dest]
        target_count = sum(1 for square in attacked_squares if square in bGP.values())
        if target_count >= 2:
            score += 2
            
        if piece.startswith(("knight", "bishop")) and dest <= 10:
            score += 0.4  # good early development
            
        for enemy_piece, pos in bGP.items():
            if pos == dest:
                if enemy_piece.startswith("queen"):
                    score += 4
                elif enemy_piece.startswith("rook"):
                    score += 3
                elif enemy_piece.startswith(("knight", "bishop")):
                    score += 2
                    
        if piece.startswith("knight"):
            future_targets = [dest + offset for offset in [6, 10, 15, 17, -6, -10, -15, -17]]
            threats = sum(1 for t in future_targets if t in bGP.values())
            if threats >= 2:
                score += 1.5  # sets up a fork
                
        if piece.startswith("pawn"):
            if dest // 8 >= 6:
                score += 2  # approaching promotion
                
        if dest in blackAttackSquares:
            score-=1
            
        if dest in occupiedBlocks:
            if all(dest not in moves for moves in possibleMovesForBlack[0].values()):
                score += 1
                
        if piece.startswith("rook"):
            file = dest % 8
            white_pawns = [wGP[p] for p in wGP if p.startswith("pawn")]
            black_pawns = [bGP[p] for p in bGP if p.startswith("pawn")]
            if all(p % 8 != file for p in white_pawns + black_pawns):
                score += 1.25  # rook on open file
        
        white_non_pawn_pieces = [p for p in wGP if not p.startswith("pawn")]
        black_non_pawn_pieces = [p for p in bGP if not p.startswith("pawn")]
        if len(white_non_pawn_pieces) <= 2 and len(black_non_pawn_pieces) <= 2:
            if piece.startswith("pawn"):
                rank = dest // 8
                score += 0.5 + 0.2 * (rank - (wGP[piece] // 8))  # heavily reward forward motion
                
                if rank >= 6:
                    score += 2  # already had this, now reinforced in endgame context

            if piece.startswith("king"):
                center_squares = {27, 28, 35, 36}
                if dest not in center_squares:
                    near_white_pawns = any(abs(dest - wp) <= 9 for wp in wGP.values() if wp != wGP[piece] and str(wp).startswith("pawn"))
                    if not near_white_pawns:
                        score -= 1.5  # king spinning away from action


        moveScores.append((piece, dest, score))

    return moveScores
    
def main():
    exitGame = False
    clock = pygame.time.Clock()
    FPS = 100

    whiteGutti = {
        "king": pygame.image.load("Media/Visual/w_king.png").convert_alpha(),
        "queen": pygame.image.load("Media/Visual/w_queen.png").convert_alpha(),
        "rook1": pygame.image.load("Media/Visual/w_rook.png").convert_alpha(),
        "knight1": pygame.image.load("Media/Visual/w_knight.png").convert_alpha(),
        "bishop1": pygame.image.load("Media/Visual/w_bishop.png").convert_alpha(),
        "bishop2": pygame.image.load("Media/Visual/w_bishop.png").convert_alpha(),
        "knight2": pygame.image.load("Media/Visual/w_knight.png").convert_alpha(),
        "rook2": pygame.image.load("Media/Visual/w_rook.png").convert_alpha(),
        "pawn1": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn2": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn3": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn4": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn5": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn6": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn7": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
        "pawn8": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha()
    }
    
    blackGutti = {
        "king": pygame.image.load("Media/Visual/b_king.png").convert_alpha(),
        "queen": pygame.image.load("Media/Visual/b_queen.png").convert_alpha(),
        "rook1": pygame.image.load("Media/Visual/b_rook.png").convert_alpha(),
        "knight1": pygame.image.load("Media/Visual/b_knight.png").convert_alpha(),
        "bishop1": pygame.image.load("Media/Visual/b_bishop.png").convert_alpha(),
        "bishop2": pygame.image.load("Media/Visual/b_bishop.png").convert_alpha(),
        "knight2": pygame.image.load("Media/Visual/b_knight.png").convert_alpha(),
        "rook2": pygame.image.load("Media/Visual/b_rook.png").convert_alpha(),
        "pawn1": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn2": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn3": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn4": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn5": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn6": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn7": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
        "pawn8": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha()
    }
    
    whiteSquare = pygame.image.load("Media/Visual/squareLight.png").convert_alpha()
    blackSquare = pygame.image.load("Media/Visual/squareDark.png").convert_alpha()
    
    whiteGuttiPosition = {
        "rook1": 0, "knight1": 1, "bishop1": 2, "queen": 3,
        "king": 4, "bishop2": 5, "knight2": 6, "rook2": 7,
        "pawn1": 8, "pawn2": 9, "pawn3": 10, "pawn4": 11,
        "pawn5": 12, "pawn6": 13, "pawn7": 14, "pawn8": 15
    }

    blackGuttiPosition = {
        "rook1": 56, "knight1": 57, "bishop1": 58, "queen": 59,
        "king": 60, "bishop2": 61, "knight2": 62, "rook2": 63,
        "pawn1": 48, "pawn2": 49, "pawn3": 50, "pawn4": 51,
        "pawn5": 52, "pawn6": 53, "pawn7": 54, "pawn8": 55
    }

    selected_piece = None
    isWhitePiece = None
    piece_selected = False
    chanceOfWhite = False
    ij = None
    scoreUser = 0
    scoreComputer = 0    
    row_positions = generate_square_positions(25,25,90)
    possibleMovesForWhite = [{}]
    possibleMovesForBlack = [{}]
    scoreUserr = None
    scoreComputerr = None
    whiteMoveThread = threading.Thread(target=calculateMovesInBackground, args=(True, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForWhite))
    blackMoveThread = threading.Thread(target=calculateMovesInBackground, args=(False, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForBlack))
    whiteMoveThread.start()
    blackMoveThread.start()
    chanceOfWhite = False
    boardStatesGutti = []
    boardStatesGuttiPositions = []
    boardStatesGutti.append([whiteGutti.copy(), blackGutti.copy()])  # Shallow copy for lists
    boardStatesGuttiPositions.append([whiteGuttiPosition.copy(), blackGuttiPosition.copy()])
    undo = False
    help = False
    interfaceColour = (130,130,130)
    gameOver = False
    whiteWon = False
    blackWon = False
    global wGPro
    global bGPro
    
    wGPro = whiteGutti
    bGPro = blackGutti
    
    pygame.event.pump()
    while not exitGame:
        if not gameOver:
            event = None                            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True  
                elif event.type == pygame.KEYDOWN:
                    if (event.key == K_z):
                        undo = True
                    if (event.key == K_h):
                        help = True
                elif event.type == pygame.KEYUP:
                    if event.key == K_h:
                        help = False
                        
            gameWindow.fill((0, 0, 0))
            board_rect = pygame.Rect(30,30, 710, 710)
            draw_gradient_border(gameWindow, board_rect, chanceOfWhite) 
            row_positions = drawBoard(whiteSquare, blackSquare)
            placeAllPieces(whiteGutti, blackGutti, whiteGuttiPosition, blackGuttiPosition, row_positions)
            occupiedBlocks = listOccupiedBlocks(whiteGuttiPosition,blackGuttiPosition)
            
            font = pygame.font.Font(None, 40)
            scoreUserDisplay = font.render(f"You : {scoreUser}", True, (255,255,255))
            gameWindow.blit(scoreUserDisplay, (150, 0))
            scoreComputerDisplay = font.render(f"Computer : {scoreComputer}", True, (255,255,255))
            gameWindow.blit(scoreComputerDisplay, (470, 0))
            if scoreUserr and scoreComputerr is not None:
                scoreUserDisplayy = font.render(f"You {scoreUserr}", True, (255,255,255))
                gameWindow.blit(scoreUserDisplayy, (150, 745))
                scoreComputerDisplayy = font.render(f"Computer {scoreComputerr}", True, (255,255,255))
                gameWindow.blit(scoreComputerDisplayy, (470, 745))
                
            aiChoosesPiece = generateUniqueKey("queen", wGPro)
            aiModelPiece = "queen"
            whiteGuttiPosition,blackGuttiPosition,whiteGutti,blackGutti,  promotedAI = pawnPromotion(whiteGuttiPosition,blackGuttiPosition,row_positions,whiteGutti,blackGutti ,aiChoosesPiece, aiModelPiece)
            if  promotedAI:
                whiteMoveThread = threading.Thread(target=calculateMovesInBackground, args=(True, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForWhite))
                whiteMoveThread.start()
                blackMoveThread = threading.Thread(target=calculateMovesInBackground, args=(False, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForBlack))
                blackMoveThread.start()
                promotedAI  =  False
            validTargetsForBlackTeam = evaluateValidTargetsForATeam(row_positions,occupiedBlocks,False,whiteGuttiPosition,blackGuttiPosition)
            validTargetsForWhiteTeam = evaluateValidTargetsForATeam(row_positions,occupiedBlocks,True,whiteGuttiPosition,blackGuttiPosition)
            whiteInCheck, blackInCheck = check(whiteGuttiPosition,blackGuttiPosition,validTargetsForWhiteTeam,validTargetsForBlackTeam)
            
            if whiteInCheck:
                colourCheckedKingsSquare(row_positions[whiteGuttiPosition["king"]])
            if blackInCheck:
                colourCheckedKingsSquare(row_positions[blackGuttiPosition["king"]])           
                            
            wCM, bCM = isCheckmate(whiteGuttiPosition,blackGuttiPosition, possibleMovesForWhite,possibleMovesForBlack, row_positions, occupiedBlocks)
            
            if bCM:
                whiteWon = True
                scoreComputerr = "Won"
                scoreUserr = "Lost"
                gameOver = True
            elif wCM:
                blackWon = True
                scoreUserr = "Won"
                scoreComputerr = "Lost"
                gameOver = True
            elif not bCM and not wCM:
                scoreUserr =  None
                scoreComputerr = None 
            
            if undo:
                boardStatesGutti, boardStatesGuttiPositions, whiteGutti, blackGutti, whiteGuttiPosition, blackGuttiPosition = undoo(boardStatesGutti, boardStatesGuttiPositions,whiteGutti, blackGutti, whiteGuttiPosition, blackGuttiPosition, whiteGuttiPosition, blackGuttiPosition)
                
            if help:
                helpY = 350
                font = pygame.font.Font(None, 30)
                startMsg = font.render(f'h - hold for Help', True, interfaceColour)
                gameWindow.blit(startMsg, (int(770 - startMsg.get_width())/2, helpY+10)) 
                startMsg = font.render(f'space - ReStart', True, interfaceColour)
                gameWindow.blit(startMsg, (int(770 - startMsg.get_width())/2, helpY+35)) 
                startMsg = font.render(f'Mouse(DragNDrop) - MovePieces', True, interfaceColour)
                gameWindow.blit(startMsg, (int(770 - startMsg.get_width())/2, helpY+60))      
            
            whiteMoveScore = calculateMoveForComputer(possibleMovesForWhite,possibleMovesForBlack,occupiedBlocks, whiteGuttiPosition, blackGuttiPosition)
            
            
            
            
            
            ########## CHESS ##########
            
            
            
            
            
            if not wCM and not bCM:      
                if not chanceOfWhite:
                    whiteGuttiPosition, blackGuttiPosition, selected_piece, isWhitePiece, piece_selected,played,ij,bKW,temp,whiteGutti,blackGutti = moveGuttiOnMouseClicks(event,
                    whiteGuttiPosition, blackGuttiPosition, row_positions, selected_piece, isWhitePiece, piece_selected,ij,occupiedBlocks,whiteGutti,blackGutti)
                    if played:
                        whiteMoveThread = threading.Thread(target=calculateMovesInBackground, args=(True, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForWhite))
                        whiteMoveThread.start()
                        blackMoveThread = threading.Thread(target=calculateMovesInBackground, args=(False, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForBlack))
                        blackMoveThread.start()
                        if bKW:
                            scoreUser+=1
                        chanceOfWhite = True                    
                        boardStatesGutti.append([whiteGutti.copy(), blackGutti.copy()])  # Shallow copy for lists
                        boardStatesGuttiPositions.append([whiteGuttiPosition.copy(), blackGuttiPosition.copy()])
                        played = False

                elif chanceOfWhite:
                    if whiteMoveScore != []:
                        move = max(whiteMoveScore, key=lambda x: x[2]) 
                        guttiForAI = move[0]
                        whiteGuttiPosition,wKB,tempp,whiteGutti,blackGutti,played  = moveGuttiForComputer(guttiForAI,whiteGuttiPosition,blackGuttiPosition,whiteGuttiPosition[guttiForAI],move[1],row_positions,occupiedBlocks,whiteGutti,blackGutti)
                    if not any(possibleMovesForBlack) and whiteMoveScore == []:
                        wCM = True
                        blackWon = True
                        scoreUserr = "Won"
                        scoreComputerr = "Lost"
                        gameOver = True
                    if wKB:
                            if tempp is not None:
                                scoreComputer+=1
                    if played:
                        boardStatesGutti.append([whiteGutti,blackGutti])
                        boardStatesGuttiPositions.append([whiteGuttiPosition,blackGuttiPosition])
                        chanceOfWhite = False
                        whiteMoveThread = threading.Thread(target=calculateMovesInBackground, args=(True, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForWhite))
                        whiteMoveThread.start()
                        blackMoveThread = threading.Thread(target=calculateMovesInBackground, args=(False, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForBlack))
                        blackMoveThread.start()
            
            undo = False
                                        
            clock.tick(FPS)
            pygame.display.update()
            
            
            
        if gameOver:
                if blackWon:
                    pygame.mixer.Sound('Media\Audio\win.mp3').play()
                if whiteWon:
                    pygame.mixer.Sound('Media\Audio\lost.mp3').play()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exitGame = True                
                    elif event.type == pygame.KEYDOWN:
                        if (event.key == K_RETURN or event.key == K_KP_ENTER):
                            whiteGutti = {
                                "rook1": pygame.image.load("Media/Visual/w_rook.png").convert_alpha(),
                                "knight1": pygame.image.load("Media/Visual/w_knight.png").convert_alpha(),
                                "bishop1": pygame.image.load("Media/Visual/w_bishop.png").convert_alpha(),
                                "king": pygame.image.load("Media/Visual/w_king.png").convert_alpha(),
                                "queen": pygame.image.load("Media/Visual/w_queen.png").convert_alpha(),
                                "bishop2": pygame.image.load("Media/Visual/w_bishop.png").convert_alpha(),
                                "knight2": pygame.image.load("Media/Visual/w_knight.png").convert_alpha(),
                                "rook2": pygame.image.load("Media/Visual/w_rook.png").convert_alpha(),
                                "pawn1": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn2": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn3": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn4": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn5": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn6": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn7": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha(),
                                "pawn8": pygame.image.load("Media/Visual/w_pawn.png").convert_alpha()
                            }                           
                            blackGutti = {
                                "rook1": pygame.image.load("Media/Visual/b_rook.png").convert_alpha(),
                                "knight1": pygame.image.load("Media/Visual/b_knight.png").convert_alpha(),
                                "bishop1": pygame.image.load("Media/Visual/b_bishop.png").convert_alpha(),
                                "king": pygame.image.load("Media/Visual/b_king.png").convert_alpha(),
                                "queen": pygame.image.load("Media/Visual/b_queen.png").convert_alpha(),
                                "bishop2": pygame.image.load("Media/Visual/b_bishop.png").convert_alpha(),
                                "knight2": pygame.image.load("Media/Visual/b_knight.png").convert_alpha(),
                                "rook2": pygame.image.load("Media/Visual/b_rook.png").convert_alpha(),
                                "pawn1": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn2": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn3": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn4": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn5": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn6": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn7": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha(),
                                "pawn8": pygame.image.load("Media/Visual/b_pawn.png").convert_alpha()
                            }
                            whiteSquare = pygame.image.load("Media/Visual/squareLight.png").convert_alpha()
                            blackSquare = pygame.image.load("Media/Visual/squareDark.png").convert_alpha()
                            whiteGuttiPosition = {
                                "rook1": 0, "knight1": 1, "bishop1": 2, "king": 3, "queen": 4,
                                "bishop2": 5, "knight2": 6, "rook2": 7,
                                "pawn1": 8, "pawn2": 9, "pawn3": 10, "pawn4": 11,
                                "pawn5": 12, "pawn6": 13, "pawn7": 14, "pawn8": 15
                            }
                            blackGuttiPosition = {
                                "rook1": 56, "knight1": 57, "bishop1": 58, "king": 59, "queen": 60,
                                "bishop2": 61, "knight2": 62, "rook2": 63,
                                "pawn1": 48, "pawn2": 49, "pawn3": 50, "pawn4": 51,
                                "pawn5": 52, "pawn6": 53, "pawn7": 54, "pawn8": 55
                            }
                            selected_piece = None
                            isWhitePiece = None
                            piece_selected = False
                            chanceOfWhite = False
                            ij = None
                            scoreUser = 0
                            scoreComputer = 0    
                            row_positions = generate_square_positions(25,25,90)
                            possibleMovesForWhite = [{}]
                            possibleMovesForBlack = [{}]
                            scoreUserr = None
                            scoreComputerr = None
                            whiteMoveThread = threading.Thread(target=calculateMovesInBackground, args=(True, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForWhite))
                            blackMoveThread = threading.Thread(target=calculateMovesInBackground, args=(False, whiteGuttiPosition, blackGuttiPosition, row_positions, possibleMovesForBlack))
                            whiteMoveThread.start()
                            blackMoveThread.start()
                            chanceOfWhite = False
                            boardStatesGutti = []
                            boardStatesGuttiPositions = []
                            boardStatesGutti.append([whiteGutti.copy(), blackGutti.copy()])  # Shallow copy for lists
                            boardStatesGuttiPositions.append([whiteGuttiPosition.copy(), blackGuttiPosition.copy()])
                            undo = False
                            help = False
                            interfaceColour = (160,160,160)
                            gameOver = False
                            whiteWon = False
                            blackWon = False
                            break
            

if __name__ == "__main__":
    main()

pygame.quit()
exit()