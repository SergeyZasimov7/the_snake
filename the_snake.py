from random import choice, randint
import pygame  # Сократить на pg не дает тренажер из-за проверки conftest.py
import sys

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION_DICT = {
    (UP, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_RIGHT): RIGHT,
    (LEFT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_UP): UP,
    (RIGHT, pygame.K_DOWN): DOWN
}

BOARD_BACKGROUND_COLOR = (197, 197, 197)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 10
# Переменная для хранения текущей скорости
speed = SPEED
# Рекордная длина, по умолчанию 1
record_length = 1
# Минимальная и максимальная скорость
MIN_SPEED = 5
MAX_SPEED = 60

# Величина изменения скорости
SPEED_INCREMENT = 1

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

# В метод __init__ присваиваю значения по умолчанию из-за проверки
# confest.py: Если в конструктор класса `GameObject` помимо параметра `self`
# передаются какие-то ещё параметры - убедитесь, что для них установлены
# значения по умолчанию.
    def __init__(self, position=None, color=None):
        """Конструктор класса, который инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = position
        self.body_color = color

    def cell_rendering(self, surface, position, color=None):
        """Метод для отрисовки одной ячейки"""
        color = color or self.body_color
        pygame.draw.rect(surface, color, (position,
                         (GRID_SIZE, GRID_SIZE)))

    def draw(self):
        """Абстрактный метод, который предназначен для переопределения в
        дочерних классах
        """
        raise NotImplementedError('this should never happen')


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self, position=None,
                 color=APPLE_COLOR):
        """Конструктор класса, который задает цвет яблока и вызывает метод
        randomize_position, чтобы установить начальную позицию яблока.
        """
        super().__init__(position, color)

    def randomize_position(self, positions):
        """Устанавливает случайное положение яблока на игровом поле —
        задаёт атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in positions:
                break

    def draw(self, surface):
        """Отрисовывает яблоко."""
        self.cell_rendering(surface, self.position)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self, position=CENTER, color=SNAKE_COLOR):
        """Конструктор класса, инициализирующий начальное состояние
        змейки.
        """
        super().__init__(position, color)
        self.reset()

    def update_direction(self, direction):
        """Метод обновления направления после нажатия на кнопку."""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции), добавляя
        новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        x, y = self.get_head_position()
        direction_x, direction_y = self.direction
        x = (x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        y = (y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        if (x, y) in self.positions:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            self.positions.insert(0, (x, y))
            self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        # Хвост змеи
        self.cell_rendering(surface, self.positions[-1])

        # Отрисовка головы змейки
        self.cell_rendering(surface, self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            self.cell_rendering(surface, self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки (1-й элемент в списке
        positions)
        """
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def program_exit():
    """Выход из системы"""
    pygame.quit()
    sys.exit()


def update_display_caption():
    """Функция обновления заголовка дисплея"""
    pygame.display.set_caption(
        f"Змейка | Скорость: {speed} | Рекорд: {record_length} | "
        f"F1/F2: изменение скорости | Esc: выход"
    )


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    global speed, record_length
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_exit()
        elif event.type == pygame.KEYDOWN:
            current_direction = game_object.direction
            game_object.update_direction(DIRECTION_DICT.get((current_direction,
                                         event.key), current_direction))
            if event.key == pygame.K_F1:
                speed = min(MAX_SPEED, speed + SPEED_INCREMENT)
            elif event.key == pygame.K_F2:
                speed = max(MIN_SPEED, speed - SPEED_INCREMENT)
            elif event.key == pygame.K_ESCAPE:
                program_exit()
            update_display_caption()


def main():
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения
    змейки
    """
    global record_length
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(speed)
        handle_keys(snake)
        update_display_caption()
        snake.move()
        apple.draw(screen)
        snake.draw(screen)

        if snake.positions[0] == apple.position:
            snake.length += 1
            record_length = max(record_length, snake.length)
            apple.randomize_position(snake.positions)

        pygame.display.update()


if __name__ == '__main__':
    main()
