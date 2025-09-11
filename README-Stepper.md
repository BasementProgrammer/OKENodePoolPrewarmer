# Node Pool Stepper
Python script to add capacity to an OKE node pool in steps.

## Business Problem
You have a node pool, and each instance in that node pool pulls a number of 
container images from OCIR or downloads a lot of files from Object Storage.
As a result your scaling runs into issues with other service limits throtteling.

## Using the script
Run the command:
python3 NodePoolStepper.py NodePoolID DesiredSize StepSize StepTime
```
python3 NodePoolStepper.py OCIDABC 500 100 10
```
The script will attempt to add 500 nodes to the nodepool identified bu the OCID. 
The capacity will be added 100 nodes at a time, and will then loop, waiting for the 
node pool to enter an ACTIVE state before attempting to add another set of 100 
nodes to the pool. You can adjust the settings to get the results that work for you.

Note the script will not attempt to move on to the next step until the previouse step has stabelized.
