import socket
import threading
import json
import time
from Graphics.game_logic import GameState

SERVER_IP = 'localhost'
SERVER_PORT = 5555

class BombermanServer:
    def __init__(self):
        #Network setup
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.clients_lock = threading.Lock()
        #Game setup
        self.game_state = GameState()
        self.player_count = 0
        self.game_running = False
        self.max_players = 4
    
    def broadcast_game_state(self):
        game_data = {
            'type': 'game_state',
            'state': self.game_state.to_render_state()
        }
        self.broadcast_to_all(game_data)

    def broadcast_to_all(self, message):
        with self.clients_lock:
            disconnected_clients = []

            for client_socket, client_address, player_id in self.clients:
                try:
                    if isinstance(message, dict):
                        data = json.dumps(message).encode('utf-8')
                    else:
                        data = str(message).encode('utf-8')
                    client_socket.send(data)
                except Exception as e:
                    print(f"Failed to send to {client_address}: {e}.")
                    disconnected_clients.append((client_socket, client_address, player_id))
            
            for client in disconnected_clients:
                if client in self.clients:
                    self.clients.remove(client)
                    self.disconnect_player(client[2])
                    print(f"Removed disconnected client {client[1]}.")
    
    def send_to_client(self, client_socket, message):
        try:
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            else:
                data = str(message).encode('utf-8')
            client_socket.send(data)
        except Exception as e:
            print(f"Failed to send to client: {e}.")
    
    def disconnect_player(self, player_id):
        if player_id in self.game_state.players:
            self.game_state.players[player_id]['alive'] = False
        self.player_count -= 1
        print(f"Player {player_id} disconnected.")

        if self.player_count == 0:
            self.game_running = False

    def handle_client(self, client_socket, client_address):
        player_id = None
        #Assign player ID
        with self.clients_lock:
            if self.player_count < self.max_players:
                self.player_count += 1
                player_id = self.player_count
                self.clients.append((client_socket, client_address, player_id))
                print(f"Player {player_id} connected from {client_address}.")
                self.game_state.add_player(player_id)
            else:
                try:
                    self.send_to_client(client_socket, {
                        'type': 'error',
                        'message': 'Server is full!'
                    })
                except:
                    pass
                client_socket.close()
                return
        #Send client their player ID
        try:
            self.send_to_client(client_socket, {
                'type': 'player_id',
                'player_id': player_id
            })
        except:
            print(f"Failed to send player_id to {client_address}.")
            self.clean_client(client_socket, client_address, player_id)
            return
        
        if self.player_count >= 2 and not self.game_running:
            self.game_running = True
            self.broadcast_to_all({
                'type': 'game_start',
                'message': 'Game starting!'
            })
        #Main client loop
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Player {player_id} disconnected.")
                    break
                try:
                    message = json.loads(data.decode('utf-8'))
                    self.process_player_message(player_id, message)
                except json.JSONDecodeError:
                    print(f"Invalid JSON from player {player_id}.")
                except Exception as e:
                    print(f"Error processing data from player {player_id}: {e}.")
            
            except Exception as e:
                print(f"Error with player {player_id}: {e}.")
                break
        
        self.clean_client(client_socket, client_address, player_id)

    def clean_client(self, client_socket, client_address, player_id):
        with self.clients_lock:
            client_tuple = (client_socket, client_address, player_id)
            if client_tuple in self.clients:
                self.clients.remove(client_tuple)
        
        if player_id:
            self.disconnect_player(player_id)
        print(f"Player {player_id} disconnected.")
        client_socket.close()

    def process_player_message(self, player_id, message):
        msg_type = message.get('type')
        
        if msg_type == 'input':
            action = message.get('action')
            if action and self.game_running:
               self.game_state.apply_input(player_id, action)
        
        elif msg_type == 'ping':
            with self.clients_lock:
                for client_socket, _, pid in self.clients:
                    if pid == player_id:
                        self.send_to_client(client_socket, {'type': 'pong'})
                        break
        
        elif msg_type == 'chat':
            chat_msg = message.get('message', '')
            self.broadcast_to_all({
                'type': 'chat',
                'player_id': player_id,
                'message': chat_msg
            })
            print(f"Player {player_id}: {chat_msg}")
    
    def game_loop(self):
        while True:
            time.sleep(1/60)

            if self.game_running and self.player_count > 0:
                self.game_state.update()
                self.broadcast_game_state()

                alive_players = [pid for pid, player in self.game_state.players.items()
                                 if player['alive']]
                
                if len(alive_players) <= 1 and len(self.game_state.players) > 1:
                    winner = alive_players[0] if alive_players else None
                    self.broadcast_to_all({
                        'type': 'game_over',
                        'winner': winner
                    })

                    time.sleep(3)
                    self.reset_game()
    
    def reset_game(self):
        self.game_state = GameState()
        with self.clients_lock:
            for _, _, player_id in self.clients:
                self.game_state.add_player(player_id)
                
        self.broadcast_to_all({
                'type': 'game_reset',
                'message': 'New game starting!'
            })

    def start_server(self):
        try:
            self.server_socket.bind((SERVER_IP, SERVER_PORT))
            self.server_socket.listen(self.max_players)
            print(f"Bomberman server listening on {SERVER_IP}:{SERVER_PORT}")
                
            game_thread = threading.Thread(target=self.game_loop, daemon=True)
            game_thread.start()
                
            while True:
                client_socket, client_address = self.server_socket.accept()
                    
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.shutdown_server()

    def shutdown_server(self):
        print("Shutting down server.")
        with self.clients_lock:
            for client_socket, client_address, player_id in self.clients:
                try:
                    client_socket.close()
                except:
                    pass
            try:
                self.server_socket.close()
            except:
                pass

def main():
    server = BombermanServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
        server.shutdown_server()

if __name__ == "__main__":
    main()
