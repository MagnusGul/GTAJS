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

        # Получение списка объектов из слоя "Walls"
        walls_layer = self.tile_map.object_lists.get("Walls")
        if walls_layer:
            self.wall_list = [
                obj for obj in walls_layer if obj.properties.get("type") == "wall"
            ]
        else:
            self.wall_list = []

        print(f"Найдено объектов стен: {len(self.wall_list)}")

    def draw(self):
        """Рисует карту"""
        if self.tile_map and self.tile_map.sprite_lists:
            for sprite_list in self.tile_map.sprite_lists.values():
                sprite_list.draw()

    def get_wall_list(self):
        """Возвращает список стен для физики"""
        return self.wall_list