import pygame
import sys
import socket
from button import Button
from server import HOST, PORT
from GAMECODE import GAMECODE

pygame.init()
SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")
BG = pygame.image.load("img/bggame.jpg")

def get_font(size):
    return pygame.font.Font("img/Atop-R99O3.ttf", size)

name_input = []  # Khởi tạo name_input như một list
ready_count = 0

def start_game():
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Stress Fight")
    bg_image = pygame.image.load("img/bggame.jpg")
    screen.blit(bg_image, (0, 0))

def connect_to_server(player_name):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(f"name:{player_name}".encode())
        # print("Connected to the server as Player", player_name)
        return client_socket  # Trả về socket nếu kết nối thành công
    except Exception as e:
        print("Error:", e)
        return None  # Trả về None nếu có lỗi kết nối

def check_ready_count():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'check_ready_count')
            data = s.recv(1024).decode()
            return data
    except Exception as e:
        print("Error checking ready count:", e)
        return "0:"

def play():
    global name_input, name_entered
    name_entered = False  # Khai báo biến cờ

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        bg = pygame.image.load("img/play.jpg")
        SCREEN.blit(bg, (0, 0))

        PLAY_TEXT = get_font(20).render("Enter Your Name: " + ''.join(name_input), True, (255, 255, 255))
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 540))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        OPTIONS_PLAY = Button(pos=(1080, 800),
                              text_input="CONTINUE", font=get_font(40), base_color=(255, 255, 255), hovering_color=(0, 255, 0))
        PLAY_BACK = Button(pos=(800, 800),
                           text_input="BACK", font=get_font(40), base_color=(255, 255, 255), hovering_color=(0, 255, 0))
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        OPTIONS_PLAY.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        OPTIONS_PLAY.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif OPTIONS_PLAY.checkForInput(PLAY_MOUSE_POS):
                    player_name = ''.join(name_input)
                    if connect_to_server(player_name):  # Kiểm tra kết nối trước khi gọi wait_enemy()
                        name_entered = True
                        print("Name entered, connecting to server...")
                        wait_enemy()
                        return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Player name:", ''.join(name_input))
                    connect_to_server("ready")
                else:
                    name_input.append(event.unicode)

        pygame.display.update()
        


def wait_enemy():
    global ready_count
    waiting_text_displayed = True

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        bg = pygame.image.load("img/waiting.jpg")
        SCREEN.blit(bg, (0, 0))

        if waiting_text_displayed:
            wait_text = get_font(40).render("Waiting for other player...", True, (42, 231, 34))
            wait_rect = wait_text.get_rect(center=(960, 400))
            SCREEN.blit(wait_text, wait_rect)

        # Get the ready count and player names from the server
        data = check_ready_count()
        if ':' in data:
            count_str, player_data = data.split(':')
            if count_str.isdigit():
                ready_count = int(count_str)

                # Display player names
                player_names = player_data.split(',')
                for i, player_name in enumerate(player_names):
                    player_text = get_font(30).render(f"Player {i + 1}: {player_name}", True, (255, 255, 255))
                    player_rect = player_text.get_rect(center=(960, 500 + i * 50))
                    SCREEN.blit(player_text, player_rect)

                # If two players are ready, display the start button
                if ready_count == 2:
                    if waiting_text_displayed:
                        waiting_text_displayed = False  # Đã hiển thị thông báo chờ, không cần hiển thị nữa
                    wait_text = get_font(40).render("READY GAME...", True, (42, 231, 34))
                    wait_rect = wait_text.get_rect(center=(960, 400))
                    SCREEN.blit(wait_text, wait_rect)
                    START_BUTTON = Button(pos=(960, 650),
                                          text_input="START", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
                    START_BUTTON.changeColor(PLAY_MOUSE_POS)
                    START_BUTTON.update(SCREEN)

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if START_BUTTON.checkForInput(PLAY_MOUSE_POS):
                                GAMECODE.run_game()  # Đảm bảo rằng điều này gọi hàm bắt đầu trò chơi của bạn một cách chính xác
                                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()



def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((255, 255, 255))

        OPTIONS_TEXT = get_font(60).render("This is the OPTIONS screen.", True, (0, 0, 0))
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(960, 540))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(pos=(960, 800),
                              text_input="BACK", font=get_font(75), base_color=(0, 0, 0), hovering_color=(0, 255, 0))

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, (182, 143, 64))
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 200))

        PLAY_BUTTON = Button(pos=(960, 400),
                             text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        OPTIONS_BUTTON = Button(pos=(960, 600),
                                text_input="OPTIONS", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        QUIT_BUTTON = Button(pos=(960, 800),
                             text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
