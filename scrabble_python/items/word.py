from .tile import Tile
from scrabble_python.helpers import create_dictionary


class Word:
    def __init__(self, text: str, start: list, direction='H', lang='fr'):
        self.score = 0
        self.text = text.upper()
        self.LANG = lang
        self.start = tuple(start)
        if direction not in ['V', 'H', 0, 1]:
            raise ValueError(
                'direction is (H or 0)for Horizontal, or V (or 1) for Vertical')
        self.direction = direction
        if direction in ['H', 0]:
            self.tiles = [Tile(lettre, (start[0], start[1] + i))
                          for (i, lettre) in enumerate(self.text)]
        else:
            self.tiles = [Tile(lettre, (start[0] + i, start[1]))
                          for (i, lettre) in enumerate(self.text)]
        self.end = self.tiles[-1].pos
        self.score = self.get_initial_score()

    def __str__(self) -> str:
        return f'{self.text}: {self.start} -> {self.end}'

    def __repr__(self) -> str:
        return f'Word({self.text}, {self.start}, {self.direction}, {self.score})'

    def __len__(self):
        return len(self.tiles)

    def __bool__(self):
        dico = create_dictionary(self.LANG)
        return self.text.lower() in dico

    def __eq__(self, other) -> int:
        return isinstance(other, Word) \
            and self.text == other.text \
            and self.start == other.start \
            and self.end == other.end

    def get_initial_score(self):
        values = [tile.value for tile in self.tiles]
        return sum(values)
