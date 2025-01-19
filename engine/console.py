import arcade
from .character import load_character

class Console:
    """
    Класс консоли для обработки ввода и вывода.
    """
    def __init__(self, game: arcade.Window):
        """
        Инициализация консоли.

        :param game: Экземпляр игры, к которому привязана консоль.
        """
        self.game = game
        self.width: int = self.game.width
        self.height: int = self.game.height
        self.font_size: int = self.game.font_size
        self.lines: list[str] = ["Добро пожаловать в консоль! Напишите 'help' для списка команд."]
        self.current_input: str = ""
        self.is_active: bool = False

    def draw(self):
        """
        Рисует консоль на экране.
        """
        camera = self.game.camera_manager.camera
        y_offset = 40

        # Рисуем фон консоли
        arcade.draw_polygon_filled(
            (
                (camera.position[0], camera.position[1]),
                (camera.position[0], 200 + camera.position[1]),
                (self.game.camera_manager.width + camera.position[0], 200 + camera.position[1]),
                (self.game.width + camera.position[0], camera.position[1])
            ),
            (0, 0, 0, 100)
        )

        # Рисуем строки текста консоли
        for line in reversed(self.lines[-10:]):  # Отображаем последние 10 строк
            arcade.draw_text(
                line,
                10 + camera.position[0],
                y_offset + camera.position[1],
                arcade.color.WHITE,
                self.font_size
            )
            y_offset += self.font_size + 2

        # Рисуем текущий ввод пользователя
        arcade.draw_text(
            f"> {self.current_input}",
            10 + camera.position[0],
            10 + camera.position[1],
            arcade.color.YELLOW,
            self.font_size
        )

    def process_key_press(self, key: int):
        """
        Обрабатывает нажатия клавиш.

        :param key: Код нажатой клавиши.
        """
        if self.is_active:
            if key == arcade.key.ENTER:
                # Обработка команды
                command = self.current_input.strip().split()
                self.lines.append(f"> {self.current_input}")
                self.current_input = ""

                if not command:
                    return

                if command[0] == "help":
                    self.lines.append("Доступные команды: help, exit, map, character")

                elif command[0] == "exit":
                    self.lines.append("Выход из игры...")
                    arcade.exit()

                elif command[0] == "map":
                    if len(command) > 1:
                        map_name = command[1]
                        try:
                            self.game.tile_map_manager.load_map(self.game, map_name, 2)
                            self.lines.append(f"Карта {map_name} успешно загружена")
                        except FileNotFoundError:
                            self.lines.append(f"Карта {map_name} не найдена")
                    else:
                        self.lines.append("Ошибка: укажите имя карты.")

                elif command[0] == "character":
                    if len(command) > 1:
                        character_name = command[1]
                        self.game.character = load_character(character_name)
                        self.game.character.physics_engine = arcade.PhysicsEngineSimple(
                            self.game.character,
                            self.game.tile_map_manager.wall_list
                        )
                        self.lines.append(f"Персонаж {character_name} успешно загружен")
                    else:
                        self.lines.append("Ошибка: укажите имя персонажа.")

                else:
                    self.lines.append(f"Неизвестная команда: {command[0]}")

            elif key == arcade.key.BACKSPACE:
                # Удаляем последний символ в текущем вводе
                self.current_input = self.current_input[:-1]

        if key == arcade.key.F1:
            # Включение/выключение консоли
            self.is_active = not self.is_active

    def append_text(self, text: str):
        """
        Добавляет текст в текущий ввод.

        :param text: Текст для добавления.
        """
        self.current_input += text
