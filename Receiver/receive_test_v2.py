import socket
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def start_receiver(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    logging.info(f"Listening on {ip}:{port}")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            logging.debug(f"Received raw data from {addr}: {data}")
            encoded_message = data.decode()
            logging.debug(f"Encoded message: {encoded_message}")
            message = base64.b64decode(encoded_message).decode()
            logging.info(f"Decoded message from {addr}: {message}")
            
            # Send an encoded response
            response_message = f"Received your message: {message}"
            encoded_response = base64.b64encode(response_message.encode()).decode()
            logging.debug(f"Encoded response: {encoded_response}")
            sock.sendto(encoded_response.encode(), addr)
            logging.info(f"Response sent to {addr}")
        except Exception as e:
            logging.error(f"Error handling message from {addr}: {e}")

if __name__ == "__main__":
    receiver_ip = "172.16.223.86"
    receiver_port = 53
    start_receiver(receiver_ip, receiver_port)
