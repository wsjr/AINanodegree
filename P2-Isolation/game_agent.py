"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    """
    Returns a score for a game state and player based on his moves and
    opponent moves
    :param game:
    :param player:
    :param factor: weight of opponent moves
    :return:
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(my_moves - 2*opponent_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    """
    Returns a score for a game state and player based on his moves and
    opponent moves putting more weight on centric moves.
    :param game:
    :param player:
    :return:
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_weighted_score = 0
    for move in game.get_legal_moves(player):
        my_weighted_score = my_weighted_score + add_move_weight(game, move)

    opp_weighted_score = 0
    for move in game.get_legal_moves(game.get_opponent(player)):
        opp_weighted_score = opp_weighted_score + add_move_weight(game, move)

    return float(my_weighted_score - opp_weighted_score)

def add_move_weight(game, move, factor=1):
    weight = 1
    # Move has atleast 2 blocks from the edge. There's a possibility it can move to all directions.
    if (move[0] >= 2 and move[0] < game.height - 2) and (move[1] >= 2 and move[1] < game.width - 2):
        weight = 10 * factor
    # Move has atleast one block from the edge. Less moves available.
    elif (move[0] >= 1 and move[0] < game.height - 1) and (move[1] >= 1 and move[1] < game.width - 1):
        weight = 5 * factor
    
    
    return weight

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    """
    Returns a score for a game state and player based on his and opponent's current and future moves
    :param game:
    :param player:
    :return:
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_player = game.get_opponent(player)

    my_weighted_score = 0
    for move in game.get_legal_moves(player):
        my_weighted_score = my_weighted_score + add_move_weight(game, move)
        game_ahead = game.forecast_move(move)
        for move_ahead in game_ahead.get_legal_moves(player):
            my_weighted_score = my_weighted_score + add_move_weight(game_ahead, move_ahead, 2)

    opp_weighted_score = 0
    for move in game.get_legal_moves(opp_player):
        opp_weighted_score = opp_weighted_score + add_move_weight(game, move)
        game_ahead = game.forecast_move(move)
        for move_ahead in game_ahead.get_legal_moves(opp_player):
            opp_weighted_score = opp_weighted_score + add_move_weight(game_ahead, move_ahead, 2)

    return float(my_weighted_score - opp_weighted_score)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return (-1, -1)

        best_score = float("-inf")
        best_move = None
        for m in game.get_legal_moves():    
            v = self.mm_min_value(game.forecast_move(m), depth-1)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move


    def terminal_test(self, game):
        """ Return True if the game is over for the active player
        and False otherwise.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not bool(game.get_legal_moves())  # by Assumption 1      

    def mm_min_value(self, game, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Deepest depth or last node reached.
        if depth == 0 or self.terminal_test(game):
            return self.score(game, self)

        v = float("inf")
        for m in game.get_legal_moves():
            v = min(v, self.mm_max_value(game.forecast_move(m), depth-1))
        return v

    def mm_max_value(self, game, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Deepest depth or last node reached.
        if depth == 0 or self.terminal_test(game):
            return self.score(game, self)

        v = float("-inf")
        for m in game.get_legal_moves():
            v = max(v, self.mm_min_value(game.forecast_move(m), depth-1))
        return v



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while (True):
                best_move = self.alphabeta(game, depth)
                depth = depth +1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Deepest depth reached.
        if depth == 0:
            return (-1, -1)        

        best_score = alpha
        best_move = None
        for move in game.get_legal_moves():
            child_score = self.ab_min_value(game.forecast_move(move), depth-1, best_score, beta)
            if child_score > best_score:
                best_score = child_score
                best_move = move
            if beta <= best_score:
                break
        return best_move


        return best_move

    def terminal_test(self, game):
        """ Return True if the game is over for the active player
        and False otherwise.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return not bool(game.get_legal_moves())  # by Assumption 1      

    def ab_max_value(self, game, depth, alpha, beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Deepest depth or last node reached.
        if depth == 0 or self.terminal_test(game):
            return self.score(game, self)
        
        best_value = alpha
        for move in game.get_legal_moves():
            child_value = self.ab_min_value(game.forecast_move(move), depth-1, best_value, beta)
            best_value = max(best_value, child_value)
            if beta <= best_value:
                break
        return best_value
    
    def ab_min_value(self, game, depth, alpha, beta):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Deepest depth or last node reached.
        if depth == 0 or self.terminal_test(game):
            return self.score(game, self)
        
        best_value = beta
        for move in game.get_legal_moves():
            child_value = self.ab_max_value(game.forecast_move(move), depth-1, alpha, best_value)
            best_value = min(best_value, child_value)
            if best_value <= alpha:
                break
        return best_value        
