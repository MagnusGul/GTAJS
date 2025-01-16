import arcade

class TileMapManager:
    """Класс для управления картами Tiled"""
    def __init__(self, map_file, scaling):
        self.map_file = map_file
        self.scaling = scaling
        self.tile_map = None
        self.wall_list = None

    def load_map(self):
        """Загружает карту из Tiled"""
        self.tile_map = arcade.load_tilemap(self.map_file, self.scaling)
        self.wall_list = self.tile_map.sprite_lists.get("Walls", arcade.SpriteList())

    def draw(self):
        """Рисует карту"""
        if self.tile_map and self.tile_map.sprite_lists:
            for sprite_list in self.tile_map.sprite_lists.values():
                sprite_list.draw()