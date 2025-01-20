import json
import math
import arcade


class Character(arcade.Sprite):
    """
    Класс персонажа, отвечающий за его движение, анимацию и взаимодействие с окружением.
    """

    def __init__(self, image_idle: str, scaling: float, speed: float, run_speed: float, walk_textures: list[str]):
        """
        Инициализация персонажа.

        :param image_idle: Путь к изображению для состояния покоя (Idle).
        :param scaling: Масштабирование спрайта.
        :param speed: Скорость движения персонажа.
        :param walk_textures: Список путей к изображениям для анимации ходьбы.
        """
        super().__init__(image_idle, scaling)
        self.speed: float = speed
        self.run_speed: float = run_speed
        self.textures_idle: list[arcade.Texture] = [arcade.load_texture(image_idle)]  # Текстуры для состояния покоя
        self.textures_walk: list[arcade.Texture] = [arcade.load_texture(tex) for tex in walk_textures]  # Текстуры для анимации ходьбы
        self.animation_timer: float = 0  # Таймер для анимации
        self.animation_speed: float = 0.2  # Скорость анимации (в секундах на кадр)
        self.current_texture_index: int = 0  # Индекс текущей текстуры
        self.is_walking: bool = False  # Флаг, указывающий, ходит ли персонаж
        self.is_running = False

        self.step_timer: float = 0  # Таймер для звуков шагов

        class Dirs:
            """Класс для хранения направлений движения персонажа."""
            up: bool = False
            down: bool = False
            right: bool = False
            left: bool = False

        self.move_dirs = Dirs()
        self.inertia_x: float = 0.0
        self.inertia_y: float = 0.0
        self.speed = speed
        self.acceleration = 0.1
        self.deceleration = 0.1
        self.change_x: float = 0.0
        self.change_y: float = 0.0
        self.physics_engine = None
        self.moving_params = None

    def update_animation(self, delta_time: float = 1 / 60):
        """
        Обновление анимации персонажа.

        :param delta_time: Время, прошедшее с последнего кадра.
        """
        self.animation_timer += delta_time

        # Проверяем, ходит ли персонаж
        self.is_walking = self.change_x != 0 or self.change_y != 0

        if not self.is_walking:
            # Если персонаж стоит, устанавливаем текстуру Idle
            self.texture = self.textures_idle[0]
            self.current_texture_index = 0
            self.animation_timer = 0  # Сброс таймера анимации
            return

        # Обновление кадра анимации ходьбы
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0  # Сбрасываем таймер
            self.current_texture_index += 1  # Переходим к следующему кадру

            # Зацикливаем индекс текстуры
            if self.current_texture_index >= len(self.textures_walk):
                self.current_texture_index = 0

            # Устанавливаем новую текстуру
            self.texture = self.textures_walk[self.current_texture_index]

    def update(self, delta_time: float = 1 / 60, mouse_pos: tuple[float, float] = None, cam_pos: tuple[float, float] = None):
        """
        Обновление состояния персонажа.

        :param delta_time: Время, прошедшее с последнего кадра.
        :param mouse_pos: Позиция мыши (X, Y).
        :param cam_pos: Позиция камеры (X, Y).
        """
        mouse_pos = mouse_pos or (0, 0)
        cam_pos = cam_pos or (0, 0)

        # Вызываем базовое обновление
        super().update()

        # Вычисляем угол между персонажем и мышью
        mouse_x, mouse_y = mouse_pos
        dx = mouse_x - self.center_x + cam_pos[0]
        dy = mouse_y - self.center_y + cam_pos[1]
        angle = math.atan2(dy, dx)

        # Поворачиваем персонаж в сторону мыши
        self.angle = math.degrees(angle)

        # Обновляем анимацию
        self.update_animation(delta_time)

    def move(self):
        """
        Рассчитывает и устанавливает скорость персонажа на основе направлений движения с учетом инерции.
        """

        speed = self.speed if not self.is_running else self.run_speed
        # Рассчитываем направления движения
        y = int(self.move_dirs.up) - int(self.move_dirs.down)
        x = int(self.move_dirs.right) - int(self.move_dirs.left)
        if y != 0 and x != 0:
            # Нормализуем скорость при движении по диагонали
            normalization_factor = 0.71
            target_x = x * speed * normalization_factor
            target_y = y * speed * normalization_factor
        else:
            target_x = x * speed
            target_y = y * speed

        # Обновляем инерцию по оси X
        if (target_x > 0 and self.inertia_x < target_x) or self.inertia_x < target_x:
            self.inertia_x += self.acceleration
            if self.inertia_x > target_x:
                self.inertia_x = target_x
        elif (target_x < 0 and self.inertia_x > target_x) or self.inertia_x > target_x:
            self.inertia_x -= self.acceleration
            if self.inertia_x < target_x:
                self.inertia_x = target_x

        # Обновляем инерцию по оси Y
        if (target_y > 0 and self.inertia_y < target_y) or self.inertia_y < target_y:
            self.inertia_y += self.acceleration
            if self.inertia_y > target_y:
                self.inertia_y = target_y
        elif (target_y < 0 and self.inertia_y > target_y) or self.inertia_y > target_y:
            self.inertia_y -= self.acceleration
            if self.inertia_y < target_y:
                self.inertia_y = target_y


        # Устанавливаем текущие скорости
        self.change_x = self.inertia_x
        self.change_y = self.inertia_y

        self.moving_params = {"y": y, "x": x, "target_x": target_x, "target_y": target_y}

    def __str__(self):
        """
        Возвращает строковое представление текущего состояния персонажа в формате списка атрибутов и их значений.
        """
        return (f"Speed: {self.speed}\n"
                f"Run speed: {self.run_speed}\n"
                f"Is Walking: {self.is_walking}\n"
                f"Is Running: {self.is_running}\n"
                f"Position: ({self.center_x / 64:.2f}, {self.center_y / 64:.2f})\n"
                f"Inertia X: {self.inertia_x:.2f}\n"
                f"Inertia Y: {self.inertia_y:.2f}\n"
                f"Move Directions: {self.move_dirs.__class__.__name__} (exists)\n"
                f"Physics Engine: {type(self.physics_engine).__name__ if self.physics_engine else 'None'}\n"
                f"{self.moving_params}")

def load_character(character_file: str) -> Character:
    """

    :param character_file: Путь к .json файлу с данными персонажа
    :return: Объект Character
    """
    with open(f"characters\\{character_file}.json", "r") as f:
        attributes = json.loads(f.read())
    return Character(*attributes.values())