import os
import secrets

import yaml
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

STORE_YAML = os.getenv(
    "STORE_YAML",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "k8s", "store.yaml"),
)


def _api_client():
    try:
        config.load_kube_config()          # laptop par chalane ke liye
    except Exception:
        config.load_incluster_config()     # baad mein cluster ke andar chalane ke liye
    return client.ApiClient()


def namespace_for(store_id):
    return f"store-{store_id}"


def create_store(store_id, storage="2Gi"):
    ns = namespace_for(store_id)
    api = _api_client()

    client.CoreV1Api(api).create_namespace(
        client.V1Namespace(metadata=client.V1ObjectMeta(name=ns))
    )

    root_pw = secrets.token_urlsafe(16)
    db_pw = secrets.token_urlsafe(16)

    with open(STORE_YAML) as f:
        docs = [d for d in yaml.safe_load_all(f) if d]

    for d in docs:
        if d["kind"] == "Secret":
            d["stringData"]["MYSQL_ROOT_PASSWORD"] = root_pw
            d["stringData"]["MYSQL_PASSWORD"] = db_pw
        if d["kind"] == "PersistentVolumeClaim" and d["metadata"]["name"] == "mysql-pvc":
            d["spec"]["resources"]["requests"]["storage"] = storage
        utils.create_from_dict(api, d, namespace=ns)

    return ns


def delete_store(store_id):
    ns = namespace_for(store_id)
    try:
        client.CoreV1Api(_api_client()).delete_namespace(ns)
    except ApiException as e:
        if e.status != 404:      # namespace pehle se nahi hai to koi dikkat nahi
            raise


def store_status(store_id):
    """'ready' agar WordPress aur MySQL dono ready hain, warna 'provisioning'."""
    ns = namespace_for(store_id)
    apps = client.AppsV1Api(_api_client())
    try:
        for name in ("mysql", "wordpress"):
            dep = apps.read_namespaced_deployment_status(name, ns)
            if (dep.status.ready_replicas or 0) < 1:
                return "provisioning"
        return "ready"
    except ApiException:
        return "provisioning"