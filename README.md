# OKE Node Pool Pre-Warmer

Python script designed to obtain compute capacity for your OKE Node Pools in Capacity reservations, ensuring capacity is available as needed.

## Business Problem
This script ensure that capacity is available for your Auto-Scaller, by updating capacity reservations attached to your node pools. This allows your node pools to auto-scale as needed, within the bounds of the reservations, without risking encountering Out of Capacity errors.

## Using the script
Set up a capacity reservation in each Availaility Domain that you intend to use.
Set up a node pool for each Availaility Domain that you intend to use.
Bind each node pool to a capacity reservation.

This script will update the capacity for each reservation to a portion of the overall capacity as follows:
1 Reservation : 100%
2 Reservations : 50% each
3 Reservations: 33.3% each
The capacity request is rounded up to the next integar.

### Updating the script
Update the reservation OCIDs to reflect the reservations in your account

```
RESERVATION1 = "ocid1......."
RESERVATION2 = "ocid1......."
RESERVATION3 = "ocid1......."
```

Update the parameters to control the script behavior

```
reservationCount = 3    # Number of reservations to monitor
desiredCapacity = 100   # Desired total capacity to reach
minimumCapacity = 90    # Minimum capacity acceptable
checkInterval = 1       # Interval in seconds to check the capacity
maximumTests = 10       # Maximum number of times we will check each reservation before giving up.
```

### Output
{
    'capacityMode': 'Desired', 
    'reservationCount': 3, 
    'desiredCapacity': 100, 
    'minimumCapacity': 31, 
    'perADCapacity': 35, 
    'safeCapacity': 105
}

Capacity mode will be one of the following options:
* Desired - At least the desired number of nodes were reserved
* Minimum - At least the minumum number of nodes were reserved, but less than the desired number of nodes
* Failed - The minimum number of nodes were not reserved during the checking period.

safeCapacity will indicate the maximum node size that is safe to launch. 

safeCapacity is based on the reservation with the least number of successful nodes times the number of reservations. This could mean that the safeCapacity is less than the number of nodes reserved. This is because the Node Auto Scaler will attempt to balance the requested nodes across the various node pools for resiliency. We do not want a situation where one reservation runs out of capacity before the other reservations, and causes an out of capacity error.
