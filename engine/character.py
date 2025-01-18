import math

import arcade

class Character(arcade.Sprite):
    """Класс персонажа"""

    def __init__(self, image_idle, scaling, speed):
        super().__init__(image_idle, scaling)
        self.speed = speed
        self.textures_idle = [arcade.load_texture(image_idle)]
        self.textures_walk = []
        self.animation_timer = 0  # Таймер для анимации
        self.animation_speed = 0.2  # Скорость анимации (секунды на кадр)
        self.current_texture_index = 0  # Индекс текущей текстуры
        self.is_walking = False  # Состояние ходьбы

        self.step_timer = 0  # Таймер для звуков шагов

        class Dirs:
            up = False
            down = False
            right = False
            left = False

        self.move_dirs = Dirs()

    def setup_animations(self, walk_textures):
        """Настройка анимаций ходьбы"""
        self.textures_walk = [arcade.load_texture(tex) for tex in walk_textures]

    def update_animation(self, delta_time: float = 1 / 60):
        """Обновление анимации"""
        self.animation_timer += delta_time

        # Определяем, ходит ли персонаж
        self.is_walking = self.change_x != 0 or self.change_y != 0

        if not self.is_walking:
            # Если персонаж стоит, устанавливаем текстуру Idle
            self.texture = self.textures_idle[0]
            self.current_texture_index = 0
            self.animation_timer = 0  # Сброс таймера для ходьбы
            return

        # Обновление кадра ходьбы
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0  # Сбрасываем таймер
            self.current_texture_index += 1  # Переходим к следующему кадру

            # Зацикливаем индекс
            if self.current_texture_index >= len(self.textures_walk):
                self.current_texture_index = 0

            # Устанавливаем текстуру для кадра
            self.texture = self.textures_walk[self.current_texture_index]


    def update(self, delta_time: float = 1 / 60, mouse_pos=None, cam_pos=None):
        """Обновление состояния персонажа"""
        # Вызов существующих обновлений
        if mouse_pos is None:
            mouse_pos = [0, 0]
        if cam_pos is None:
            cam_pos = [0, 0]
        super().update()

        # Получаем позицию курсора
        mouse_x, mouse_y = mouse_pos

        # Вычисляем угол между персонажем и курсором
        dx = mouse_x - self.center_x + cam_pos[0]
        dy = mouse_y - self.center_y + cam_pos[1]
        angle = math.atan2(dy, dx)

        # Поворот текстуры
        self.angle = math.degrees(angle)

        # Обновляем анимацию
        self.update_animation(delta_time)

    def move(self):
        # Сбрасываем скорость
        self.change_x = 0
        self.change_y = 0

        # Направления движения
        sin = 0
        cos = 0
        sin += self.move_dirs.up
        sin -= self.move_dirs.down
        cos += self.move_dirs.right
        cos -= self.move_dirs.left

        # Диагональное движение
        if cos != 0 and sin != 0:
            move_y = sin / math.sqrt(2)
            move_x = cos / math.sqrt(2)
        else:
            move_y = sin
            move_x = cos

        # Устанавливаем скорость
        self.change_x = move_x * self.speed
        self.change_y = move_y * self.speed

