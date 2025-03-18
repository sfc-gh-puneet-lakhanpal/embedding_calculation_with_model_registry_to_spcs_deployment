
from locust import User, task, between
from accessviakeypair import get_jwt
import logging
import json
import requests
import os
import sys
import json
account = "sfsenorthamerica-demo391"
user = "PLAKHANPAL"
private_key_file_path = "./rsa_key.p8"
endpoint = "nd64aqc-sfsenorthamerica-demo391.snowflakecomputing.app"
role = "SYSADMIN"
endpoint_path = "/encode"
spcs_url=f'https://{endpoint}{endpoint_path}'
data = {'data': [[0, 'This is the first sentence.']]}
jwt = get_jwt(account, user, private_key_file_path, endpoint, role)
print(jwt)
def embed(token, url, data):
  # Create a request to the ingress endpoint with authz.
  headers = {'Authorization': f'Snowflake Token="{token}"'}
  response = requests.post(url,  json=data, headers=headers)
  return response.text
class ClassificationUser(User):
    @task
    def generation(self):
        # Invoke the model
        with self.environment.events.request.measure("[Send]", "Embedding REST API performance authenticated with JWT"):
            results = embed(token=jwt, url=spcs_url, data=data)
            #logging.info(results)
                  
