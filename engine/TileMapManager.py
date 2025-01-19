import arcade
from arcade import Window as GameWindow


class TileMapManager:
    """Класс для управления картами Tiled."""

    def __init__(self):
        # Путь к файлу карты
        self.map_file: str | None = None
        # Масштаб карты
        self.scaling: float | None = None
        # Объект карты Tiled
        self.tile_map: arcade.TileMap | None = None
        # Список спрайтов для слоя "Walls"
        self.wall_list: arcade.SpriteList | None = None
        # Ширина уровня в пикселях
        self.level_width: float | None = None
        # Высота уровня в пикселях
        self.level_height: float | None = None

    def load_map(self, game: GameWindow, map_file: str, scaling: float) -> None:
        """Загружает карту из Tiled.

        Аргументы:
        - game (GameWindow): Экземпляр игрового окна.
        - map_file (str): Имя файла карты (без пути и расширения).
        - scaling (float): Коэффициент масштабирования карты.
        """
        # Формируем полный путь к файлу карты
        self.map_file = f"maps/{map_file}/map.tmx"
        self.scaling = scaling

        # Загружаем карту Tiled
        self.tile_map = arcade.load_tilemap(self.map_file, self.scaling)

        # Получение списка объектов из слоя "Walls"
        self.wall_list = self.tile_map.sprite_lists.get("Walls")

        # Устанавливаем начальную позицию персонажа, если он существует
        if hasattr(game, "character") and game.character is not None:
            game.character.center_x = self.tile_map.properties.get("player_pos_x", 0)
            game.character.center_y = self.tile_map.properties.get("player_pos_y", 0)

            # Создаем простой физический движок для персонажа
            game.character.physics_engine = arcade.PhysicsEngineSimple(
                game.character, self.wall_list
            )

        # Вычисляем размеры уровня
        if self.tile_map:
            self.level_width = (
                self.tile_map.width * self.tile_map.tile_width * self.scaling
            )
            self.level_height = (
                self.tile_map.height * self.tile_map.tile_height * self.scaling
            )

    def draw(self) -> None:
        """Рисует карту."""
        if self.tile_map and self.tile_map.sprite_lists:
            for sprite_list in self.tile_map.sprite_lists.values():
                sprite_list.draw()

    def get_wall_list(self) -> arcade.SpriteList | None:
        """Возвращает список стен для физики."""
        return self.wall_list