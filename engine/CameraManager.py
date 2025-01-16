import arcade

class CameraManager:
    """Класс для управления камерой"""
    def __init__(self, width, height):
        self.camera = arcade.Camera(width, height)
        self.target_position = (0, 0)
        self.mouse_offset = (0, 0)  # Смещение от мыши
        self.width = width
        self.height =height
        self.offset_multiply = 1

    def update(self, target_x, target_y, level_width, level_height):
        """Обновляет положение камеры с плавным переходом"""
        # Рассчитываем желаемую позицию камеры, центрированную на персонаже
        desired_x = target_x - self.width // 2 + self.mouse_offset[0] * self.offset_multiply
        desired_y = target_y - self.height // 2 + self.mouse_offset[1] * self.offset_multiply

        # Ограничиваем положение камеры в пределах уровня
        desired_x = max(0, min(desired_x, level_width - self.width))
        desired_y = max(0, min(desired_y, level_height - self.height))

        # Плавное движение камеры (интерполяция)
        smooth_factor = 0.1  # Чем меньше значение, тем плавнее движение
        self.target_position = (
            self.target_position[0] + (desired_x - self.target_position[0]) * smooth_factor,
            self.target_position[1] + (desired_y - self.target_position[1]) * smooth_factor
        )

        # Перемещаем камеру
        self.camera.move_to(self.target_position)

    def set_mouse_offset(self, mouse_x, mouse_y):
        """Рассчитывает смещение камеры в зависимости от положения мыши"""
        center_x = self.width // 2
        center_y = self.height // 2
        max_offset = 100  # Максимальное смещение камеры от центра экрана

        # Рассчитываем нормализованное смещение от центра экрана
        offset_x = (mouse_x - center_x) / center_x * max_offset
        offset_y = (mouse_y - center_y) / center_y * max_offset

        self.mouse_offset = (offset_x, offset_y)

    def resize(self, width, height):
        """Обновляет размер камеры"""
        self.camera.resize(width, height)

    def use(self):
        """Активирует камеру"""
        self.camera.use()
