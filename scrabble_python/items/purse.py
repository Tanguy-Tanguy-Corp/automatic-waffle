import random
from scrabble_python.errors import EmptyPurse
from scrabble_python.helpers import create_distribution
from .tile import Tile


class Purse:
    def __init__(self, dist: dict = None, lang: str = 'fr') -> None:
        self.LANG = lang
        self.tiles = self.__init_purse() if dist is None else self.__init_from_dist(dist)

    def __init_purse(self) -> list[Tile]:
        init_dist = create_distribution(self.LANG, 'dict')
        initial_purse_tiles = []
        for letter in init_dist:
            initial_purse_tiles.extend([Tile(letter)] * init_dist[letter]['count'])
        random.shuffle(initial_purse_tiles)
        return initial_purse_tiles

    def __init_from_dist(self, dist):
        purse_tiles = []
        for letter in dist:
            purse_tiles.extend([Tile(letter)] * dist[letter])
        random.shuffle(purse_tiles)
        return purse_tiles

    def shuffle(self):
        random.shuffle(self.tiles)

    def __len__(self) -> int:
        return len(self.tiles)

    def __str__(self) -> str:
        dist = self.get_dist()
        filt_dist = {letter: count for letter, count in dist.items() if count != 0}
        return(str(filt_dist))

    def __repr__(self) -> str:
        return(f'Purse({str(self.get_dist())})')

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Purse) and self.get_dist() == __o.get_dist()

    def get_dist(self) -> dict:
        """
        Return the letter distribution in the purse
        """
        init_dist = create_distribution(lang=self.LANG, format='dict')
        return {letter: sum(tile.letter == letter for tile in self.tiles) for letter in init_dist}

    def draw(self, n=1) -> list[Tile]:
        drawn_tiles = []
        for _ in range(n):
            if len(self) == 0:
                raise EmptyPurse
            drawn_tiles.append(self.tiles.pop())
        return drawn_tiles
