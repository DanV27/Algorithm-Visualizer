import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('arial', 20)
    LARGE_FONT = pygame.font.SysFont('arial', 30, bold=True)  # Updated to Arial, bold

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    @staticmethod
    def generate_starting_list(n, min_val, max_val):
        return [random.randint(min_val, max_val) for _ in range(n)]


def draw(draw_info, algo_name, ascending, reset_highlight=False, sorting=False):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Determine the color for "R - Reset"
    reset_color = (255, 102, 102) if reset_highlight else draw_info.BLACK  # Light red if highlighted

    # Determine the color for "SPACE - Start Sorting"
    sorting_color = (144, 238, 144) if sorting else draw_info.BLACK  # Light green if sorting is active

    # Render the large font text with a grey border and black main text
    render_text_center(draw_info, f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 5, draw_info.LARGE_FONT, draw_info.BLACK)

    # Render "R - Reset" separately with its dynamic color
    render_text_center(draw_info, "R - Reset", 45, draw_info.FONT, reset_color)

    # Render "SPACE - Start Sorting" with its dynamic color
    render_text_center(draw_info, "SPACE - Start Sorting", 75, draw_info.FONT, sorting_color)

    # Determine the colors for "A - Ascending" and "D - Descending"
    ascending_color = (173, 216, 230) if ascending else draw_info.BLACK  # Light blue if ascending is selected
    descending_color = (173, 216, 230) if not ascending else draw_info.BLACK  # Light blue if descending is selected

    # Render sorting order options
    render_text_center(draw_info, f"A - Ascending", 105, draw_info.FONT, ascending_color)
    render_text_center(draw_info, f"D - Descending", 135, draw_info.FONT, descending_color)

    # Determine the colors for "I - Insertion Sort" and "B - Bubble Sort"
    insertion_color = (255, 182, 193) if algo_name == "Insertion Sort" else draw_info.BLACK  # Light pink if Insertion Sort is selected
    bubble_color = (255, 182, 193) if algo_name == "Bubble Sort" else draw_info.BLACK  # Light pink if Bubble Sort is selected

    # Render sorting options with dynamic colors
    render_text_center(draw_info, "I - Insertion Sort", 165, draw_info.FONT, insertion_color)
    render_text_center(draw_info, "B - Bubble Sort", 195, draw_info.FONT, bubble_color)

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i] 

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


# Add a delay in the sorting loop
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    if not lst:
        print("The list is empty. Please reset.")
        return

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                pygame.time.delay(50)  # Add a delay (in milliseconds)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    if not lst:
        print("The list is empty. Please reset.")
        return

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def render_text_center(draw_info, text, y, font, color, border_color=(128, 128, 128)):
    # Render the border by drawing the text offset in a larger range
    rendered_text = font.render(text, 1, border_color)
    offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]  # More offsets for a thicker border
    for dx, dy in offsets:
        draw_info.window.blit(rendered_text, (draw_info.width / 2 - rendered_text.get_width() / 2 + dx, y + dy))

    # Render the main text in the center
    rendered_text = font.render(text, 1, color)
    draw_info.window.blit(rendered_text, (draw_info.width / 2 - rendered_text.get_width() / 2, y))


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = DrawInformation.generate_starting_list(n, min_val, max_val)
    
    # Constants for window dimensions
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    # Use these constants in your code
    draw_info = DrawInformation(WINDOW_WIDTH, WINDOW_HEIGHT, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    # Map keys to sorting algorithms and names
    sorting_algorithms = {
        pygame.K_i: (insertion_sort, "Insertion Sort"),
        pygame.K_b: (bubble_sort, "Bubble Sort")
    }

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, sorting=sorting)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                # Highlight "R - Reset" in light red
                draw(draw_info, sorting_algo_name, ascending, reset_highlight=True)
                pygame.display.update()
                pygame.time.delay(1000)  # Wait for 1 second

                # Reset the list and redraw without the highlight
                lst = DrawInformation.generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                draw(draw_info, sorting_algo_name, ascending, reset_highlight=False)
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True  # Set ascending to True
            elif event.key == pygame.K_d and not sorting:
                ascending = False  # Set ascending to False
            elif event.key in sorting_algorithms and not sorting:
                sorting_algorithm, sorting_algo_name = sorting_algorithms[event.key]

        if not lst:
            print("The list is empty. Please reset.")
            continue

        if sorting_algorithm is None:
            print("No sorting algorithm selected.")
            continue

    pygame.quit()


if __name__ == "__main__":
    main()