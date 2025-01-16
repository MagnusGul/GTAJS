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
        if self.animation_timer < self.animation_speed:
            return  # Ждем до следующего кадра

        # Сброс таймера
        self.animation_timer = 0

        if self.change_x != 0 or self.change_y != 0:
            # Проверка на направление движения по осям X и Y
            if abs(self.change_x) > abs(self.change_y):
                self.texture = self.textures_walk[int(self.center_x // 10) % len(self.textures_walk)]
            else:
                self.texture = self.textures_walk[int(self.center_y // 10) % len(self.textures_walk)]
        else:
            self.texture = self.textures_idle[0]


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
        sin = 0
        cos = 0
        sin += self.move_dirs.up
        sin -= self.move_dirs.down
        cos += self.move_dirs.right
        cos -= self.move_dirs.left

        if cos != 0 and sin != 0:
            move_y = 0.7 * sin
            move_x = 0.7 * cos
        else:
            move_y = sin
            move_x = cos

        self.change_x = move_x * self.speed
        self.change_y = move_y * self.speed

