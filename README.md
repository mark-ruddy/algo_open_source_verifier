# Algorand Open Source Verifier
The Algorand Open Source Verifier provides tools to check Algorand contract source code against on-chain applications.  

It is made up of 2 parts currently:
- The Python Algorand Verifier Library - it is a normal Python package that can be imported anywhere https://pypi.org/project/algorand-verifier-lib/. For more detail on library see it's [README.md](algorand_verifier_lib/README.md)
- A Django Webapp which utilises the library features

## Django Webapp
The webapp provides an easy-to-use GUI to the verifier library. A simple form is used with 2 options "Verify" and "Verify and Submit" - in both cases the verification takes place for the provided contract source code and application ID, which checks if it matches the on-chain application.  

If the "Verify and Submit" button is clicked, assuming the contract is verified, then it will be added to the list maintained by the Django app. This allows other users visiting the site to see recently verified contracts.  

### Technical Implementation
It uses the `helper` functions from the library, which assume the simplest form of Algorand API communication, using the Purestake mainnet endpoint with a Purestake API key.  

It currently uses a `sqlite` database which is Django's default. This DB is stored as a file at `webapp/db.sqlite3`. In a real deployment `sqlite` could be continued to be used for most cases for relatively low-traffic website, and the `db.sqlite3` could be easily backed up from the deployment servers.

There is no javascript frontend library used etc., just pure Django with MVC model. The frontend is styled and made responsive using `bootstrap4`.

### Deployment
To deploy normally without Kubernetes on a Linux system.  

First initialise a virtualenv and install the dependencies of the webapp:
```
cd webapp
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Export a valid Purestake API key on the environment and launch the server:
```
export PURESTAKE_API_KEY=XYZ
python manage.py runserver 0.0.0.0:8000
```

### Helm Deployment
To deploy on a Kubernetes cluster, a Helm chart is provided.

Build a new container image of the webapp - assuming you have a registry running at `localhost:30000` the following code will work:
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
