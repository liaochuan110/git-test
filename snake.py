import curses
import random

# Key mapping
KEY_UP = curses.KEY_UP
KEY_DOWN = curses.KEY_DOWN
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT

# Game settings
HEIGHT = 20
WIDTH = 60


def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Create game window
    win = curses.newwin(HEIGHT, WIDTH, 0, 0)
    win.keypad(1)
    win.border(0)

    # Initial snake and food positions
    snake = [(HEIGHT // 2, WIDTH // 4 + i) for i in range(3, 0, -1)]
    direction = KEY_RIGHT
    food = (random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2))
    win.addch(food[0], food[1], '*')

    score = 0

    while True:
        win.border(0)
        win.addstr(0, 2, f" Score: {score} ")

        next_key = win.getch()
        if next_key in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
            # Prevent the snake from reversing into itself
            if (direction == KEY_UP and next_key != KEY_DOWN) or \
               (direction == KEY_DOWN and next_key != KEY_UP) or \
               (direction == KEY_LEFT and next_key != KEY_RIGHT) or \
               (direction == KEY_RIGHT and next_key != KEY_LEFT):
                direction = next_key

        head_y, head_x = snake[0]
        if direction == KEY_UP:
            head_y -= 1
        elif direction == KEY_DOWN:
            head_y += 1
        elif direction == KEY_LEFT:
            head_x -= 1
        elif direction == KEY_RIGHT:
            head_x += 1

        # Check collisions
        if head_y in (0, HEIGHT - 1) or head_x in (0, WIDTH - 1) or (head_y, head_x) in snake:
            break

        snake.insert(0, (head_y, head_x))

        if (head_y, head_x) == food:
            score += 1
            food = None
            while food is None:
                nf = (random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2))
                if nf not in snake:
                    food = nf
            win.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        win.addch(head_y, head_x, '#')

    msg = f"Game Over! Your score: {score}".center(WIDTH)
    win.addstr(HEIGHT // 2, 0, msg)
    win.nodelay(0)
    win.getch()


if __name__ == "__main__":
    curses.wrapper(main)
