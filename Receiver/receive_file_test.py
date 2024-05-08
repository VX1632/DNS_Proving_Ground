import socket
import base64
import logging
import os

# Configure logging to display information, including the timestamp, log level, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_server(host='0.0.0.0', port=53):
    """
    Starts a UDP server that listens for incoming DNS-like queries and processes them
    to reconstruct a transmitted file.
    """
    # Create a UDP socket to listen on the specified port and IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Bind the socket to the provided host and port
        server_socket.bind((host, port))
        logging.info(f"DNS Server started on {host}:{port}")

        # Initialize a bytearray to accumulate the incoming file data
        file_content = bytearray()

        # Continuously listen for incoming data
        while True:
            try:
                # Receive up to 1024 bytes from a client, along with the address of the sender
                data, addr = server_socket.recvfrom(1024)
                if data:
                    # Decode the received data, assuming it's formatted like a DNS query
                    # You might want to ensure this strip is accurate to your DNS-like queries format
                    message = data.decode().rstrip('.example.com')  # This needs to match your sending format

                    # Attempt to decode the base64 data back into binary
                    try:
                        chunk = base64.urlsafe_b64decode(message)
                        # Extend the file_content bytearray with the decoded binary data
                        file_content.extend(chunk)
                        # Log the reception of data
                        logging.info(f"Received data from {addr}")
                    except base64.binascii.Error as e:
                        # Log decoding errors without stopping the server
                        logging.error(f"Base64 decoding error: {e}")
                        continue
                else:
                    # If no data is received, consider the transmission complete and prepare to break the loop
                    logging.info("No more data received. Preparing to close the server.")
                    break
            except Exception as e:
                # Log unexpected errors and break the loop
                logging.error(f"Unexpected error: {e}")
                break

        # Write the accumulated binary data into a file
        with open('received_image.png', 'wb') as file:
            file.write(file_content)
        # Confirm file writing
        logging.info("File has been reconstructed and saved.")

        # Check if the file exists and log the confirmation
        if os.path.exists('received_image.png'):
            logging.info("Confirmation: File 'received_image.png' exists and has been saved successfully.")

if __name__ == "__main__":
    run_server()
