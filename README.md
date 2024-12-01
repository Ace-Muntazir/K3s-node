# K3s Based Setup
## K3s - Lightweight Kubernetes

K3s is a lightweight, fully compliant Kubernetes distribution designed for simplicity and efficiency. It is optimized for production workloads, edge devices, and IoT environments.

## Why K3s?

- **Lightweight**: Minimal resource consumption compared to standard Kubernetes (K8s).
- **Simplified installation**: One-line install script to get started quickly.
- **Efficient**: Stripped down to essentials while retaining compatibility with Kubernetes APIs.
- **Extendable**: Easy to add nodes and scale workloads.

## Why Prefer K3s Over Other Tools?

- **K3d**: K3d is a wrapper that runs K3s in Docker. K3s is more efficient and doesn't rely on Docker.
- **kind**: While `kind` is great for testing Kubernetes, it is resource-intensive and not ideal for production.
- **Minikube**: Minikube is useful for local setups but is Docker-dependent and less optimized for edge or production environments.
- **Kubernetes**: K3s is a stripped-down Kubernetes, perfect for small to medium workloads without losing functionality.

## Prerequisites

- Linux-based machine (e.g., Ubuntu).
- `curl` command installed.
- Root or sudo access.

## Steps to Install K3s

1. **Run the Installation Command**:
   ```bash
   curl -sfL https://get.k3s.io | sh -
   ```

2. **Verify Installation**:
   ```bash
   kubectl get nodes
   ```

## Deploying a Python Server

The Python server is a lightweight service designed to listen for incoming HTTP requests. Upon receiving a request, it processes the payload and dynamically creates pods in the Kubernetes cluster. It utilizes the Kubernetes Python client to interact with the Kubernetes API.

### Python Server Code

You can find the Python server code in this folder: **[Python Server Code](./python-server/server.py)**.

An already-built Docker image for the server is available at: ```mrace17/python-server:1.0.2```.


### Deployment Steps:
### **Deployment Steps**

Follow these steps to deploy the Python server and ensure it has the necessary permissions to interact with the Kubernetes API:  

1. **Deploy Authorization Configuration**  
   Apply the `auth.yaml` file to set up the required permissions for the Python server to create, delete, and manage pods in the cluster.  
   ```bash
   kubectl apply -f k8s/manifests/auth.yaml
    ```  
   Verify that the service account has all required permissions:

   ```bash
   kubectl auth can-i create pods --as=system:serviceaccount:default:default -n default
   kubectl auth can-i update pods --as=system:serviceaccount:default:default -n default
   kubectl auth can-i delete pods --as=system:serviceaccount:default:default -n default
    ```   
2. **Deploy Python Server**  
   Run the Deployment and Service for the Python server from the provided manifests directory: `k8s/manifests`.

    ```bash
    kubectl apply -f k8s/manifests/main.yaml
    ```  
   Check if the Python server's pod is running successfully:
    ```bash
    kubectl get pods
    ```    
3. **Get Service Details**  
  Retrieve the service details to interact with the Python server:
      ```bash
    kubectl get svc python-server
    ``` 
4. **Test the Python Server**  
  Once the Python server is running, you can test its functionality by sending a POST request to create a new pod. Replace `<loadbalancer-IP>` with the external IP or NodePort of the `python-server-service`. 

   Use the following `curl` command:  

    ```bash
    curl -X POST http://<loadbalancer-IP>:5000/create-pod \
        -H "Content-Type: application/json" \
        -d '{"name": "test-pod", "image": "mrace17/my-react-app:v1"}'
     ```
    **Expected Behavior**:  
    The Python server will process the request and create a new pod using the specified image (mrace17/my-react-app:v1). 

    A dynamically generated name will be assigned to the pod to avoid conflicts. 

    Note: For each POST request sent to the server, a new pod will be created. 

    You can verify that the pod has been created by running:
    ```bash
    kubectl get pods
    ``` 
5. **Delete a Pod**

    If you want to delete any pod that was created, use the following command:
    ``` echo 
    kubectl delete pod <pod-name>
    ```
## Tear Down the Architecture

Once you're done testing or no longer need the setup, you can tear down the deployed resources to clean up the environment.

1. **Delete the Python Server Deployment and Service**  
   To remove the Python server's deployment and service, run the following command:

   ```bash
   kubectl delete -f k8s/manifests/main.yaml
2. **Delete Authorization configuration**  
   ```bash
   kubectl delete -f k8s/manifests/auth.yaml
   ```

3. **Delete Any Remaining Pods**  
    If any pods were manually created and remain, you can delete them using:
    ``` echo 
    kubectl delete pod <pod-name>
    ```
4. **Closing the k3s Cluster**

    Once you are done and no longer need the k3s cluster, you can shut it down and clean up the resources.

   **Stop the k3s Service**  
   To stop the k3s service on the node, run the following command:

   ```bash
   sudo systemctl stop k3s
   ```
5. **Uninstall k3s**  
    If you wish to fully uninstall k3s from your machine, run the following command:
    ```bash
    /usr/local/bin/k3s-uninstall.sh
    ```


### References:

- [k3s Documentation](https://k3s.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Python Client](https://github.com/kubernetes-client/python)