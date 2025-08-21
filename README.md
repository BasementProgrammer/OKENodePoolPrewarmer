# OKE Node Pool Pre-Warmer

Python script designed to grab capacity to your account for a nodepool to leverage using self-service capacity reservations.

## Business Problem
You want to be able to scale up your OKE Node pools, hwoever you want to ensure capacity before your job kicks off. You do not want to risk having an out of capacity issue during the execution of your job.

## Ussage
Set up a node pool for each Availaility Domain that you intend to use.
Bind each node pool to a capacity reservation.
Edit the script to identify the the reservations that you will use, and the desired capacity overall.

This script will update the capacity for each node pool to a portion of the requested calpacity, and then wait for the node pools to obtain the correct number of pools. 