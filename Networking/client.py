import pygame
import socket
import json
import threading
from Graphics.ui import UI

SERVER_IP = 'localhost'
SERVER_PORT = 5555

class BombermanClient:
    def __init__(self):
        pygame.init()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui = UI()
        self.player_id = None
        self.game_state = {}
        self.running = True
        self.connected = False

    def connect_to_server(self):
        try:
            self.sock.connect((SERVER_IP, SERVER_PORT))
            self.connected = True
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
            threading.Thread(target=self.listen_to_server, daemon=True).start()
        except Exception as e:
            print(f"Connection failed: {e}")
            self.running = False

    def listen_to_server(self):
        while self.running and self.connected:
            try:
                data = self.sock.recv(4096)
                if not data:
                    print("Disconnected from server")
                    self.connected = False
                    break

                message = json.loads(data.decode('utf-8'))

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
                self.connected = False

        self.running = False

    def send_input(self, action):
        if self.player_id is None or not self.connected:
            return

        try:
            msg = {
                'type': 'input',
                'action': action
            }
            self.sock.send(json.dumps(msg).encode('utf-8'))
        except Exception as e:
            print(f"Failed to send input: {e}")

    def close(self):
        self.running = False
        if self.connected:
            try:
                self.sock.close()
            except:
                pass
        pygame.quit()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting game.")
                    self.close()
                    return

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
                self.ui.render_game(self.game_state)

            clock.tick(60)

def main():
    client = BombermanClient()
    client.connect_to_server()
    if client.running:
        client.run()

if __name__ == "__main__":
    main()
