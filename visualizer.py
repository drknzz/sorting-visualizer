import pygame
import random
import math

pygame.init()

class DrawInfo:
    PADDING_LEFT = PADDING_RIGHT = 50
    PADDING_TOP = 150
    PADDING_TOP_TEXT = 5

    FONT = pygame.font.SysFont('georgia', 30)
    FONT_LARGE = pygame.font.SysFont('georgia', 40)

    class Color:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        BONE = (255, 255, 240)
        GREY_ONE = (125, 125, 125)
        GREY_TWO = (175, 175, 175)
        GREY_THREE = (225, 225, 225)

    def __init__(self, width=800, height=600, lst=None):
        self.color = self.Color()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")

        self.start_x = self.PADDING_LEFT
        self.start_y = self.PADDING_TOP

        if not lst:
            lst = create_random_list()
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst

        self.min_val = min(lst)
        self.max_val = max(lst)

        self.unit_width = round(self.width - self.PADDING_LEFT - self.PADDING_RIGHT) / len(lst)
        self.unit_height = math.floor((self.height - self.PADDING_TOP) / (self.max_val - self.min_val))


class Sort:
    def get_sort_alg(self):
        '''generator function for changing sorting algorithms'''
        
        algs = (
            ("Bubble Sort", self.bubble_sort),
            ("Insertion Sort", self.insertion_sort),
            ("Selection Sort", self.selection_sort),
            ("Merge Sort", self.merge_sort),
            ("Quick Sort", self.quick_sort),
            ("Bogo Sort", self.bogo_sort),
            ("Heap Sort", self.heap_sort),
        )
        i = 0
        while True:
            yield algs[i]
            i = (i + 1) % len(algs)

    def bubble_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        for i in range(len(lst) - 1):
            for j in range(len(lst) - 1 - i):
                if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    draw_list(draw_info, {j: draw_info.color.GREEN, j+1: draw_info.color.RED}, True)
                    yield True
        
        return lst

    def insertion_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        for i in range(1, len(lst)):
            j = i - 1
            while j >= 0 and ((lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending)):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.color.GREEN, j+1: draw_info.color.RED}, True)
                yield True
                j -= 1
        
        return lst

    def selection_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        for i in range(len(lst) - 1):
            m = lst[i]
            m_idx = i
            for j in range(i + 1, len(lst)):
                if (lst[j] < m and ascending) or (lst[j] > m and not ascending):
                    m = lst[j]
                    m_idx = j
            if m_idx != i:
                lst[i], lst[m_idx] = lst[m_idx], lst[i]
                draw_list(draw_info, {i: draw_info.color.GREEN, m_idx: draw_info.color.RED}, True)
                yield True

        return lst

    def merge_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        def merge_s(lst, start, end, ascending=True):
            if start >= end:
                return
            
            mid = (start + end) // 2
            yield from merge_s(lst, start, mid, ascending)
            yield from merge_s(lst, mid + 1, end, ascending)

            i = start
            j = mid + 1

            while i <= mid and j <= end:
                if (lst[i] <= lst[j] and ascending) or (lst[i] >= lst[j] and not ascending):
                    i += 1
                else:
                    tmp = lst[j]
                    idx = j

                    while idx > i:
                        lst[idx] = lst[idx - 1]
                        idx -= 1
                    
                    lst[i] = tmp

                    color_positions = {i: draw_info.color.GREEN, j: draw_info.color.RED}

                    i += 1
                    j += 1
                    mid += 1

                    draw_list(draw_info, color_positions, True)
                    yield True

        yield from merge_s(lst, 0, len(lst) - 1, ascending)

        return lst

    def quick_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        def quick_s(lst, start, end, ascending=True):
            if start >= end:
                return
            
            p_idx = (start + end) // 2
            p = lst[p_idx]

            lst[p_idx], lst[end] = lst[end], lst[p_idx]
            draw_list(draw_info, {p_idx: draw_info.color.GREEN, end: draw_info.color.RED}, True)
            yield True

            j = start
            for i in range(start, end):
                if (lst[i] < p and ascending) or (lst[i] > p and not ascending):
                    lst[j], lst[i] = lst[i], lst[j]
                    color_positions = {i: draw_info.color.GREEN, j: draw_info.color.RED}
                    j += 1
                    draw_list(draw_info, color_positions, True)
                    yield True
            
            lst[j], lst[end] = lst[end], lst[j]
            draw_list(draw_info, {j: draw_info.color.GREEN, end: draw_info.color.RED}, True)
            yield True

            yield from quick_s(lst, start, j - 1, ascending)
            yield from quick_s(lst, j + 1, end, ascending)

        yield from quick_s(lst, 0, len(lst) - 1, ascending)

        return lst

    def bogo_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        while not all(lst[i] <= lst[i+1] if ascending else lst[i] >= lst[i+1] for i in range(len(lst) - 1)):
            random.shuffle(lst)
            draw_list(draw_info, {}, True)
            yield True
        
        return lst

    def heap_sort(self, draw_info, ascending=True):
        lst = draw_info.lst

        def build_heap(lst, ascending=True):
            # ascending -> max heap / descending -> min heap
            for i in range(1, len(lst)):
                j = i
                while j > 0 and ((lst[(j-1)//2] < lst[j] and ascending) or (lst[(j-1)//2] > lst[j] and not ascending)):
                    lst[j], lst[(j-1)//2] = lst[(j-1)//2], lst[j]
                    draw_list(draw_info, {j: draw_info.color.GREEN, (j-1)//2: draw_info.color.RED}, True)
                    yield True
                    j = (j-1)//2

        yield from build_heap(lst, ascending)
        
        for i in range(len(lst) - 1):
            lst[0], lst[len(lst)-1-i] = lst[len(lst)-1-i], lst[0]
            draw_list(draw_info, {0: draw_info.color.GREEN, len(lst)-1-i: draw_info.color.RED}, True)
            yield True

            j = 0
            while j*2+1 < len(lst)-1-i:
                idx = j*2 + 1
                if j*2+2 < len(lst)-1-i:
                    if (lst[j*2+1] < lst[j*2+2] and ascending) or (lst[j*2+1] > lst[j*2+2] and not ascending):
                        idx = j*2 + 2

                if not ((lst[j] < lst[idx] and ascending) or (lst[j] > lst[idx] and not ascending)):
                    break
                
                lst[j], lst[idx] = lst[idx], lst[j]
                draw_list(draw_info, {j: draw_info.color.GREEN, idx: draw_info.color.RED}, True)
                yield True
                j = idx

        return lst


def create_random_list(length=50, min_value=1, max_value=100):
    return [random.randint(min_value, max_value) for _ in range(length)]


def draw(draw_info, sort_alg_name, ascending=True):
    '''draws everything on screen'''

    draw_info.screen.fill(draw_info.color.BONE)

    draw_text(draw_info, sort_alg_name, ascending)
    draw_list(draw_info)

    pygame.display.update()


def draw_text(draw_info, sort_alg_name, ascending=True):
    '''draws all the text on screen'''

    top_alg = draw_info.PADDING_TOP_TEXT
    alg_text = f"{sort_alg_name} - {'Ascending' if ascending else 'Descending'}"
    alg_text_obj = draw_info.FONT_LARGE.render(alg_text, 1, draw_info.color.BLUE)
    draw_info.screen.blit(alg_text_obj, (draw_info.width / 2 - alg_text_obj.get_width() / 2, top_alg))

    top_controls = top_alg + draw_info.FONT_LARGE.size(sort_alg_name)[1]
    controls_text = "SPACE - start / stop   |   R - restart"
    controls_text_obj = draw_info.FONT.render(controls_text, 1, draw_info.color.BLACK)
    draw_info.screen.blit(controls_text_obj, (draw_info.width / 2 - controls_text_obj.get_width() / 2, top_controls))

    top_controls_2 = top_controls + draw_info.FONT.size(controls_text)[1]
    controls_tex_2 = "A - change algorithm   |   S - change order"
    controls_text_2_obj = draw_info.FONT.render(controls_tex_2, 1, draw_info.color.BLACK)
    draw_info.screen.blit(controls_text_2_obj, (draw_info.width / 2 - controls_text_2_obj.get_width() / 2, top_controls_2))


def draw_list(draw_info, color_positions={}, clear_bg=False):
    '''draws list part of the screen'''

    draw_x = draw_info.start_x
    item_colors = (draw_info.color.GREY_ONE, draw_info.color.GREY_TWO, draw_info.color.GREY_THREE)

    if clear_bg:
        clear_rect = pygame.Rect(0, draw_info.start_y, draw_info.width, draw_info.height)
        pygame.draw.rect(draw_info.screen, draw_info.color.BONE, clear_rect)

    for idx, x in enumerate(draw_info.lst):
        rect = pygame.Rect(draw_x, draw_info.height - x * draw_info.unit_height, draw_info.unit_width, draw_info.unit_height * x)
        
        color = item_colors[idx % 3]
        if idx in color_positions:
            color = color_positions[idx]
        
        pygame.draw.rect(draw_info.screen, color, rect)
        draw_x += draw_info.unit_width
    
    if clear_bg:
        pygame.display.update()


def main():
    draw_info = DrawInfo()
    sort = Sort()

    end = sorting = False
    ascending = True

    clock = pygame.time.Clock()

    # generator for sorting algorithms
    choose_sort_alg_generator = sort.get_sort_alg()
    sort_alg_name, sort_alg = next(choose_sort_alg_generator)

    # generator for a single step in a sorting algorithm
    sort_step_generator = None

    while not end:
        # ticks per second
        clock.tick(60)

        if sorting:
            # try to do next step in sorting
            try:
                next(sort_step_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sort_alg_name, ascending)

        # detect events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type != pygame.KEYDOWN:
                continue

            # restart
            if event.key == pygame.K_r:
                draw_info.set_list(create_random_list())
                sorting = False
            # start / stop
            elif event.key == pygame.K_SPACE:
                sorting = not sorting
                sort_step_generator = sort_alg(draw_info, ascending)
            # change algorithm
            elif event.key == pygame.K_a and not sorting:
                sort_alg_name, sort_alg = next(choose_sort_alg_generator)
            # change order
            elif event.key == pygame.K_s and not sorting:
                ascending = not ascending
            # quit
            elif event.key == pygame.K_ESCAPE:
                end = True

    pygame.quit()

if __name__ == '__main__':
    main()