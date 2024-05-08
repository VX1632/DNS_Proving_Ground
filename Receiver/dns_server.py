import socket
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_server(host='0.0.0.0', port=53):
    """Run the DNS server."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        logging.info(f"DNS Server started on {host}:{port}")
        while True:
            try:
                data, addr = server_socket.recvfrom(512)
                message = data.decode().split('.')[0]  # Assume simple text query
                logging.info(f"Received message: {message} from {addr}")
                # Respond back with a simple acknowledgement
                response = f"ACK: {message}".encode()
                server_socket.sendto(response, addr)
            except Exception as e:
                logging.error(f"Error: {e}")

if __name__ == "__main__":
    run_server()
