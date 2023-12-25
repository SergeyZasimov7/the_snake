from random import choice, randint
import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Тут опишите все классы игры
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        """Конструктор класса, который инициализирует базовые атрибуты объекта,

        такие как его позиция и цвет.

        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Абстрактный метод, который предназначен для переопределения в

        дочерних классах

        """
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject,

    описывающий змейку и её поведение.

    """

    def __init__(self, snake_positions=[list[tuple[int, int]]]):
        """Конструктор класса, который задает цвет яблока и вызывает метод

        randomize_position, чтобы установить начальную позицию яблока.

        """
        super().__init__()
        self.body_color = (255, 0, 0)
        self.snake_positions = snake_positions
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока на игровом поле —

        задаёт атрибуту position новое значение. Координаты выбираются так,

        чтобы яблоко оказалось в пределах игрового поля.

        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,

    описывающий змейку и её поведение.

    """

    def __init__(self):
        """Конструктор класса, инициализирующий начальное состояние

        змейки.

        """
        super().__init__()
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.positions = [self.position]
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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
        if self.direction in {RIGHT, LEFT}:
            if x >= SCREEN_WIDTH:
                x = 0
            elif x < 0:
                x = SCREEN_WIDTH - GRID_SIZE
        elif self.direction in {UP, DOWN}:
            if y >= SCREEN_HEIGHT:
                y = 0
            elif y < 0:
                y = SCREEN_HEIGHT - GRID_SIZE
        if (x, y) in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (x, y))
            self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
               (self.last[0], self.last[1]),
               (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

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


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения

    змейки

    """
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(20)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw(screen)
        snake.draw(screen)

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple = Apple(snake.positions)

        pygame.display.update()


if __name__ == '__main__':
    main()
