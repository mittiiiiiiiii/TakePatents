import os
from dotenv import load_dotenv

load_dotenv()

super_user_password = os.getenv('POSTGRES_SUPERUSER_PASSWORD')
replication_user_password = os.getenv('POSTGRES_REPLICATION_PASSWORD')

secret_yaml = f"""
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: default
type: Opaque
stringData:
  superUserPassword: {super_user_password}
  replicationUserPassword: {replication_user_password}
"""

with open('k8s/my-postgres-secret.yaml', 'w') as file:
    file.write(secret_yaml)