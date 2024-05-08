import socket

def send_message(message, server_ip, server_port=53):
    """Send plain text message as a DNS-like query."""
    dns_query = f"{message}.towson.edu"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(dns_query.encode(), (server_ip, server_port))
        client_socket.settimeout(2)
        try:
            response, _ = client_socket.recvfrom(1024)
            print(f"Response from server: {response.decode()}")
        except socket.timeout:
            print("No response received; server may be down or check network.")

# Example usage:
send_message("Hello, DNS World!", "172.16.223.86")
