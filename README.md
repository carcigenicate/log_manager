#Log Manager

## Description

This is a backend that stores log entries for easy retrieval. Input data to be stored has the shape:

    {userId: ...,
     sessionId: ...,
     actions: [{time: ..., type: ..., properties: {...}]}

Whereas the shape of the data when retrieved is:

    [{time: ...,
      type: ...,
      properties: {...},
      userId: ...,
      sessionId: ...}]

The user and session are duplicated in each entry for easy access.

## Local Deployment

In order to deploy this locally, follow these steps from the project folder:

 - Setup and activate a virtual environment if desired.
 - `pip install -r requirements.txt`
 - `python .\manage.py migrate`
 - `python .\manage.py runserver`

This will set up the database, and then start a development server.

## Testing

Basic tests are included in log_manager/tests.py. They can be run by running the following:

    python .\manage.py test

## API Documentation

There is only one endpoint due to the simplicity of the app: `/logs/`.

Change the host to fit the deployment type. `127.0.0.1:8000` is the default for local, development deploys, and is used in the examples below.

The below example uses the `requests` library to show usage of the API.

```python
import requests

url = "http://127.0.0.1:8000/logs/"
```

### Creation

```python
new_log = {"userId": "ABC123XYZ",
           "sessionId": "XYZ456ABC",
           "actions": [{"time": "2018-10-18T21:37:28-06:00",
                        "type": "CLICK",
                        "properties": {"locationX": 52, "locationY": 11}}]}

create_response = requests.post(url, json=new_log)

print(create_response.status_code)
```

### Unfiltered Retrieval

```python
retrieve_response = requests.get(url)
print(retrieve_response.json())
```


### Filtered Retrieval

Query arguments supported:
 - `user`: The name of the user to retrieve logs for.
 - `type`: The type of the log to retrieve.
 - `start_time`/`end_time`: The start and end datetimes to retrieve logs from. The end is exclusive. Datetimes are in the format `2018-10-18T21:37:28-06:00`.
    
```python
retrieve_response = requests.get(url, json={"user": "ABC123XYZ",
                                            "type": "CLICK",
                                            "start_time": "2018-10-18",
                                            "end_time": "2018-10-18"})
print(retrieve_response.json())
```

## Follow-up Question

To make this scalable to handle many clients, the machine handling the requests would need to be elastic and add additional virtual machines to handle the load as the load increases. The server instances would also need to ensure that they aren't locking resources that would prevent additional instances from being bottle-necked.

If there are well-defined times of load as well, the hypervisor could pre-emptively scale-up in anticipation of the load so clients aren't required to want for instances to spin-up.