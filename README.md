# OKE Node Pool Pre-Warmer

Python script designed to grab capacity to your account for an OKE Nodepool to leverage using self-service capacity reservations.

## Business Problem
You want to be able to scale up your OKE Node pools, hwoever you want to ensure capacity before your job kicks off. You do not want to risk having an out of capacity issue during the execution of your job.

## Ussage
Set up a node pool for each Availaility Domain that you intend to use.
Bind each node pool to a capacity reservation.
Edit the script to identify the the reservations that you will use, and the desired capacity overall.

This script will update the capacity for each node pool to a portion of the requested calpacity, and then wait for the node pools to obtain the correct number of pools. 

Update the following sections.
Set the Reservations to the OCIDs for up to three reservations that will be updated.
Each reservation should have a single placement group definition.

```
RESERVATION1 = "ocid1......."
RESERVATION2 = "ocid1......."
RESERVATION3 = "ocid1......."

reservationCount = 3    # Number of reservations to monitor
desiredCapacity = 100   # Desired total capacity to reach
minimumCapacity = 90    # Minimum capacity acceptable
checkInterval = 1       # Interval in seconds to check the capacity
maximumTests = 10       # Maximum number of times we will check each reservation before giving up.
```