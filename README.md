# Algorand Open Source Verifier
The Algorand Open Source Verifier provides tools to check Algorand contract source code against on-chain applications.  

Currently the verifier supports TEAL source code only - [Why PyTeal and Reach is not Currently Supported](algorand_verifier_lib/README.md#why-pyteal-and-reach-is-not-currently-supported)

It is made up of 2 parts currently:
- The Python [Algorand Verifier Library](https://pypi.org/project/algorand-verifier-lib/) - which is a normal Python package that can be imported. For more detail on the library see it's [README.md](algorand_verifier_lib/README.md)
- A Django Webapp which imports the library

## Django Webapp
The webapp provides an easy-to-use GUI to the verifier library. A simple form is used with 2 options "Verify" and "Verify and Submit" - in both cases the verification takes place for the provided contract source code and application ID, which checks if it matches the on-chain application.  

If the "Verify and Submit" button is clicked, assuming the contract is verified, then it will be added to the list maintained by the Django app. This allows other users visiting the site to see recently verified contracts.  

## Deployment
### Linux Deployment
To deploy normally without Kubernetes on a Linux system.  

First initialise a virtualenv and install the dependencies of the webapp:
```
git clone https://github.com/mark-ruddy/algo_open_source_verifier
cd algo_open_source_verifier/webapp
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Export a valid Purestake API key on the environment and launch the server:
```
export PURESTAKE_API_KEY=XYZ
python manage.py runserver 0.0.0.0:8000
```

### Helm Deployment on a Kubernetes Cluster
To deploy on a Kubernetes cluster, a Helm chart is provided.

Build a new container image of the webapp - assuming you have a registry running at `localhost:30000`:
```
podman build . -t localhost:30000/algorand_webapp:0.0.2
podman push localhost:30000/algorand_webapp:0.0.2
```

Check the `webapp_chart/values.yaml`, these can be overridden depending on your configuration.  

The `purestake_api_key` value is mandatory to override as base64 to be included in a Kubernetes secret:
```
export ENCODED_PURESTAKE_API_KEY=$(echo "<YOUR_PURESTAKE_API_KEY>" | base64)
helm install algorand-verifier webapp_chart/ --set purestake_api_key="$ENCODED_PURESTAKE_API_KEY"
```

The deployment will be running on a nodePort - if your host machine is a node, it will by default be available at <http://127.0.0.1:31850/>
```
kubectl get svc | grep algorand
```

If your host machine is not a node, the app should be available at the `31850` port under any node IP which can be seen using:
```
kubectl get nodes -owide
```

### Technical Design
The webapp uses the `helper` functions from the library, which assume the simplest form of Algorand API communication, using the Purestake mainnet endpoint with a Purestake API key.  

Currently `sqlite` is used as the database which is Django's default. This DB is stored as a file at `webapp/db.sqlite3`. In a real deployment `sqlite` could be continued to be used for most cases, and the `db.sqlite3` could be easily backed up from the deployment servers.

There is no javascript frontend library used etc., just pure Django with MVC model. The frontend is styled and made responsive using `bootstrap4`.
