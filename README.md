# Health Check Monitor

## Project Overview
This project is a Python application designed to monitor the health of HTTP endpoints. It periodically checks the availability of specified endpoints and calculates their uptime percentages. The application reads a list of endpoints from a YAML file and checks each endpoint every 15 seconds to determine if it's 'UP' (responding with a 2xx status code within 500 ms) or 'DOWN'.


## Features
- **Concurrent Checks**: Utilizes threading to perform health checks on multiple endpoints simultaneously.
- **Configurable via YAML**: Easy configuration of endpoints through a YAML file.
- **Logging**: Detailed logging of health check results and errors.


## Prerequisites
- Python 3.6 or higher
- `requests` library
- `PyYAML` library


## Installation
1. Clone the repository: git clone https://github.com/patkolak/fletch-assessment/
2. Install required dependencies: pip install -r requirements.txt


## Usage
1. Edit the `sample.yaml` file to list the endpoints you want to monitor.
2. Run the script: python main.py


## Configuration
- Modify `sample.yaml` to add or remove HTTP endpoints.
- Each endpoint can be configured with the following properties:
- `url`: The URL of the endpoint.
- `method`: (Optional) HTTP method (default is GET).
- `headers`: (Optional) HTTP headers.
- `body`: (Optional) Request body for methods like POST.


## Logging
- The application logs the status of each domain after every check cycle.
- Logs include availability percentages and any errors encountered.
