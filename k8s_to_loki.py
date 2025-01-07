import os
import time
import json
import requests
import re
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from datetime import datetime, timezone

#----------------------------------------------------------------#
# set environment variables
#----------------------------------------------------------------#
# Get environment variables with validation
loki_url = os.getenv('LOKI_URL')
namespace = os.getenv('NAMESPACE')
interval_str = os.getenv('INTERVAL')
container_names = os.getenv('CONTAINER_NAMES')

# Validate all required environment variables are set
if loki_url is None:
    raise ValueError("LOKI_URL environment variable is not set")
if namespace is None:
    raise ValueError("NAMESPACE environment variable is not set")
if interval_str is None:
    raise ValueError("INTERVAL environment variable is not set")
if container_names is None:
    raise ValueError("CONTAINER_NAMES environment variable is not set.")

# Set the variables after validation
LOKI_URL = loki_url
NAMESPACE = namespace
INTERVAL = int(interval_str)  # Convert to integer after validation
CONTAINER_NAMES = container_names.split(',')  # Convert comma-separated string to list

#----------------------------------------------------------------#
# END set environment variables
#----------------------------------------------------------------#

#----------------------------------------------------------------#

# Track the last log timestamp for each container
last_timestamps = {}

#----------------------------------------------------------------#


#----------------------------------------------------------------#
# functions 
#----------------------------------------------------------------#

def get_k8s_client():
    """Initialize Kubernetes API client."""
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()
    return client.CoreV1Api()

def parse_timestamp(timestamp_str):
    """Parse Kubernetes timestamp format with variable precision."""
    timestamp_str = timestamp_str.rstrip('Z')
    parts = timestamp_str.split('.')
    if len(parts) == 2:
        parts[1] = parts[1][:6].ljust(6, '0')
        timestamp_str = f"{parts[0]}.{parts[1]}"
    timestamp_str += 'Z'
    return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

def calculate_seconds_since(timestamp_str):
    """Calculate seconds elapsed since the given timestamp."""
    if not timestamp_str:
        return None
    try:
        last_time = parse_timestamp(timestamp_str).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        seconds = int((now - last_time).total_seconds())
        return max(1, seconds)  # Ensure we don't return 0 or negative values
    except Exception as e:
        print(f"Error calculating time difference: {e}")
        return None

def get_pod_logs(v1_api, pod_name, container_name, namespace, since_seconds=None):
    """Fetch logs for a specific container in a pod."""
    try:
        return v1_api.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container_name,
            timestamps=True,
            since_seconds=since_seconds,
            tail_lines=None
        )
    except ApiException as e:
        print(f"Error fetching logs for {pod_name}/{container_name}: {e}")
        return ""

def send_logs_to_loki(log_lines, pod_name, container_name):
    for line in log_lines:
        try:
            parts = line.split(' ', 1)
            if len(parts) != 2:
                continue
                
            timestamp, message = parts
            
            if not message.strip():
                continue
                
            clean_line = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', message)
            clean_line = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', clean_line)
            clean_line = clean_line.replace('"', '\\"').replace("'", "\\'")

            dt = parse_timestamp(timestamp)
            nano_timestamp = str(int(dt.replace(tzinfo=timezone.utc).timestamp() * 1e9))

            payload = {
                "streams": [{
                    "stream": {
                        "namespace": "chart-test",
                        "pod": pod_name,
                        "container": container_name
                    },
                    "values": [
                        [nano_timestamp, clean_line]
                    ]
                }]
            }

            response = requests.post(
                LOKI_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=5
            )

            if response.status_code not in [200, 204]:
                print(f"Error {response.status_code}: {response.text}")
            elif response.status_code == 204:
                print(f"Log sent successfully for {container_name}: {clean_line[:50]}...")

        except Exception as e:
            print(f"Error processing log for {container_name}: {str(e)}")
            continue

#----------------------------------------------------------------#
# END functions 
#----------------------------------------------------------------#


def main():
    """Main function."""
    v1_api = get_k8s_client()
    
    while True:
        print("Fetching container logs...")
        try:
            pods = v1_api.list_namespaced_pod(namespace=NAMESPACE)
            
            for pod in pods.items:
                pod_name = pod.metadata.name
                container_names = [container.name for container in pod.spec.containers]
                
                # Check each target container
                for container_name in CONTAINER_NAMES:
                    if container_name in container_names:
                        pod_key = f"{pod_name}/{container_name}"
                        
                        # Calculate seconds since last timestamp
                        since_seconds = calculate_seconds_since(last_timestamps.get(pod_key))
                        logs = get_pod_logs(v1_api, pod_name, container_name, NAMESPACE, since_seconds)
                        
                        if logs:
                            log_lines = logs.strip().split("\n")
                            if log_lines and log_lines[0]:
                                send_logs_to_loki(log_lines, pod_name, container_name)
                                
                                # Update the last timestamp
                                last_line = log_lines[-1]
                                timestamp = last_line.split(' ', 1)[0]
                                last_timestamps[pod_key] = timestamp

        except Exception as e:
            print(f"Error fetching or processing logs: {e}")

        print(f"Sleeping for {INTERVAL} seconds...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()