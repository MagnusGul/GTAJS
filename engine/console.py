import arcade

class Console:
    """Класс консоли для обработки ввода и вывода"""
    def __init__(self, width, height, font_size):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.lines = ["Добро пожаловать в консоль! Напишите 'help' для списка команд."]
        self.current_input = ""
        self.is_active = False

    def draw(self):
        """Рисует консоль на экране"""
        y_offset = 40
        for line in reversed(self.lines[-10:]):  # Отображаем последние 10 строк
            arcade.draw_text(line, 10, y_offset, arcade.color.WHITE, self.font_size)
            y_offset += self.font_size + 2

        # Текущий ввод пользователя
        arcade.draw_text(f"> {self.current_input}", 10, 10, arcade.color.YELLOW, self.font_size)

    def process_key_press(self, key):
        """Обрабатывает нажатия клавиш"""
        if key == arcade.key.ENTER:
            self.process_command(self.current_input)
            self.current_input = ""
        elif key == arcade.key.BACKSPACE:
            self.current_input = self.current_input[:-1]

    def append_text(self, text):
        """Добавляет текст в текущий ввод"""
        self.current_input += text

    def process_command(self, command):
        """Обрабатывает введённую команду"""
        command = command.strip()
        if not command:
            return

        self.lines.append(f"> {command}")
        if command.lower() == "help":
            self.lines.append("Доступные команды: help, exit")
        elif command.lower() == "exit":
            self.lines.append("Выход из игры...")
            raise SystemExit