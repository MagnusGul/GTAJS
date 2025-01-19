import arcade

class CameraManager:
    """
    Класс для управления камерой, позволяющий плавно следить за объектами и учитывать положение мыши.
    """
    def __init__(self, width: int, height: int):
        """
        Инициализирует камеру с заданной шириной и высотой.

        :param width: Ширина экрана в пикселях.
        :param height: Высота экрана в пикселях.
        """
        self.camera = arcade.Camera(width, height)
        self.target_position: tuple[float, float] = (0, 0)  # Текущая позиция камеры
        self.mouse_offset: tuple[float, float] = (0, 0)  # Смещение камеры в зависимости от мыши
        self.width: int = width
        self.height: int = height
        self.offset_multiply: int = 1  # Множитель для усиления смещения камеры

    def update(self, target_x: float, target_y: float, level_width: float, level_height: float):
        """
        Обновляет положение камеры, плавно перемещая её к целевой позиции.

        :param target_x: Координата X целевого объекта.
        :param target_y: Координата Y целевого объекта.
        :param level_width: Ширина уровня в пикселях.
        :param level_height: Высота уровня в пикселях.
        """
        # Рассчитываем желаемую позицию камеры, центрированную на целевом объекте
        desired_x = target_x - self.width // 2 + self.mouse_offset[0] * self.offset_multiply
        desired_y = target_y - self.height // 2 + self.mouse_offset[1] * self.offset_multiply

        # Ограничиваем положение камеры в пределах размеров уровня
        desired_x = max(0, min(desired_x, level_width - self.width))
        desired_y = max(0, min(desired_y, level_height - self.height))

        # Плавное движение камеры (интерполяция)
        smooth_factor = 0.1  # Чем меньше значение, тем плавнее перемещение
        self.target_position = (
            self.target_position[0] + (desired_x - self.target_position[0]) * smooth_factor,
            self.target_position[1] + (desired_y - self.target_position[1]) * smooth_factor
        )

        # Перемещаем камеру в новую позицию
        self.camera.move_to(self.target_position)

    def set_mouse_offset(self, mouse_x: float, mouse_y: float):
        """
        Устанавливает смещение камеры в зависимости от положения мыши на экране.

        :param mouse_x: Текущая координата X мыши.
        :param mouse_y: Текущая координата Y мыши.
        """
        center_x = self.width // 2
        center_y = self.height // 2
        max_offset = 100  # Максимальное смещение камеры от центра экрана в пикселях

        # Рассчитываем нормализованное смещение относительно центра экрана
        offset_x = (mouse_x - center_x) / center_x * max_offset
        offset_y = (mouse_y - center_y) / center_y * max_offset

        self.mouse_offset = (offset_x, offset_y)

    def resize(self, width: int, height: int):
        """
        Обновляет размер камеры при изменении размеров окна.

        :param width: Новая ширина экрана в пикселях.
        :param height: Новая высота экрана в пикселях.
        """
        self.camera.resize(width, height)

    def use(self):
        """
        Активирует текущую камеру для последующей отрисовки.
        """
        self.camera.use()
