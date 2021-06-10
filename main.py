from tkinter import *
import chess
#import mimimax


# TODO fix score
# TODO let player choose a piece for promotion
# TODO implement MINIMAX
# TODO write tests

first_request=[]
currentscore = "0-0"

#engine
def make_a_good_move(legalmoves):


    uci = "e2e4"
    return uci



#gui
def game():
    '''
    lets you play a chess game.

    '''

    #making board
    global board
    board = chess.Board()

    #generating window and frame
    print(board.result())
    window,frame,scorelabel = display_board(currentscore)
    choose_starting_color(window,frame,scorelabel)

    #refresh_board(window,frame,board.board_fen(),scorelabel)



def choose_starting_color(window,frame,scorelabel):
    whitebutton =Button(window,text="click here to start as white", command= lambda : player_one_white(True,whitebutton,blackbutton,window,frame,scorelabel))
    blackbutton =Button(window,text="click here to start as black", command= lambda : player_one_white(False,whitebutton,blackbutton,window,frame,scorelabel))
    whitebutton.pack(side="left",padx=20)
    blackbutton.pack(side="right",padx=20)
    window.mainloop()

def player_one_white(iswhite,button_1,button_2,window,frame,scorelabel):
    if iswhite:
        global player_one
        player_one = chess.WHITE
    else:
        player_one = chess.BLACK

    button_1.pack_forget()
    button_2.pack_forget()
    refresh_board(window,frame,board.board_fen(),scorelabel)

def reverse_uci(uci,alphabet):
    newuci = ""
    for char in uci:
        if char in "123456789":
            newuci += str(9-int(char))
        else:
            newuci += alphabet[7-alphabet.index(char)]
    # print(uci)
    # print("new",newuci)

    return newuci
def make_a_move(event, window, frame, score_label):
    alphabet = ['a','b','c','d','e','f','g','h']
    global first_request
    legal = board.legal_moves
    # TODO
    # later utilised by letting ai make a move
    make_a_good_move(legal)

    # checks if the player has not yet selected a square to move a piece from
    if first_request !=[]:
        #printing the uci code of the move

        uci = first_request[0]+str(first_request[1])+alphabet[event.x//60]+str(8-event.y//60)
        if player_one == chess.BLACK:
            uci =reverse_uci(uci,alphabet)




                # waittil = IntVar()
                # val =StringVar(window)
                # l=["queen","rook","bisshop","knight"]
                # choicemenu= OptionMenu(window,val,*l)
                # waitbutton = Button(window,text="Click me",command= lambda: waittil.set(1))
                # choicemenu.pack(side="right")
                # waitbutton.pack(side="right")
                # waitbutton.wait_variable(waittil)
                #
                # choicemenu.pack_forget()
                # waitbutton.pack_forget()
                # promolist = ["q","r","b","n"]
                # uci+=promolist[l.index(val.get())]

        #making sure move is not a null move
        if not (uci[0]==uci[2]and uci[1]==uci[3]):

            #promotion
            if uci[3] == "8" and uci[1] == "7" or uci[3] == "1" and uci[1] == "2":
                m = create_matrix(board.board_fen())

                if m[8 - first_request[1]][alphabet.index(first_request[0])].upper() == "P":
                    uci += "q"

            #generating the actual move
            move = chess.Move.from_uci(uci)

            #checking if move is legal
            if move in legal:
                board.push_uci(uci)

                #makes sure that when a move is made,
                # that a new square can be selected to move a piece from
                # by emptying the variable first_request
                first_request = []

                #handling checkmate
                if board.is_checkmate():

                    if not board.turn == chess.WHITE:
                        print("Black won by checkmate")
                        score_label =update_score(window, frame,score_label)
                        score_label.pack(side="bottom")
                        refresh_board(window,frame,board.board_fen(),score_label)
                    else:
                        print("White won by checkmate")
                        score_label =update_score(window, frame,score_label)
                        score_label.pack(side="bottom")
                        refresh_board(window,frame,board.board_fen(),score_label)

                else:
                    #refreshing board when there is no checkmate
                    refresh_board(window,frame,board.board_fen(),score_label)
        else:

            #emptying the variable of the first square so that game goes on after a misclick
            first_request = []

    #storing the first clicked square
    first_request =[alphabet[event.x//60],8-event.y//60]


def empty_first_request(event):
    global first_request
    first_request = []



def create_matrix(fen):
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

def update_score(window, frame,score_label):
    result =board.result()
    print(result)
    global currentscore
    currentscore =str(int(currentscore[0])+ int(result[0])) + "-" +str(int(currentscore[2])+ int(result[2]))
    print(currentscore)
    score_label.pack_forget()
    #score_label.destroy()
    score_label.text = "Score = " + currentscore

    return score_label


def display_board(score):
    '''initializes tkinter window, frame and score Label'''
    window =Tk()
    window.geometry("500x500")


    scorelabel = Label(window,text="Score = "+score)
    scorelabel.pack(side="bottom")

    frame = Frame(window,height=480,width=480)
    return window,frame,scorelabel

def reverse_list(lst):
    newstr =""
    newstr+= lst[-1]
    for index in range(1,len(lst)):
        newstr+= lst[-1*index-1]
    return newstr

def refresh_board(window,frame,fen,scorelabel):
    '''
    refreshes the board after every move
    :param window:
    :param frame:
    :param fen:
    :param scorelabel:
    :return:
    '''

    frame.destroy()
    frame = Frame(window,height=480,width=480)
    bg = PhotoImage(file ="Images/background.png")
    canvas =Canvas(frame,width = 480, height = 480)
    canvas.pack(fill="both",expand = True)
    canvas.create_image(0,0,image = bg,anchor = "nw")
    #binds mouse button one to making a move
    canvas.bind("<Button-1>",func=lambda event: make_a_move(event,window,frame,scorelabel))
    canvas.bind("<Button-3>",empty_first_request)

    imagedict = {'b':'bB.png','k':'bK.png','n':'bN.png','p':'bP.png','q':'bQ.png','r':'bR.png','B':'wB.png','K':'wK.png','N':'wN.png','P':'wP.png','Q':'wQ.png','R':'wR.png'}

    imagelist=[]
    if player_one == chess.BLACK:
        fen = reverse_list(fen)
    print(fen)
    matrix =create_matrix(fen)
    for fileindex in range(len(matrix)):

        for square_index in range(len(matrix[0])):




            if matrix[fileindex][square_index] !=' ':
                imagelist.append(PhotoImage(file = "Images/"+imagedict.get(matrix[fileindex][square_index])))
                canvas.create_image(60*square_index, 60*fileindex, image=imagelist[-1], anchor = "nw")



    frame.pack(side="left")
    window.mainloop()

if __name__ == '__main__':
    game()
