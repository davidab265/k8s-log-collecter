# Kubernetes Logs to Loki Script

This script fetches logs from specific Kubernetes containers in a namespace and forwards them to a Loki instance. It is designed to run as a service within a Kubernetes cluster.

## Features

- Fetch logs from specific containers in Kubernetes pods.
- Forward logs to a Loki instance with metadata.
- Parse timestamps to calculate log intervals.
- Clean and sanitize log lines before forwarding.
- Environment variable-based configuration.

## Requirements

- Python 3.x
- `kubernetes` Python client
- `requests` library

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables:

- `LOKI_URL`: URL of the Loki instance to forward logs to.
- `NAMESPACE`: Kubernetes namespace to monitor.
- `INTERVAL`: Interval (in seconds) between log fetches.
- `CONTAINER_NAMES`: Comma-separated list of container names to fetch logs from.

Example:
```bash
export LOKI_URL="http://loki:3100/loki/api/v1/push"
export NAMESPACE="default"
export INTERVAL="30"
export CONTAINER_NAMES="app-container,sidecar-container"
```

## Usage

Run the script:
```bash
python script.py
```

### Deployment in Kubernetes

To deploy this script as a Kubernetes pod:

1. Build a Docker image:
   ```bash
   docker build -t k8s-loki-logger:latest .
   ```

2. Push the image to your container registry.

3. Create a Kubernetes manifest (YAML file) with the following:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: k8s-loki-logger
  namespace: default
spec:
  containers:
  - name: logger
    image: <your-image-registry>/k8s-loki-logger:latest
    env:
    - name: LOKI_URL
      value: "http://loki:3100/loki/api/v1/push"
    - name: NAMESPACE
      value: "default"
    - name: INTERVAL
      value: "30"
    - name: CONTAINER_NAMES
      value: "app-container,sidecar-container"
```

4. Apply the manifest:
   ```bash
   kubectl apply -f manifest.yaml
   ```

## Code Structure

### Environment Variables

The script validates and retrieves required environment variables at the start.

### Functions

- `get_k8s_client()`: Initializes Kubernetes API client.
- `parse_timestamp()`: Parses and normalizes Kubernetes timestamp strings.
- `calculate_seconds_since()`: Calculates seconds elapsed since a given timestamp.
- `get_pod_logs()`: Fetches logs for a specific container in a pod.
- `send_logs_to_loki()`: Sends logs to the configured Loki instance.

### Main Loop

The script continuously fetches logs at intervals specified by the `INTERVAL` variable, processes them, and forwards them to Loki.

## Troubleshooting

- **Error: Environment variable not set**: Ensure all required environment variables are set before running the script.
- **Logs not sent to Loki**: Check the Loki URL and ensure the instance is reachable.
- **APIException**: Verify Kubernetes API access and permissions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

