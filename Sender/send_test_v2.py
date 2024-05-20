import socket
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message(message, server_ip, server_port):
    encoded_message = base64.b64encode(message.encode()).decode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(encoded_message.encode(), (server_ip, server_port))
        logging.info(f"Encoded message sent: {encoded_message}")
        data, _ = sock.recvfrom(1024)
        logging.debug(f"Received raw response: {data}")
        decoded_response = base64.b64decode(data).decode()
        logging.info(f"Received response: {decoded_response}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    server_ip = "172.16.223.86"
    server_port = 53
    message = "Hello, DNS Receiver!"
    send_message(message, server_ip, server_port)
