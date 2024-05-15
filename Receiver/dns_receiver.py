import os
import socket
import logging
from flask import Flask, send_from_directory, abort
import hashlib
import base64

# Configure logging to display information, including the timestamp, log level, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def decode_base64(data):
    try:
        padding_needed = 4 - (len(data) % 4)
        if padding_needed:
            data += "=" * padding_needed
        return base64.urlsafe_b64decode(data)
    except Exception as e:
        logging.error(f"Error decoding base64 data: {e}")
        return None

app = Flask(__name__)

@app.route('/downloads/<filename>')
def download_file(filename):
    try:
        # Specify the path to the received file
        file_path = os.path.join('/app/downloads', filename)
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            abort(404)
        logging.info(f"Serving file from path: {file_path}")
        return send_from_directory(directory='/app/downloads', filename=filename)
    except Exception as e:
        logging.error(f"Error serving file {filename}: {e}")
        abort(500)

# Ensure that the directory exists or create it
save_path = os.path.join(app.root_path, 'downloads')
if not os.path.exists(save_path):
    os.makedirs(save_path)

def run_server(host='0.0.0.0', port=53):
    """
    Starts a UDP server that listens for incoming DNS-like queries and processes them
    to reconstruct a transmitted file.
    """
    received_packets = {}
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        logging.info(f"DNS Server started on {host}:{port}")

        expected_packets = 200
        checksum = None

        while True:
            try:
                data, addr = server_socket.recvfrom(1024)
                if data:
                    try:
                        packet_info, message, checksum = data.decode().split(":", 2)
                        packet_number = int(packet_info)
                        message = decode_base64(message.rstrip('.towson.edu'))
                        if message is not None:
                            received_packets[packet_number] = message
                            logging.info(f"Received packet {packet_number}: {data}")
                        else:
                            logging.error(f"Received invalid base64 message in packet {packet_number}")
                    except ValueError as ve:
                        logging.error(f"Error processing packet from {addr}: {ve}")
                    except Exception as e:
                        logging.error(f"Unexpected error while processing data from {addr}: {e}")

                    if len(received_packets) == expected_packets:
                        break
                else:
                    logging.info("No more data received. Preparing to close the server.")
                    break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break

        file_path = os.path.join(save_path, 'received_image.jpg')
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        try:
            with open(file_path, 'wb') as file:
                for i in sorted(received_packets.keys()):
                    file.write(received_packets[i])

            logging.info("File has been reconstructed and saved to: %s", file_path)
        except Exception as e:
            logging.error(f"Error writing to file {file_path}: {e}")

        if os.path.exists(file_path):
            logging.info("Confirmation: File 'received_image.jpg' exists and has been saved successfully.")

        received_checksum = generate_checksum(file_path)
        if received_checksum is not None:
            if received_checksum == checksum:
                logging.info(f"File integrity verified. Checksum: {received_checksum}")
            else:
                logging.error(f"File integrity check failed. Received checksum: {received_checksum}, Expected checksum: {checksum}")
        else:
            logging.error("Failed to generate checksum for the received file.")

        app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    run_server()
