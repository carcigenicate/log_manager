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

## Follow-up Question

To make this scalable to handle many clients, the machine handling the requests would need to be elastic and add additional virtual machines to handle the load as the load increases. The server instances would also need to ensure that they aren't locking resources that would prevent additional instances from being bottle-necked.

If there are well-defined times of load as well, the hypervisor could pre-emptively scale-up in anticipation of the load so clients aren't required to want for instances to spin-up.