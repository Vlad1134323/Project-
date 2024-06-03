import pygame
import sys
import webbrowser

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Установка размеров окна
size = (360, 640)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Меню")

# Шрифты
font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 24)

# Тексты кнопок
buttons = ["Тварини", "Донат", "Вихід"]

# Загрузка анкет (фото и тексты)
profiles = [
    {"image": "image1.png", "text": "Маунглі.  Дзвоніть за номером +380блаблаблабла"},
    {"image": "image2.png", "text": "Адольф. Дзвоніть за номером +380блаблаблабла"},
    {"image": "image3.png", "text": "Акакий.  Дзвоніть за номером +380блаблаблабла"},
    {"image": "image4.png", "text": "Мурзик.   Дзвоніть за номером +380блаблаблабла"},
    {"image": "image5.png", "text": "Грусля.  Дзвоніть за номером +380блаблаблабла"},
    {"image": "image6.png", "text": "Шрек.   Дзвоніть за номером +380блаблаблабла"}
    ]
for profile in profiles:
    profile["image"] = pygame.image.load(profile["image"])

# Загрузка изображения стрелки для кнопки "Назад"
back_arrow = pygame.image.load("back_arrow.png")
back_arrow = pygame.transform.scale(back_arrow, (40, 40))  # Масштабирование изображения

# Загрузка фонового изображения
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, size)  # Масштабирование под размер экрана

current_profile = 0

# Функция отрисовки кнопок
def draw_buttons():
    screen.blit(background, (0, 0))  # Отрисовка фонового изображения
    button_height = 70
    button_width = 200
    for i, text in enumerate(buttons):
        rect = pygame.Rect((size[0] - button_width) // 2, 150 + i * (button_height + 20), button_width, button_height)
        pygame.draw.rect(screen, GREY, rect)
        label = font.render(text, True, BLACK)
        screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + (rect.height - label.get_height()) // 2))
    pygame.display.flip()

# Функция отрисовки экрана с анкетами
def draw_profile():
    screen.blit(background, (0, 0))  # Отрисовка фонового изображения
    profile = profiles[current_profile]
    img = pygame.transform.scale(profile["image"], (size[0], size[0]))  # Пропорционально уменьшаем изображение под экран
    screen.blit(img, (0, 0))

    # Отрисовка кнопки "Назад"
    back_button_rect = pygame.Rect(10, 10, 40, 40)
    pygame.draw.rect(screen, WHITE, back_button_rect)
    screen.blit(back_arrow, (10, 10))

    # Разбиваем текст на строки
    text_lines = profile["text"].split('. ')
    y_offset = size[0] + 20
    for line in text_lines:
        text_surface = text_font.render(line, True, BLACK)
        screen.blit(text_surface, (10, y_offset))
        y_offset += text_surface.get_height() + 5
    
    pygame.display.flip()
    return back_button_rect

# Основной цикл программы
running = True
in_profiles_screen = False
start_swipe_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if in_profiles_screen:
                start_swipe_pos = mouse_pos
                back_button_rect = draw_profile()
                if back_button_rect.collidepoint(mouse_pos):
                    in_profiles_screen = False
            else:
                button_height = 70
                button_width = 200
                for i, text in enumerate(buttons):
                    rect = pygame.Rect((size[0] - button_width) // 2, 150 + i * (button_height + 20), button_width, button_height)
                    if rect.collidepoint(mouse_pos):
                        if text == "Тварини":
                            in_profiles_screen = True
                        elif text == "Донат":
                            webbrowser.open("https://gladpet.org/help/shelters")  # Замените URL на нужный
                        elif text == "Вихід":
                            running = False
        elif event.type == pygame.MOUSEBUTTONUP and in_profiles_screen:
            if start_swipe_pos:
                end_swipe_pos = event.pos
                if end_swipe_pos[0] < start_swipe_pos[0] - 50:  # Свайп влево
                    current_profile = (current_profile + 1) % len(profiles)
                elif end_swipe_pos[0] > start_swipe_pos[0] + 50:  # Свайп вправо
                    current_profile = (current_profile - 1) % len(profiles)
                start_swipe_pos = None

    if in_profiles_screen:
        back_button_rect = draw_profile()
    else:
        draw_buttons()

pygame.quit()
sys.exit()