import random
from copy import deepcopy
from .errors import BadWords, EmptyPurse, NotInRack, ScrabbleError, UnavailableLanguage
from .helpers import get_avail_langs
from .items import Board, Player, Purse, Word, Tile


class Scrabble:
    df_board_size = 15
    df_rack_size = 7
    df_lang = 'fr'
    df_players = [
        Player('player_1'),
        Player('player_2')
    ]

    def __init__(self, players: list[Player] = None, purse: Purse = None, board: Board = None, **scrabble_config) -> None:
        if players is None:
            players = Scrabble.df_players
        if len(players) > 4:
            raise ScrabbleError('4 players max')

        self.players = {player.ID: player for player in players}
        self.players_ids = [*self.players.keys()]
        self.nb_players = len(self.players)

        self.BOARD_SIZE = scrabble_config.get(
            'board_size', Scrabble.df_board_size)
        self.RACK_SIZE = scrabble_config.get(
            'rack_size', Scrabble.df_rack_size)
        self.LANG = scrabble_config.get(
            'lang', Scrabble.df_lang)
        if self.LANG not in get_avail_langs():
            raise UnavailableLanguage(unavail_lang=self.LANG)

        self.turn = scrabble_config.get('turn', 0)
        self.turn_rand = scrabble_config.get(
            'turn_rand', random.randint(0, self.nb_players-1))
        self.turn_id = self.__get_turn_id()
        self.history = scrabble_config.get('history', {})

        self.purse = purse
        self.board = board
        if purse is None or board is None:
            self.__initialize_game()
        self.display_info()

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Scrabble) and self.players == __o.players and self.turn == __o.turn and self.turn_id == __o.turn_id and self.history == __o.history and self.purse == __o.purse and self.board == __o.board

    def __initialize_game(self) -> None:
        self.purse = Purse(lang=self.LANG)
        self.board = Board(size=self.BOARD_SIZE)
        for _ in range(self.RACK_SIZE):
            for player_id in self.players:
                rack = self.players[player_id].rack
                rack.extend(self.purse.draw())

    def __get_turn_id(self) -> str:
        return self.players_ids[(self.turn + self.turn_rand) % self.nb_players]

    def save_move(self, move) -> None:
        new_words = self.board.get_next_words(move)
        scored_points = self.board.get_points(move)
        self.history[self.turn] = new_words
        self.players[self.turn_id].score += scored_points
        self.board.add_tiles(move)
        self.turn += 1
        self.turn_id = self.__get_turn_id()

    def display_info(self) -> None:
        scores = [self.players[player_id].score for player_id in self.players_ids]
        print('Scores:')
        print(*zip(self.players_ids, scores))
        print(self.board)
        print(f'Player turn: {self.turn_id}')
        print(self.players[self.turn_id].rack)

    def check_n_format_move(self, move):
        move_letters = list(move.values())
        temp_rack = deepcopy(self.players[self.turn_id].rack)
        for letter in move_letters:
            try:
                temp_rack.remove(Tile(letter))
            except ValueError as e:
                raise NotInRack from e
        return [Tile(move[pos], pos) for pos in move.keys()]

    def update_rack(self, move):
        letters = list(move.values())
        rack = self.players[self.turn_id].rack
        for letter in letters:
            rack.remove(Tile(letter))
            rack.extend(self.purse.draw())

    # move: {(x, y): letter}, dict(pos:str)

    def submit(self, move) -> None:
        try:
            print('move submission')
            move_formated = self.check_n_format_move(move)
            next_words = self.board.get_next_words(move_formated)
        except BadWords as err:
            print('BadWords Error:')
            print(f'These words are unvalid : {err.bad_words}')
            print(f'These words are valid: {err.good_words}')
        except ScrabbleError as e:
            print('Scrabble Error')
            print(f'Type: {type(e).__name__}')
            print(e.__dict__)
        else:
            print(f'Added words: {next_words}')
            self.update_rack(move)
            self.save_move(move_formated)
        finally:
            self.display_info()

    def cli_play(self):
        raise NotImplementedError