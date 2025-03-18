# Embedding calculation using model registry to SPCS deployment

This repo shows how to deployment an embedding model into SPCS using model registry. Also performs how to interact with the REST API in a single record format, as well as with locust using JWT authentication.

Locust Test report overview:

![Embedding calculation](locust_test_report_overview.png?raw=true "Overview")

Locust Test report chart:

![Embedding calculation](locust_test_report_chart.png?raw=true "Overview")

### Snowflake notebook for deployment
Bring in `Model Registry based model deployment to SPCS for GPU inferencing.ipynb` as a Snowflake notebook and attach it to container runtime notebook running on gpu_nv_s compute pool.

```
CREATE COMPUTE POOL if not exists kipi_dev_gpu_nv_s
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = GPU_NV_S
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  AUTO_SUSPEND_SECS = 300
  ;
```

Run through all the steps and get the endpoint. 

### Setup For REST API

We will be using JWT authentication for interacting with REST API deployed on SPCS. 

1. Create private/public key pair
    - openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
    - openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
    - ALTER USER <user-name> SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';

2. Update the user with the public key. For example:
```
use role securityadmin;

ALTER USER plakhanpal SET RSA_PUBLIC_KEY='X';
```

### Setup for conda environment
1. Run `conda create -n gpu_model_registry_to_spcs python=3.11`.
2. Run `conda activate gpu_model_registry_to_spcs`.
3. Run `pip install -r requirements.txt`

### Testing single record
1. Copy rsa_key.p8 into `single_record_rest_api` folder and change the following params in `Embedding with JWT.ipynb` notebook.
```
account = "sfsenorthamerica-demo391"
user = "PLAKHANPAL"
endpoint = "nd64aqc-sfsenorthamerica-demo391.snowflakecomputing.app"
role = "SYSADMIN"
```
2. Execute the notebook `Embedding with JWT.ipynb`.

### Performing locust based performance testing
1. Copy rsa_key.p8 into `locust` folder and change the following params in `locustfile.py`.
```
account = "sfsenorthamerica-demo391"
user = "PLAKHANPAL"
endpoint = "nd64aqc-sfsenorthamerica-demo391.snowflakecomputing.app"
role = "SYSADMIN"
```
2. Alter locust params in `execute.sh` if you like.
3. Run `sh execute.sh`. This will create `gpu_embedding_run.html` file. Double clicking it will open up the HTML file graphs.