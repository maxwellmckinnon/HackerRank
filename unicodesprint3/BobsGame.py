#!/bin/python3
# no Print statement version
DEBUG = False
import sys

"""Custom input
5
3
X.X
...
XKK
1
.
1
X
1
K
4
XXXX
KXKK
XX.X
XX.K
"""

winnable_d = {}  # Maps from board tuple to current player's status on the board: "WIN", "LOSS", or "UNKNOWN" e.g. format of {((1,0),(-1,-1)):"WIN"}


class Leaf:
    def __init__(self, board, turn, parent=None):
        self.board = board
        self.winnable = "UNKNOWN"  # WIN, LOSS, UNKNOWN - this assumes optimal play from both sides, this is wrt self.turn
        self.parent = parent
        self.children = []  # List of children leaf nodes
        self.turn = turn  # Bob ("B") or Alice's ("A") current turn on this board?
        self.nextturn = "A" if self.turn == "B" else "B"

    def __str__(self):
        r = ""
        for row in self.board:
            r += str(row) + "\n"
        return r

    def print_board_stats(self):
        print("Winnable:", self.winnable)
        print("Turn:", self.turn)
        print("Board:")
        print(self)
        if self.parent:
            print("Parent:\n{}".format(self.parent))

    def number_winnable(self):
        """Get the number of moves that result in a win given optimal play from both sides
        uses check_winnable but on the first depth,
        doesn't trim branches early as it needs to check for number of possible first moves to win"""

        win_options = 0
        self.get_children()

        if len(self.children) == 0:  # Edge case, no moves off the start
            return 0
        else:
            if DEBUG: print("Initial Board:\n{}".format(self))
            for child in self.children:
                if DEBUG: print("First Expansion, child:\n{}".format(child))
                child.check_winnable()
                if child.winnable == "LOSS":  # If Alice has a loss in that position
                    win_options += 1
            return win_options

    def check_winnable(self):
        # Depth first recursion along children leaves

        # Code to search if board is winnable here:
        # Breadth first seems bad as every node would have to be searched. Depth first? Then work backwards from optimal play? Would be a good way to eliminate branches along with a dictionary of what positions are winnable as leaves in the tree won't be unique

        # First check if board is known winnable (lookup dictionary), this could be set by a child
        self.winnable = winnable_d.get(self.board, "UNKNOWN")  # Return UNKNOWN if game lookup doesn't exist

        if self.winnable != "UNKNOWN":
            return  # Status already known, maybe set by a child, no need to check children

        # Get children from this leaf and put in self.children
        self.get_children()

        #########
        # Base Case: no children moves available
        if len(self.children) == 0:  # All kings have been checked, legitimately no moves left now
            # No moves left, game is lost
            # Report position as a win if it is A's turn. Else report loss.
            self.winnable = "LOSS"
            winnable_d[self.board] = self.winnable
            if DEBUG: print("Base Case, No moves remaining, Player {}, W/L:{}".format(self.turn, self.winnable))
            if DEBUG: self.print_board_stats()

            # Can we also set the parent depending on what happens here?
            if self.winnable == "LOSS":  # If this position is a loss, then the above player will take it to win
                self.parent.winnable = "WIN"
                winnable_d[self.parent.board] = self.parent.winnable
            # If this position is a win though, the above player won't have to take it unless there is no other option
            return
        # End Base Case
        #########

        childlossfound = False
        for child in self.children:
            # Check if a branch with optimal play is found, no need to search for other optimal branches
            # Optimal if forced loss is found in children for the other player
            child.check_winnable()
            if child.winnable == "LOSS":
                self.winnable = "WIN"
                winnable_d[self.board] = "WIN"
                if DEBUG: self.print_board_stats()
                return  # exits from loop that expands on children

        # All children result in a forced win for the next player, therefore this position is a loss
        # Additionally, the parent playing optimally will take this path, making it a win for the parent
        self.winnable = "LOSS"
        winnable_d[self.board] = "LOSS"
        self.parent.winnable = "WIN"
        winnable_d[self.parent.board] = "WIN"
        if DEBUG: print("All next move paths have been exhausted as wins for the next player, this position is a loss")
        if DEBUG: self.print_board_stats()

    def get_children(self):
        """Make leaf nodes for each legal board position one move later from self
        Check all kings and all moves that king can make

        Returns nothing but puts children in self.children array
        Also updates this children node with its parent
        """
        # For each square if it has 1+ kings, make a leaf for each of that square's legal moves with the next board instantiated to that leaf

        n = len(self.board)
        for row in range(n):
            for col in range(n):
                if self.board[row][col] > 0:  # King is on square
                    # Check which of 3 moves for this king are legal and make a new board
                    next_move_boards = self.get_legal_moves(row, col)
                    for b in next_move_boards:
                        self.children.append(Leaf(b, turn=self.nextturn, parent=self))
                    if DEBUG:
                        print("Number of children from board below moving K at r{},c{}:".format(row, col)
                              + "{}".format(len(next_move_boards)))
                    if DEBUG: self.print_board_stats()

    def get_legal_moves(self, row, col):
        """returns list of boards with next move made, King at row,col moved"""
        # Three possible moves: up, left, up-left

        ret_list = []

        # Up
        if row - 1 >= 0:
            upval = self.board[row - 1][col]
            if upval >= 0:  # On the board and not a damaged cell
                uptuple_board = self.move_king(row, col, row - 1, col)
                ret_list.append(uptuple_board)
        # Left
        if col - 1 >= 0:
            leftval = self.board[row][col - 1]
            if leftval >= 0:  # On the board and not a damaged cell
                lefttuple_board = self.move_king(row, col, row, col - 1)
                ret_list.append(lefttuple_board)
        # Up-Left
        if col - 1 >= 0 and row - 1 >= 0:
            ulval = self.board[row - 1][col - 1]
            if ulval >= 0:  # On the board and not a damaged cell
                ultuple_board = self.move_king(row, col, row - 1, col - 1)
                ret_list.append(ultuple_board)
        return ret_list

    def move_king(self, x, y, x2, y2):
        """Moves a king from x,y to x2,y2
        Returns a tuple of the new board
        Does not check if move is legal or not before doing it
        Throw exception if OFF THE BOARD
        Turning a tuple into a list and back may be costly... Not sure
        """
        try:
            boardlist = [list(r) for r in self.board]
            boardlist[x][y] = self.board[x][y] - 1
            boardlist[x2][y2] = self.board[x2][y2] + 1
            uptuple_board = ()
            for r in boardlist:
                uptuple_board += (tuple(r),)
            return uptuple_board
        except:
            print("Failure to move king from x,y {},{} to x2,y2 {},{}".format(x, y, x2, y2))


if __name__ == "__main__":
    q = int(input().strip())
    for a0 in range(q):
        n = int(input().strip())
        board = []  # ['.K', 'X.'] gets mapped to [[0,1],[-1,0]] -- this struct will support more than one king on a square
        board_i = 0
        for board_i in range(n):
            board_t = [i for i in str(input().strip())]
            board_tt = []
            for i in board_t:
                if i == 'X':
                    j = -1
                if i == '.':
                    j = 0
                if i == 'K':
                    j = 1
                board_tt.append(j)
            board_tt = tuple(board_tt)
            board.append(board_tt)
        board = tuple(board)  # Make board hashable

        # Write Your Code Here
        # Return the number of ways the first player to move can force the win
        headleaf = Leaf(board, turn="B")
        num_winnable = headleaf.number_winnable()
        if DEBUG: headleaf.print_board_stats()

        if DEBUG: print("Final dict:\n{}".format(winnable_d))
        if num_winnable > 0:
            print("WIN", num_winnable)
        else:
            print("LOSE")