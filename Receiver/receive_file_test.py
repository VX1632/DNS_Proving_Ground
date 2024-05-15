import os
import socket
import logging
from flask import Flask, send_file

# Configure logging to display information, including the timestamp, log level, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/download')
def download_file():
    # Specify the path to the received file
    file_path = 'downloads/received_image.jpg'  # Update this path according to your setup
    # Use Flask's send_file function to send the file to the client
    return send_file(file_path, as_attachment=True)

def run_server(host='0.0.0.0', port=53):
    """
    Starts a UDP server that listens for incoming DNS-like queries and processes them
    to reconstruct a transmitted file.
    """
    # Define a dictionary to store received packets
    received_packets = {}
    
    # Ensure that the directory exists or create it
    save_path = 'downloads'  # Update this with the desired directory path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Create a UDP socket to listen on the specified port and IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Bind the socket to the provided host and port
        server_socket.bind((host, port))
        logging.info(f"DNS Server started on {host}:{port}")

        expected_packets = 10  # Assuming 10 packets for demonstration, adjust according to your setup

        # Continuously listen for incoming data
        while True:
            try:
                # Receive up to 1024 bytes from a client, along with the address of the sender
                data, addr = server_socket.recvfrom(1024)
                if data:
                    # Decode the received data, assuming it's formatted like a DNS query
                    packet_info, message = data.decode().split(":", 1)
                    packet_number = int(packet_info)
                    # You might want to ensure this strip is accurate to your DNS-like queries format
                    message = message.rstrip('.towson.edu')  # This needs to match your sending format

                    # Store packets in received_packets dictionary...
                    received_packets[packet_number] = message
                    
                    if len(received_packets) == expected_packets:
                        break
                    
                else:
                    # If no data is received, consider the transmission complete and prepare to break the loop
                    logging.info("No more data received. Preparing to close the server.")
                    break
            except Exception as e:
                # Log unexpected errors and break the loop
                logging.error(f"Unexpected error: {e}")
                break

        # Reassemble file...
        with open(os.path.join(save_path, 'received_image.jpg'), 'wb') as file:
            for i in sorted(received_packets.keys()):
                file.write(received_packets[i].encode('utf-8'))
                
        # Confirm file writing
        logging.info("File has been reconstructed and saved to: %s", os.path.join(save_path, 'received_image.jpg'))

        # Check if the file exists and log the confirmation
        if os.path.exists(os.path.join(save_path, 'received_image.jpg')):
            logging.info("Confirmation: File 'received_image.jpg' exists and has been saved successfully.")

        # Run the Flask app after saving the file
        app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    run_server()
