
from copy import copy

goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goalnum = 1234567890
printpuzzle = True

class node:
    def __init__(self, istate):
        self.puzzle = istate
        self.fval = 0
        self.gval = 0
        self.hval = 0
        self.children = []
        self.num_children = 0
# print puzzle in nice looking format
def print_puzzle(puzzle):
    # display puzzle
    print('---------------')
    print(f'| {puzzle[0]}  | {puzzle[1]}  | {puzzle[2]} |')
    print('---------------')
    print(f'| {puzzle[3]}  | {puzzle[4]}  | {puzzle[5]} |')
    print('---------------')
    print(f'| {puzzle[6]}  | {puzzle[7]}  | {puzzle[8]} |')
    print('---------------')

# print algorithm selection and get option
def menu():
    print('1. Uniform Cost Search.')
    print('2. A* with the Misplaced Tile heuristic.')
    print('3. A* with the Manhattan Distance heuristic.')
    print('4. Rum all 3 Algorithm without print intermediate states')
    try:
        select = int(input())
        while (select > 4 or select < 1):
            print('Enter selection 1-3')
            select = int(input())
    except ValueError:
        print("input not integer")
    return select

# calculate number of misplaced tiles
def Misplaced_Tile_Heuristic(problem):
    compare = 1
    count = 0
    for i in range(len(problem)-1):
        if problem[i] != compare:
            count += 1
        compare+=1

    return count

# calculate manhattan distance
def Manhattan_Distance_Heuristic(problem):
    # not including distance for '0'
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    sum = 0
    for i in range(1, len(problem)):
        prob_index = problem.index(i)
        prob_col = prob_index % 3
        prob_row = prob_index // 3
        goal_index = goal.index(i)
        goal_col = goal_index % 3
        goal_row = goal_index // 3
        sum += abs(prob_row - goal_row) + abs(prob_col - goal_col)
    return sum

# helper function convert puzzle to integer, for later comparison
def ltoi(puzzle):
    s = [str(integer) for integer in puzzle]
    return int("".join(s))

# check if input puzzle has valid format
def validpuzzle(problem):
    if len(problem) != 9:
        return False
    for i in range(len(problem)):
        if problem.count(i) != 1:
            return False
    return True

#search algorithm for all 3 searches
def generalsearch(problem, QUEUEING_FUNCTION):
    myqueue = []
    visited = []
    rootnode = node(problem)
    nodecount = 0
    myqueue.append(copy(rootnode))
    qtracker = 1

    while len(myqueue):

        temp_node = myqueue.pop(0)  # dequeue min cost
        if printpuzzle:
            print(f'Expanding node with g(n) = {temp_node.gval} h(n) = {temp_node.hval} Puzzle:')
            print_puzzle(temp_node.puzzle)
        myqueue = sorted(myqueue, key=lambda node: node.fval)

        if (len(temp_node.puzzle)) == 0:
            return "failure"

        puzzlenumber = ltoi(temp_node.puzzle)
        if puzzlenumber == ltoi(goal):  # if reach goal
            print('===== Goal State ! ======')
            print(f"Solution Depth: {temp_node.gval}")
            print(f"Number of nodes expanded: {nodecount}")
            print(f"Max queue size: {qtracker}")
            return 0

        visited.append(copy(puzzlenumber))

        children_nodes = copy(EXPAND(temp_node))

        for i in range(children_nodes.num_children):
            tempn = node(children_nodes.children[i])
            if ltoi(tempn.puzzle) not in visited:
                nodecount += 1
                if(nodecount>100000): return print("failure, complexity exceeds 100K")
                # print_puzzle(tempn.puzzle)
                tempn.gval = temp_node.gval + 1
                if QUEUEING_FUNCTION == 2:
                    tempn.hval = Misplaced_Tile_Heuristic(tempn.puzzle)
                if QUEUEING_FUNCTION == 3:
                    tempn.hval = Manhattan_Distance_Heuristic(tempn.puzzle)

                tempn.fval = tempn.hval + tempn.gval
                visited.append(copy(ltoi(tempn.puzzle)))
                myqueue.append(copy(tempn))

                if qtracker < len(myqueue):
                    qtracker = len(myqueue)


    print('Error. search stoped')

# expand children node/puzzle for valid moves
def EXPAND(n):
    cstate = n.puzzle
    index = cstate.index(0)  # get index of '0'
    col = index % 3
    row = index // 3
    nstate = []
    cindex = 0

    if col != 0:  # left
        nstate.append(copy(cstate))
        nstate[cindex][index], nstate[cindex][index - 1] = nstate[cindex][index - 1], nstate[cindex][index]
        n.children.append(copy(nstate[cindex]))
        cindex += 1
        n.num_children += 1

    if col != 2:  # right
        nstate.append(copy(cstate))
        nstate[cindex][index], nstate[cindex][index + 1] = nstate[cindex][index + 1], nstate[cindex][index]
        n.children.append(copy(nstate[cindex]))
        cindex += 1
        n.num_children += 1

    if row != 0:  # 0 can go up
        nstate.append(copy(cstate))
        nstate[cindex][index], nstate[cindex][index - 3] = nstate[cindex][index - 3], nstate[cindex][index]  # swap tile
        n.children.append(copy(nstate[cindex]))
        cindex += 1
        n.num_children += 1

    if row != 2:  # down
        nstate.append(copy(cstate))
        nstate[cindex][index], nstate[cindex][index + 3] = nstate[cindex][index + 3], nstate[cindex][index]
        n.children.append(copy(nstate[cindex]))
        cindex += 1
        n.num_children += 1

    return n


if __name__ == '__main__':
    #sample_in = [8, 6, 4, 0, 7, 2, 5, 1, 3]
    #sample_in = [1,2,3,7,4,8,6,5,0]
    #sample_in = [1,2,3,0,5,6,4,7,8]
    sample_in = [1, 2, 3, 5,0,6,4,7,8]
    #sample_in = [1,2,3,7,4,0,8,6,5,]
    #sample_in = [7, 1, 3, 0, 2, 5, 8, 4, 6]
    #sample_in = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    userin = []
    puzzle = []
    print('1. use default puzzle')
    print('2. create a puzzle')

    puzzle_selection = int(input())

    if (puzzle_selection == 1):
        print("your puzzle: ")
        print_puzzle(sample_in)
        puzzle = sample_in
    else:
        print("Enter 9 tiles, EX: 1 2 3 4 5 6 7 8 0")
        userin = list(map ( int, (input().split())))
        while not validpuzzle(userin):
            print("Invalid input, Try again: ")
            userin = list(map ( int, (input().split())))
        print("your puzzle: ")
        print_puzzle(userin)
        puzzle = userin
    selection = menu()  # just print 3 options and get selection

    if selection != 4:
        generalsearch(puzzle, selection)
    else: # run all 3 search without print puzzle
        printpuzzle = False
        print('=== Search with Manhattan Distance ===')
        generalsearch(puzzle, 3)
        print('=== Search with Misplaced Tile === ')
        generalsearch(puzzle, 2)
        print('=== Search with Uniform Cost === ')
        generalsearch(puzzle, 1)

