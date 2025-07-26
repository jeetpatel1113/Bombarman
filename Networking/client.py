import socket

SERVER_IP = '127.0.0.1'  # Change to your server's IP
SERVER_PORT = 5555

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server.")
    except Exception as e:
        print(f"Connection error: {e}")
        return

    while True:
        # Receive message from server
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"Server: {msg}")
            else:
                break
        except:
            break

        # Send message to server
        msg = input("You: ")
        if msg.lower() == 'quit':
            break
        client_socket.send(msg.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()