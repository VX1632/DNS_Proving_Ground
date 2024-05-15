# Proving Ground

## Description

Proving Ground is a project designed to demonstrate file transfer using DNS queries within a Dockerized environment. This project simulates a simple DNS server and client to encode and send files as DNS queries, showcasing the potential for DNS-based data exfiltration techniques.

## Installation

To set up this project locally, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/proving_ground.git
   cd proving_ground
2. Build Docker Containers
   Navigate to the project directory and run:
   docker-compose up --build

## Directory Structure

dns-file-transfer/
├── app/
│   ├── downloads/           # Directory to store reconstructed files
│   ├── static/              # Directory for static files (if needed)
│   ├── templates/           # Directory for HTML templates (if needed)
│   └── __init__.py          # Initialize the Flask app
├── run.py                   # Main script to run the DNS server and Flask app
├── requirements.txt         # Required Python packages
├── README.md                # This README file
└── .gitignore               # Git ignore file

## Usage

To start the project, simply run:

bash

docker-compose up

This command starts both the DNS sender and receiver services. The sender splits a specified file into chunks, encodes each chunk in Base64, and sends it over a simulated DNS query. The receiver collects these queries, decodes them, and reconstructs the original file.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1.    Fork the Project
2.    Create your Feature Branch (git checkout -b feature/NewFeature)
3.    Commit your Changes (git commit -m 'Add some NewFeature')
4.    Push to the Branch (git push origin feature/NewFeature)
5.    Open a Pull Request

## License

Distributed under the MIT License. See LICENSE for more information.

