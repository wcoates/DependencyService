# SFS-POC

Runs on http://localhost:5000.

## Running in Docker:
https://www.docker.com/blog/containerized-python-development-part-1/
* docker build -t myimage .
* docker run -d -p 5000:5000 myimage
* docker ps
* curl http://localhost:5000

## Recommended: Running in IDE:

#### Endpoints:
* '/' GET
  * Returns "Hello World"
* '/s3access_success' POST
  * Simulates a successful task (Scripts.Script.S3AccessSuccessful)
* '/s3access_failure' POST
  * Simulates a unsuccessful task (Scripts.Script.S3AccessFailure)
 
#### Intended Flow
* Jira Service Mgmt provides a POST to SFS endpoint
  * SFS serialized response to corresponding script
* Script runs
  * Success - Status.RequestState is unchanged
  * Failure - Status.RequestState is updated to FAIL and error messages are appended to Status.RequestState.problems
* SFS updates Jira Service Ticket based on Status.RequestState
  * Update Jira Request Status - Update to "Closed" on SUCCESS/"Failed in Automation" on FAIL
  * Comment (internal only) Status.RequestState.problems on Jira Request
  
#### Considerations
* Scripts must have a corresponding Model.RequestModel
* Jira Schema and Python datamodels must be exactly the same
* Scripts must catch all exceptions
* Will need to build out clients, think about key mgmt
* Partial completion will require manual intervention
* Re-run flow - JSM moving status from Failed in Automation to To Do refires POST
  
  
