from tkinter import *
from tkinter import messagebox
import chess
import minmax as mm




# TODO projectsamenvatting
# TODO poster maken
# TODO copyright toevoegen


# TODO code nog twee keer nalopen

#gui
def game():
    '''
    Initiates board and starts chess game
    '''

    #generating board
    global board
    global first_request
    first_request =[]
    board = chess.Board()
    window,frame = display_board()
    choose_starting_color(window,frame)


def choose_starting_color(window,frame):
    '''
    Lets player choose starting color
    calls player_one_color when a button is clicked
    :param window: tkinter window used to display frame
    :param frame: tkinter frame used to display chessboard and pieces
    '''
    whitebutton =Button(window, text="click here to start as white", command= lambda : player_one_color(True, whitebutton, blackbutton, window, frame))
    blackbutton =Button(window, text="click here to start as black", command= lambda : player_one_color(False, whitebutton, blackbutton, window, frame))
    whitebutton.pack(side="left",padx=20)
    blackbutton.pack(side="right",padx=20)
    window.mainloop()

def player_one_color(is_white, button_1, button_2, window, frame):
    '''
    assigns :param player_one a value based on the color chosen
    :param is_white: used to store color of human, True = white, False = black
    :param player_one: see :param iswhite
    :param button_1: button to be removed
    :param button_2: button to be removed
    :param window: tkinter window used to display frame
    :param frame: tkinter frame used to display chess board and pieces
    '''

    global player_one
    player_one = is_white
    button_1.pack_forget()
    button_2.pack_forget()
    player_or_computer(window,frame)

def player_or_computer(window,frame):
    '''
    called to alternate between computer and player making moves
    :param window: tkinter window used to display frame
    :param frame: tkinter frame used to display chess board and pieces
    '''

    if board.turn == player_one:
        refresh_board(window,frame,True)

    else:
        refresh_board(window,frame,False)


def refresh_board(window,frame,playerturn):
    '''
    refreshes the board after every move
    :param window: tkinter window used to display frame
    :param frame: tkinter frame used to display chess board and pieces
    :param fen:
    :param playerturn:
    :return:
    '''
    global board
    if not playerturn and board.outcome() == None:
        mm.make_a_good_move(board)
        # print(mm.evaluate(board))



    frame.destroy()
    frame = Frame(window,height=480,width=480)
    bg = PhotoImage(file ="Images/background.png")
    canvas =Canvas(frame,width = 480, height = 480)
    canvas.pack(fill="both",expand = True)
    canvas.create_image(0,0,image = bg,anchor = "nw")

    #binds mouse button one to making a move if it is turn of player
    if board.outcome() == None:
        canvas.bind("<Button-1>",func=lambda event: make_a_move(event,window,frame))
    imagedict = {'b':'bB.png','k':'bK.png','n':'bN.png','p':'bP.png','q':'bQ.png','r':'bR.png','B':'wB.png','K':'wK.png','N':'wN.png','P':'wP.png','Q':'wQ.png','R':'wR.png'}

    imagelist=[]
    fen = board.board_fen()

    if player_one == chess.BLACK:
        fen = reverse_fen(fen)

    matrix =create_matrix(fen)
    for fileindex in range(len(matrix)):

        for square_index in range(len(matrix[0])):

            if matrix[fileindex][square_index] !=' ':
                imagelist.append(PhotoImage(file = "Images/"+imagedict.get(matrix[fileindex][square_index])))
                canvas.create_image(60*square_index, 60*fileindex, image=imagelist[-1], anchor = "nw")



    frame.pack(side="left")

    #game ending handling

    if board.outcome() != None:
        window.after(50,lambda :determine_endgame(window))
    # if board.is_checkmate():
    #     if board.turn:
    #         window.after(50,lambda : messagebox.askyesno("end of game","black won"))
    #     else:
    #         window.after(50,lambda : messagebox.askyesno("end of game","white won"))
    # elif board.is_stalemate():
    #     window.after(50,lambda : messagebox.askyesno("end of game","its a draw no one won"))

    window.mainloop()

def determine_endgame(window):
    end_scenario_list = {1:"checkmate",2:"stalemate",3:"insufficient material",4:"seventyfive moves",5:"fivefold repetition"}
    out = board.outcome()

    if out.termination.value ==1:
        if board.turn:
            if messagebox.askyesno("black won by checkmate \n do you want to play another game?"):
                window.destroy()
                game()
        else:
            if messagebox.askyesno("white won by checkmate \n do you want to play another game?"):
                window.destroy()
                game()

    elif out.termination.value == 2:
        if messagebox.askyesno("game drawn by stalemate \n do you want to play another game?"):
            window.destroy()
            game()

    elif out.termination.value == 3:
        if messagebox.askyesno("game drawn by insufficient material \n do you want to play another game?"):
            window.destroy()
            game()

    elif out.termination.value ==4:
        if messagebox.askyesno("game drawn by more than seventyfive moves \n do you want to play another game?"):
            window.destroy()
            game()

    elif out.termination.value ==5:
        if messagebox.askyesno("game drawn by fivefold repetition \n do you want to play another game?"):
            window.destroy()
            game()



def reverse_uci(uci,alphabet):
    '''
    when playing as black the black pieces are displayed at the bottom
    but the make_a_move function still uses the same coordinate system to get correct square
    so to correct for this the function checks whether player_one is False(black) and reveses the uci if this is the case
    :param uci: move to be reversed
    :param alphabet: list containing first 8 letters of the alphabet
    :return: returns reversed uci
    '''

    newuci = ""
    for char in uci:
        if char in "123456789":
            newuci += str(9-int(char))
        else:
            newuci += alphabet[7-alphabet.index(char)]

    return newuci


def make_a_move(event, window, frame):
    '''
    function used to handle player moves by getting coördinates of where the player clicked
    :param first_request: stores first clicked square
    :param event: the event containing the coördinates of the click
    :param window: tkinter window used to display frame
    :param frame: tkinter frame used to display chess board and pieces
    '''

    alphabet = ['a','b','c','d','e','f','g','h']
    global first_request
    legal = board.legal_moves

    # checks if the player has not yet selected a square to move a piece from
    if first_request !=[]:
        #getting the uci code of the move

        uci = first_request[0]+str(first_request[1])+alphabet[event.x//60]+str(8-event.y//60)
        if not player_one:
            uci =reverse_uci(uci,alphabet)

        #making sure move is not a null move
        if not (uci[0]==uci[2]and uci[1]==uci[3]):

            #promotion
            if uci[3] == "8" and uci[1] == "7" or uci[3] == "1" and uci[1] == "2":
                m = create_matrix(board.board_fen())
                if board.turn == chess.WHITE:
                    #checks if there is a white pawn on the first square of the uci
                    if m[8 - first_request[1]][alphabet.index(first_request[0])] == "P":
                        uci += "q"
                else:
                    #checks if there is a black pawn on the first square of the uci
                    if m[first_request[1]-1][7-alphabet.index(first_request[0])] == "p":
                        uci += "q"

            #generating the actual move
            move = chess.Move.from_uci(uci)

            #checking if move is legal
            if move in legal:
                board.push_uci(uci)

                #makes sure that when a move is made,
                # a new square can be selected to move a piece from
                # by emptying the variable first_request
                first_request = []

                #handling checkmate
                if board.is_checkmate():

                    if not board.turn == chess.WHITE:
                        print("White won by checkmate")
                        refresh_board(window,frame,player_one == board.turn)
                    else:
                        print("Black won by checkmate")
                        refresh_board(window,frame,player_one == board.turn)

                elif board.is_stalemate():
                    print("Draw by stalemate")
                    refresh_board(window,frame,player_one == board.turn)


                else:
                    #refreshing board when there is no checkmate
                    refresh_board(window,frame,player_one == board.turn)
        else:

            #emptying the variable of the first square so that game goes on after a misclick
            first_request = []

    #storing the first clicked square
    first_request =[alphabet[event.x//60],8-event.y//60]


def create_matrix(fen):
    '''
    creates a matrix with empty spaces when there is no
    :param fen: string containing the pieces and the empty spaces
    :return: returns matrix of board
    '''

    matrix =[]
    fen = fen.split("/")
    for file in fen:
        matrix.append([])
        for square in file:
            if square in '123456789':

                for empty_square in range(int(square)):
                    matrix[-1].append(' ')
            else:
                matrix[-1].append(square)
    return matrix

def display_board():
    '''
    initializes tkinter window, frame
    :return: returns window and frame
    '''

    window =Tk()
    window.geometry("480x480")
    frame = Frame(window,height=480,width=480)
    return window,frame

def reverse_fen(fen):
    '''
    called to display blacks pieces at the bottom of the board
    :param fen: list
    :return: returns reversed fen
    '''

    newstr =""
    newstr+= fen[-1]
    for index in range(1, len(fen)):
        newstr+= fen[-1 * index - 1]
    return newstr


if __name__ == '__main__':
    game()
