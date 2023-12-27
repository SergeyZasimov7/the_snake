from random import choice, randint
import pygame as pg
import sys

# Инициализация PyGame
pg.init()

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

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (197, 197, 197)

# Скорость движения змейки
SPEED = 10
# Переменная для хранения текущей скорости
current_speed = SPEED
# Рекордная длина, по умолчанию 1
record_length = 1
# Минимальная и максимальная скорость
MIN_SPEED = 5
MAX_SPEED = 60

# Величина изменения скорости
SPEED_INCREMENT = 5

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени
clock = pg.time.Clock()


# Тут опишите все классы игры
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, position=None, color=None):
        """Конструктор класса, который инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = position
        self.body_color = color

    def cell_rendering(self, surface, position, color=None):
        """Метод для отрисовки одной ячейки"""
        if color is None:
            color = self.body_color
        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, color, rect)

    def draw(self):
        """Абстрактный метод, который предназначен для переопределения в
        дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self, position=None,
                 color=(255, 0, 0)):
        """Конструктор класса, который задает цвет яблока и вызывает метод
        randomize_position, чтобы установить начальную позицию яблока.
        """
        super().__init__(position, color)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока на игровом поле —
        задаёт атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in snake_positions:
                self.position = position
                break


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self, color=(0, 255, 0)):
        """Конструктор класса, инициализирующий начальное состояние
        змейки.
        """
        super().__init__(CENTER, color)
        self.reset()
        self.direction = RIGHT
        self.last = None

    def update_direction(self, direction):
        """Метод обновления направления после нажатия на кнопку."""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции), добавляя
        новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        x, y = self.get_head_position()
        if self.direction == RIGHT:
            x += GRID_SIZE
        elif self.direction == LEFT:
            x -= GRID_SIZE
        elif self.direction == UP:
            y -= GRID_SIZE
        elif self.direction == DOWN:
            y += GRID_SIZE
        x = x % SCREEN_WIDTH
        y = y % SCREEN_HEIGHT
        if (x, y) in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (x, y))
            self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        # Хвост змеи
        self.cell_rendering(surface, self.positions[-1], (93, 216, 228))

        # Отрисовка головы змейки
        self.cell_rendering(surface, self.positions[0], (93, 216, 228))

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
        screen.fill(BOARD_BACKGROUND_COLOR)


def program_exit():
    """Выход из системы"""
    pg.quit()
    sys.exit()


def update_display_caption():
    """Функция обновления заголовка дисплея"""
    pg.display.set_caption(
        f"Змейка | Скорость: {current_speed} | Рекорд: {record_length} |"
        f"+/-: изменение скорости | Esc: выход"
    )


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    global current_speed, record_length
    direction_dict = {
        (UP, pg.K_DOWN): UP,
        (DOWN, pg.K_UP): DOWN,
        (LEFT, pg.K_RIGHT): LEFT,
        (RIGHT, pg.K_LEFT): RIGHT,
        (UP, pg.K_LEFT): LEFT,
        (UP, pg.K_RIGHT): RIGHT,
        (DOWN, pg.K_LEFT): LEFT,
        (DOWN, pg.K_RIGHT): RIGHT,
        (LEFT, pg.K_UP): UP,
        (LEFT, pg.K_DOWN): DOWN,
        (RIGHT, pg.K_UP): UP,
        (RIGHT, pg.K_DOWN): DOWN
    }
    for event in pg.event.get():
        if event.type == pg.QUIT:
            program_exit()
        elif event.type == pg.KEYDOWN:
            current_direction = game_object.direction
            game_object.direction = direction_dict.get((current_direction,
                                                        event.key),
                                                       current_direction)
            if (event.key == pg.K_EQUALS or event.key == pg.K_PLUS
               or event.key == pg.K_KP_PLUS):
                current_speed = min(MAX_SPEED, current_speed + SPEED_INCREMENT)
            elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                current_speed = max(MIN_SPEED, current_speed - SPEED_INCREMENT)
            elif event.key == pg.K_ESCAPE:
                program_exit()
    update_display_caption()
    game_object.update_direction(game_object.direction)


def main():
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения
    змейки
    """
    global record_length
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(current_speed)
        handle_keys(snake)
        update_display_caption()
        snake.move()
        apple.cell_rendering(screen, apple.position)
        snake.draw(screen)

        if snake.positions[0] == apple.position:
            snake.length += 1
            if snake.length > record_length:
                record_length = snake.length
            apple = Apple(snake.positions)
            apple.randomize_position(snake.positions)

        pg.display.update()


if __name__ == '__main__':
    main()
