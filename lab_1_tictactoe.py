

def print_tic_tac_toe(values):
    print("\n")
    print("\t{}|{}|{}".format(values[0], values[1], values[2]))
    print('\t-----')
 
    print("\t{}|{}|{}".format(values[3], values[4], values[5]))
    print('\t----- ')
 
 
    print("\t{}|{}|{}".format(values[6], values[7], values[8]))
    print("\n")

# print_tic_tac_toe(['x','x','x','x','x','x','x','x','x'])

def check_for_winner(values,check):
    # winner = 'none'
    # if values[0:3]== ['X','X','X'] or values[3:6]== ['X','X','X'] or values[6:9]== ['X','X','X'] or values[0:7:3]== ['X','X','X'] or values[1:8:3]== ['X','X','X'] or values[2:9:3]== ['X','X','X'] or values[0:9:4]== ['X','X','X'] or values[2:7:2]== ['X','X','X']:
    #     is_there_winner = True
    #     winner = 'Player X'
    # elif values[0:3]== ['O','O','O'] or values[3:6]== ['O','O','O'] or values[6:9]== ['O','O','O'] or values[0:7:3]== ['O','O','O'] or values[1:8:3]== ['O','O','O'] or values[2:9:3]== ['O','O','O'] or values[0:9:4]== ['O','O','O'] or values[2:7:2]== ['O','O','O']:
    #     is_there_winner = True
    #     winner = 'Player_O'
    # else:
    #     is_there_winner = False

    # return is_there_winner, winner
    if values[check[0]] == values[check[1]] == values[check[2]] and values[check[0]]!= ' ':
        is_there_winner = True
        winner = str(values[check[1]])
    else:
        is_there_winner = False
        winner = 'none'

    return is_there_winner, winner


values = []
for i in range(1,10):
    values.append(' ')

# print_tic_tac_toe(values)
is_there_winner = False
print_tic_tac_toe(values)
win_formats = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

while is_there_winner == False:
    
    
    while True:
        move_1 = input('now it\'s X\'s turn. Enter your desired position (1-9): ')
        if not move_1.isnumeric():
            print('please input an appopriate number')
            continue
        move_1 = int(move_1)
        if values[move_1-1] == ' ':
            values[move_1-1] = 'X'
            print_tic_tac_toe(values)
            break
        else:
            print('Spot already taken, please input another position \n')

    for i in win_formats:
        if is_there_winner != True:
            is_there_winner, winner = check_for_winner(values,i)
        else:
            break   

    if values.count(' ') == 0:
        print('It\'s a tie!')
        break
    elif is_there_winner == True:
        print('congratulations {}, you are the winner'.format(winner))
        break
    
    while True:
        move_2 = input('now it\'s O\'s turn. Enter your desired position (1-9): ')
        if not move_2.isnumeric():
            print('please input an appopriate number')
            continue
        move_2 = int(move_2)
        if values[move_2-1] == ' ':
            values[move_2-1] = 'O'
            print_tic_tac_toe(values)
            break
        else:
            print('Spot already taken, please input another position \n')
    
    for i in win_formats:
        if is_there_winner != True:
            is_there_winner, winner = check_for_winner(values,i)
        else:
            break   

    if values.count(' ') == 0:
        print('It\'s a tie!')
        break
    elif is_there_winner == True:
        print('congratulations {}, you are the winner'.format(winner))
        break



    
