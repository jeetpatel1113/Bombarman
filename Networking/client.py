import socket
import threading

SERVER_IP = '207.6.193.56'  # Change to your server's IP
SERVER_PORT = 5555

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"Server: {msg}")
            else:
                print("Disconnected from server")
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

    while True:
        # Receive message from server
        msg = input("You: ")
        if msg.lower() == 'quit':
            break
        try:
            client_socket.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"Error sending: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()