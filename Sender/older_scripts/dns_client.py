import socket
import struct
import logging
import sys

# Logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mapping from hostname to IP for A and AAAA records
hostname_to_ip = {
    'dig.towson.edu': ('172.16.223.86', '2001:0db8:85a3:0000:0000:8a2e:0370:7334')  # Example IPv6 address
}

# Reverse mapping from IP to hostname for PTR records
ip_to_hostname = {
    '172.16.223.86': 'dig.towson.edu.',
    '2001:0db8:85a3:0000:0000:8a2e:0370:7334': 'dig.towson.edu.'
}

def parse_dns_query(data):
    """
    Parse the DNS query to extract the domain name and the query type.
    """
    position = 12
    domain = ''
    length = data[position]
    while length != 0:
        position += 1
        domain += data[position:position + length].decode('utf-8') + '.'
        position += length
        length = data[position]
    qtype = struct.unpack('!H', data[position+1:position+3])[0]
    query_type = 'PTR' if qtype == 12 else 'A' if qtype == 1 else 'AAAA' if qtype == 28 else 'UNKNOWN'
    return domain[:-1], query_type

def build_response(query_data, domain, query_type):
    """
    Route the response building based on the query type.
    """
    if query_type == 'A':
        return build_a_record_response(query_data, domain)
    elif query_type == 'PTR':
        return build_ptr_record_response(query_data, domain)
    elif query_type == 'AAAA':
        return build_aaaa_record_response(query_data, domain)

def build_a_record_response(query_data, domain):
    """
    Build an A record response for the given domain.
    """
    ip_address = hostname_to_ip.get(domain, ('10.20.1.6', None))[0]  # Default IPv4 if not found
    
    # Standard DNS response components
    transaction_id = query_data[:2]
    flags = b'\x81\x80'
    questions = query_data[4:6]
    answers_rrs = b'\x00\x01'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    question = query_data[12:query_data.find(b'\x00', 12) + 5]
    answer = b'\xc0\x0c' + b'\x00\x01' + b'\x00\x01' + struct.pack('!I', 60) + struct.pack('!H', 4) + socket.inet_aton(ip_address)

    return transaction_id + flags + questions + answers_rrs + authority_rrs + additional_rrs + question + answer

def build_aaaa_record_response(query_data, domain):
    """
    Build an AAAA record response for the given domain.
    """
    ip_address = hostname_to_ip.get(domain, (None, '::1'))[1]  # Default IPv6 if not found
    
    transaction_id = query_data[:2]
    flags = b'\x81\x80'
    questions = query_data[4:6]
    answers_rrs = b'\x00\x01'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    question = query_data[12:query_data.find(b'\x00', 12) + 5]
    answer = b'\xc0\x0c' + b'\x00\x1c' + b'\x00\x01' + struct.pack('!I', 60) + struct.pack('!H', 16) + socket.inet_pton(socket.AF_INET6, ip_address)

    return transaction_id + flags + questions + answers_rrs + authority_rrs + additional_rrs + question + answer

def run_server(host='0.0.0.0', port=53):
    """
    Start and run the DNS server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        logging.info(f"DNS Server started on {host}:{port}")
        while True:
            try:
                data, addr = server_socket.recvfrom(512)
                domain, query_type = parse_dns_query(data)
                logging.info(f"Received {query_type} query for {domain} from {addr}")

                response = build_response(data, domain, query_type)
                server_socket.sendto(response, addr)
                logging.info(f"Sent {query_type} response for {domain} to {addr}")

            except Exception as e:
                logging.error(f"Error: {e}")

if __name__ == "__main__":
    try:
        run_server()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
