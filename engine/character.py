import arcade

class Character(arcade.Sprite):
    """Класс персонажа"""
    def __init__(self, image_idle, scaling, speed):
        super().__init__(image_idle, scaling)
        self.speed = speed
        self.textures_idle = [arcade.load_texture(image_idle)]
        self.textures_walk = []

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
        if self.change_x != 0 or self.change_y != 0:
            self.texture = self.textures_walk[int(self.center_x // 10) % len(self.textures_walk)]
        else:
            self.texture = self.textures_idle[0]

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

