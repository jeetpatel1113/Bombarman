import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

def handle_client(client_socket, client_address):
    print(f"Client {client_address} connected.")
    
    try:
        client_socket.send("Connected".encode('utf-8'))
    except:
        print(f"Failed {client_address}")
        client_socket.close()
        return
    
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                print(f"Client {client_address} disconnected (empty message)")
                break
            
            print(f"Client {client_address}: {msg}")
            
            response = f"Server received: {msg}"
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"Error {client_address}: {e}")
            break
    
    print(f"Client {client_address} disconnected.")
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(4)
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
