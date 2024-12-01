from flask import Flask, request, jsonify
from kubernetes import client, config
import datetime

app = Flask(__name__)

# Load Kubernetes configuration
try:
    config.load_incluster_config()
    print("Loaded in-cluster Kubernetes config")
except:
    config.load_kube_config()
    print("Loaded local Kubernetes config")

v1 = client.CoreV1Api()

@app.route('/create-pod', methods=['POST'])
def create_pod():
    data = request.json
    image = data.get('image', 'nginx')
    base_name = data.get('name', 'default-pod')

    # Generate a unique name using image name and current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pod_name = f"{base_name}-{timestamp}"

    # Define the pod manifest
    pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": pod_name},
        "spec": {
            "containers": [
                {"name": "default-container", "image": image}
            ]
        },
    }

    # Create the pod
    try:
        v1.create_namespaced_pod(namespace="default", body=pod_manifest)
        return jsonify({"status": "success", "message": f"Pod {pod_name} created!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
