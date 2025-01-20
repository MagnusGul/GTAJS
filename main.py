from engine import *

class Game(arcade.Window):
    def __init__(
        self,
        screen_title="game",
        font_size=14
    ):
        super().__init__(title=screen_title, fullscreen=True, vsync=True)
        arcade.set_background_color(arcade.color.AMAZON)

        # Камера
        self.camera_manager = CameraManager(self.screen.width, self.screen.height)

        # Консоль
        self.font_size = font_size
        self.console = Console(self)

        # Карта
        self.tile_map_manager = TileMapManager()
        # Персонаж
        self.character = None

        self.character = load_character("girl")
        self.character.physics_engine = arcade.PhysicsEngineSimple(self.character, self.tile_map_manager.wall_list)
        self.tile_map_manager.load_map(self, "testmap", 2)

    def on_draw(self):
        """Отрисовка экрана"""
        arcade.start_render()

        # Использование камеры для карты и персонажей
        self.camera_manager.use()

        # Отрисовка карты и персонажа
        self.tile_map_manager.draw()
        if self.character is not None:
            self.character.draw()

        # Отрисовка консоли
        self.console.draw()

    def on_update(self, delta_time):
        """Обновление состояния игры"""
        if self.character is not None:
            self.character.update(
                mouse_pos=(self._mouse_x, self._mouse_y),
                cam_pos=self.camera_manager.camera.position
            )
            self.character.move()
            self.character.physics_engine.update()
            self.character.update_animation(delta_time)

            # Обновление камеры с учётом размеров уровня
            if self.tile_map_manager.tile_map is not None:
                self.camera_manager.update(
                    self.character.center_x,
                    self.character.center_y,
                    self.tile_map_manager.level_width,
                    self.tile_map_manager.level_height
                )

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if not self.console.is_active and self.character is not None:
            movement_keys = {
                arcade.key.W: "up",
                arcade.key.S: "down",
                arcade.key.A: "left",
                arcade.key.D: "right"
            }
            if key in movement_keys:
                setattr(self.character.move_dirs, movement_keys[key], True)
            if key == arcade.key.LSHIFT:
                self.character.is_running = True
        self.console.process_key_press(key)


    def on_key_release(self, key, modifiers):
        """Обработка отпусканий клавиш"""
        if not self.console.is_active and self.character is not None:
            movement_keys = {
                arcade.key.W: "up",
                arcade.key.S: "down",
                arcade.key.A: "left",
                arcade.key.D: "right"
            }
            if key in movement_keys:
                setattr(self.character.move_dirs, movement_keys[key], False)

            if key == arcade.key.LSHIFT:
                self.character.is_running = False

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

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.camera_manager.offset_multiply = 4

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.camera_manager.offset_multiply = 1

# Запуск игры
if __name__ == "__main__":
    game = Game("Grand Thieves Almetyevsk: Jumbulstan Stories")
    arcade.run()