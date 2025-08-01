import socket
import threading
import json
import pygame

# 207.6.193.56
# 192.168.1.107
SERVER_IP = '192.168.1.107'  # Change to your server's IP
SERVER_PORT = 5555

def get_player_action(keys):
    action = None
    if keys == pygame.K_UP or keys == pygame.K_w:
        action = {"type": "move", "direction": "UP"}
    elif keys == pygame.K_DOWN or keys == pygame.K_s:
        action = {"type": "move", "direction": "DOWN"}
    elif keys == pygame.K_LEFT or keys == pygame.K_a:
        action = {"type": "move", "direction": "LEFT"}
    elif keys == pygame.K_RIGHT or keys == pygame.K_d:
        action = {"type": "move", "direction": "RIGHT"}
    elif keys == pygame.K_SPACE:
        action = {"type": "place_bomb"}
    elif keys == pygame.K_r: # Example for a reset action
        action = {"type": "reset_game"}
    
    return action
def receive_messages(client_socket):
    while True:
        try:
            connection_establish = client_socket.recv(4096)
            if not connection_establish:
                print("Disconnected from server.")
                break
            try:
                msg = json.loads(connection_establish.decode('utf-8'))
                print(f"Server: {msg}") # Print the received dictionary
            except json.JSONDecodeError:
                print(f"Received invalid JSON from server: {connection_establish.decode('utf-8')}")
            
        except ConnectionResetError:
            print("Server forcibly closed the connection.")
            break
        except Exception as e:
            print(f"Error receiving: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server.")
    except Exception as e:
        print(f"Connection error: {e}")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    running = True
    while running:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.K_ESCAPE:
        #         running = False
        #     elif event.type == pygame.KEYDOWN:
                # message_to_send = get_player_action(key)
                send = input("Want to send?")
                if send == "y":
                    message_to_send = {"type": "input", "action": "UP"}
                    if message_to_send:
                        try:
                            client_socket.send(json.dumps(message_to_send).encode('utf-8'))
                        except Exception as e:
                            print(f"Error sending: {e}")
                            running = False
                            break
                else:
                    running = False
                    break

    client_socket.close()
    pygame.quit()

if __name__ == "__main__":
    main()