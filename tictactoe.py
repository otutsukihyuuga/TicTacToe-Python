import pygame
import sys
import time

import tictactoe_utils as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

scoreBoard = []
notAppended = True

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False
is_mult = None
which_user = False
tile_size = 80

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    
    # Let user select what to play against
    if is_mult is None:

        # Draw multiplayer title
        mtitle = largeFont.render("Play Tic-Tac-Toe", True, white)
        mtitleRect = mtitle.get_rect()
        mtitleRect.center = ((width / 2), 50)
        screen.blit(mtitle, mtitleRect)

        # Draw buttons
        playWithBot = pygame.Rect((width / 8), (height / 2), width / 3, 50)
        playWB = mediumFont.render("against Bot", True, black)
        playWBRect = playWB.get_rect()
        playWBRect.center = playWithBot.center
        pygame.draw.rect(screen, white, playWithBot)
        screen.blit(playWB, playWBRect)

        playWithUser = pygame.Rect(width - (3 * (width / 6)), (height / 2), width / 3, 50)
        playWU = mediumFont.render("against User", True, black)
        playWURect = playWU.get_rect()
        playWURect.center = playWithUser.center
        pygame.draw.rect(screen, white, playWithUser)
        screen.blit(playWU, playWURect)

        # Check which button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playWithBot.collidepoint(mouse):
                time.sleep(0.3)
                is_mult = False
            elif playWithUser.collidepoint(mouse):
                time.sleep(0.3)
                is_mult = True

    else:
        if is_mult:

            # Draw game board
                tile_origin = (width / 2 - (1.5 * tile_size),
                            height / 2 - (1.5 * tile_size))
                tiles = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        rect = pygame.Rect(
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size, tile_size
                        )
                        pygame.draw.rect(screen, white, rect, 3)

                        if board[i][j] != ttt.EMPTY:
                            move = moveFont.render(board[i][j], True, white)
                            moveRect = move.get_rect()
                            moveRect.center = rect.center
                            screen.blit(move, moveRect)
                        row.append(rect)
                    tiles.append(row)

                game_over = ttt.terminal(board)

                # Show gameOver title
                if game_over:
                    winner = ttt.winner(board)
                    if notAppended:
                        scoreBoard.append(winner)
                        notAppended = False
                        which_user = False
                    if winner is None:
                        title = "Game Over: Tie."
                    else:
                        title = "Game Over: " + winner + " wins."
                elif which_user:
                    title = "Player 2's turn"
                else:
                    title = "Player 1's turn"
                title = largeFont.render(title, True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 30)
                screen.blit(title, titleRect)

                # Check for a user move
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1 and not game_over:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                                board = ttt.result(board, (i, j))
                                which_user = not which_user

                if game_over:
                    
                    #scoreboard
                    tie=x=o=0
                    for i in range( len(scoreBoard) ):
                        if scoreBoard[i] == None:
                            tie += 1
                        elif scoreBoard[i] == "X":
                            x += 1
                        else:
                            o += 1
                    xscore = mediumFont.render(f"X   : {x}", True, white)
                    oscore = mediumFont.render(f"O   : {o}", True, white)
                    tiescore = mediumFont.render(f"TIE : {tie}", True, white)
                    xscoreRect = xscore.get_rect()
                    oscoreRect = oscore.get_rect()
                    tiescoreRect = tiescore.get_rect()
                    xscoreRect.center = (width / 2 - 2.5*tile_size - 4, height/2 - 1.5*tile_size + 90)
                    oscoreRect.center = (width / 2 - 2.5*tile_size - 6, height/2 - 1.5*tile_size + 120)
                    tiescoreRect.center = (width / 2 - 2.5*tile_size - 6, height/2 - 1.5*tile_size + 150)
                    screen.blit(xscore, xscoreRect)
                    screen.blit(oscore, oscoreRect)
                    screen.blit(tiescore, tiescoreRect)
                    
                    #play again button
                    againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                    again = mediumFont.render("Play Again", True, black)
                    againRect = again.get_rect()
                    againRect.center = againButton.center
                    pygame.draw.rect(screen, white, againButton)
                    screen.blit(again, againRect)
                    click, _, _ = pygame.mouse.get_pressed()
                    if click == 1:
                        mouse = pygame.mouse.get_pos()
                        if againButton.collidepoint(mouse):
                            time.sleep(0.2)
                            board = ttt.initial_state()
                            
                else:
                    notAppended = True

        else:

            # Let user choose a player.
            if user is None:

                # Draw title
                title = largeFont.render("Play Tic-Tac-Toe", True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 50)
                screen.blit(title, titleRect)

                # Draw buttons
                playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
                playX = mediumFont.render("Play as X", True, black)
                playXRect = playX.get_rect()
                playXRect.center = playXButton.center
                pygame.draw.rect(screen, white, playXButton)
                screen.blit(playX, playXRect)

                playOButton = pygame.Rect(width - (3 * (width / 8)), (height / 2), width / 4, 50)
                playO = mediumFont.render("Play as O", True, black)
                playORect = playO.get_rect()
                playORect.center = playOButton.center
                pygame.draw.rect(screen, white, playOButton)
                screen.blit(playO, playORect)

                # Check if button is clicked
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    if playXButton.collidepoint(mouse):
                        time.sleep(0.3)
                        user = ttt.X
                    elif playOButton.collidepoint(mouse):
                        time.sleep(0.3)
                        user = ttt.O

            else:

                # Draw game board
                tile_origin = (width / 2 - (1.5 * tile_size),
                            height / 2 - (1.5 * tile_size))
                tiles = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        rect = pygame.Rect(
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size, tile_size
                        )
                        pygame.draw.rect(screen, white, rect, 3)

                        if board[i][j] != ttt.EMPTY:
                            move = moveFont.render(board[i][j], True, white)
                            moveRect = move.get_rect()
                            moveRect.center = rect.center
                            screen.blit(move, moveRect)
                        row.append(rect)
                    tiles.append(row)

                game_over = ttt.terminal(board)
                player = ttt.player(board)

                # Show gameOver title
                if game_over:
                    winner = ttt.winner(board)
                    if winner is None:
                        title = "Game Over: Tie."
                    else:
                        title = "Game Over: " + winner + " wins."
                elif user == player:
                    title = "Play as {user}"
                else:
                    title = "Computer thinking..."
                title = largeFont.render(title, True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 30)
                screen.blit(title, titleRect)

                # Check for AI move
                if user != player and not game_over:
                    if ai_turn:
                        time.sleep(0.5)
                        move = ttt.minimax(board)
                        board = ttt.result(board, move)
                        ai_turn = False
                    else:
                        ai_turn = True

                # Check for a user move
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1 and user == player and not game_over:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                                board = ttt.result(board, (i, j))

                if game_over:
                    againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                    again = mediumFont.render("Play Again", True, black)
                    againRect = again.get_rect()
                    againRect.center = againButton.center
                    pygame.draw.rect(screen, white, againButton)
                    screen.blit(again, againRect)
                    click, _, _ = pygame.mouse.get_pressed()
                    if click == 1:
                        mouse = pygame.mouse.get_pos()
                        if againButton.collidepoint(mouse):
                            time.sleep(0.2)
                            user = None
                            board = ttt.initial_state()
                            ai_turn = False

    pygame.display.flip()
