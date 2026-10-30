from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

ns = client.V1Namespace(metadata=client.V1ObjectMeta(name="store-test"))
v1.create_namespace(ns)
print("namespace is ready")