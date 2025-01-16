import pyglet.math as pm

from engine import *

# Константы экрана
SCREEN_TITLE = "Игра с ООП"

# Константы карты
TILE_SCALING = 2.0
MAP_FILE = "C:\\Users\\Musa\\Chat\\GTAJS\\desertmap\\desert.tmx"

# Константы персонажа
CHARACTER_SCALING = 1.0
CHARACTER_SPEED = 5

# Константы консоли
CONSOLE_HEIGHT = 150
FONT_SIZE = 14


class Game(arcade.Window):
    def __init__(self):
        super().__init__(title=SCREEN_TITLE, fullscreen=True)
        arcade.set_background_color(arcade.color.AMAZON)
        print(self.screen.width, self.screen.height)
        # Камера
        self.camera_manager = CameraManager(self.screen.width, self.screen.height)

        # Консоль
        self.console = Console(self.screen.width, self.screen.height, FONT_SIZE)

        # Карта
        self.tile_map_manager = TileMapManager(MAP_FILE, TILE_SCALING)
        self.tile_map_manager.load_map()

        # Размеры уровня
        self.level_width = self.tile_map_manager.tile_map.width * self.tile_map_manager.tile_map.tile_width * TILE_SCALING
        self.level_height = self.tile_map_manager.tile_map.height * self.tile_map_manager.tile_map.tile_height * TILE_SCALING

        # Персонаж
        self.character = Character(":resources:images/animated_characters/female_person/femalePerson_idle.png", CHARACTER_SCALING, CHARACTER_SPEED)
        self.character.setup_animations([
            ":resources:images/animated_characters/female_person/femalePerson_walk0.png",
            ":resources:images/animated_characters/female_person/femalePerson_walk1.png",
        ])
        self.character.center_x = 100
        self.character.center_y = 100

    def on_draw(self):
        """Отрисовка экрана"""
        arcade.start_render()

        # Использование камеры для карты и персонажей
        self.camera_manager.use()

        # Отрисовка карты
        self.tile_map_manager.draw()

        # Отрисовка персонажа
        self.character.draw()

        # Отрисовка консоли
        if self.console.is_active:
            self.console.draw()


    def on_update(self, delta_time):
        """Обновление состояния игры"""
        self.character.update()
        self.character.update_animation(delta_time)
        if self.character.move():
            self.camera_manager.camera.shake(pm.Vec2(1, 1))

        # Обновление камеры с учётом размеров уровня
        self.camera_manager.update(
            self.character.center_x,
            self.character.center_y,
            self.level_width,
            self.level_height
        )

        # Проверка столкновений
        if arcade.check_for_collision_with_list(self.character, self.tile_map_manager.wall_list):
            self.character.change_x = 0
            self.character.change_y = 0

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if key == arcade.key.W:
            self.character.move_dirs.up = True
        elif key == arcade.key.S:
            self.character.move_dirs.down = True
        elif key == arcade.key.A:
            self.character.move_dirs.left   = True
        elif key == arcade.key.D:
            self.character.move_dirs.right = True

        if key == arcade.key.F1:
            self.console.is_active = not self.console.is_active

    def on_key_release(self, key, modifiers):
        """Обработка отпусканий клавиш"""
        if key == arcade.key.W:
            self.character.move_dirs.up = False
        elif key == arcade.key.S:
            self.character.move_dirs.down = False
        elif key == arcade.key.A:
            self.character.move_dirs.left   = False
        elif key == arcade.key.D:
            self.character.move_dirs.right = False

    def on_text(self, text):
        """Обработка текстового ввода"""
        if self.console.is_active:
            self.console.append_text(text)

    def on_mouse_motion(self, x, y, dx, dy):
        """Обрабатывает движение мыши"""
        self.camera_manager.set_mouse_offset(x, y)

    def on_resize(self, width, height):
        """Обрабатывает изменение размера окна"""
        super().on_resize(width, height)
        self.camera_manager.camera.resize(width, height)
# Запуск игры
if __name__ == "__main__":
    game = Game()
    arcade.run()
