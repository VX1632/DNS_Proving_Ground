import socket
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

CHUNK_SIZE = 1024  # Size of each chunk to receive

def start_receiver(ip, port, output_file_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    logging.info(f"Listening on {ip}:{port}")

    try:
        with open(output_file_path, 'wb') as file:
            while True:
                try:
                    data, addr = sock.recvfrom(CHUNK_SIZE)
                    logging.debug(f"Received chunk from {addr}: {data[:10]}... ({len(data)} bytes)")
                    
                    # Write the chunk to the file
                    file.write(data)
                    
                    # Send acknowledgment
                    ack_message = b'ACK'
                    sock.sendto(ack_message, addr)
                    logging.info(f"Acknowledgment sent to {addr}")
                except Exception as e:
                    logging.error(f"Error handling chunk from {addr}: {e}")
                    break
        logging.info("File received and reconstructed successfully")
    except Exception as e:
        logging.error(f"Error writing file: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    receiver_ip = "172.16.223.86"
    receiver_port = 53
    output_file_path = "/app/downloads/received_test_image.jpg"
    start_receiver(receiver_ip, receiver_port, output_file_path)
