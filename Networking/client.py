import pygame
import socket
import json
import threading
import time
from Graphics.ui import UI

# Server Configuration
SERVER_IP = '192.168.1.64' # Server IP
SERVER_PORT = 5555 # Server Port

class BombermanClient:
    def __init__(self):
        pygame.init()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui = UI()
        self.player_id = None
        self.game_state = {}
        self.running = True

        # Input throttling
        self.last_input_time = 0
        self.input_delay = {
            "UP": 0.1,
            "DOWN": 0.1,
            "LEFT": 0.1,
            "RIGHT": 0.1,
            "BOMB": 0.2
        }
        self.last_action_time = {}

    def connect_to_server(self):
        try:
            self.sock.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
        except Exception as e:
            print(f"Connection failed: {e}")
            self.running = False
            return

        # Start a thread to listen to the server
        threading.Thread(target=self.listen_to_server, daemon=True).start()

    def listen_to_server(self):
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    print("Disconnected from server")
                    self.running = False
                    break

                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    message_str, buffer = buffer.split('\n', 1)
                    if message_str.strip() == '':
                        continue
                    message = json.loads(message_str)

                    if message['type'] == 'player_id':
                        self.player_id = message['player_id']
                        print(f"Assigned Player ID: {self.player_id}")

                    elif message['type'] == 'game_state':
                        self.game_state = message['state']

                    elif message['type'] == 'game_over':
                        print("Game Over!")
                        winner = message.get("winner")
                        if winner:
                            print(f"Player {winner} wins!")
                        else:
                            print("It's a draw!")

                    elif message['type'] == 'chat':
                        print(f"Player {message['player_id']}: {message['message']}")

            except Exception as e:
                print(f"Error receiving data: {e}")
                self.running = False

    def send_input(self, action):
        now = time.time()
        delay = self.input_delay.get(action)
        last_time = self.last_action_time.get(action, 0)

        if now - last_time < delay:
            return  # throttle input

        self.last_action_time[action] = now

        if self.player_id is None:
            return
        try:
            msg = {
                'type': 'input',
                'action': action
            }
            self.sock.send((json.dumps(msg) + '\n').encode('utf-8'))
        except Exception as e:
            print(f"Failed to send input: {e}")

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting game.")
                    self.sock.close()
                    pygame.quit()
                    return

            try:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.send_input("UP")
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.send_input("DOWN")
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.send_input("LEFT")
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.send_input("RIGHT")
                elif keys[pygame.K_SPACE]:
                    self.send_input("BOMB")

                if self.game_state:

                    if self.game_state["audio"]["play_bomb"]:
                        self.ui.play_sound("place_bomb")
                    if self.game_state["audio"]["play_explosion"]:
                        self.ui.play_sound("explosion")

                    self.ui.render_game(self.game_state)

            except pygame.error as e:
                print(f"Pygame rendering error: {e}")
                continue  # Skip this frame but stay running

            clock.tick(60)


def main():
    client = BombermanClient()
    client.connect_to_server()
    client.run()

if __name__ == "__main__":
    main()
