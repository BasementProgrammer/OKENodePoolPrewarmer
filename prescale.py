# Create python code to set the capacity for an existing OCI compute reservation
import oci

RESERVATION1 = "ocid1......."
RESERVATION2 = "ocid1......."
RESERVATION3 = "ocid1......."

reservationCount = 3    # Number of reservations to monitor
desiredCapacity = 100   # Desired total capacity to reach
minimumCapacity = 90    # Minimum capacity acceptable
checkInterval = 1       # Interval in seconds to check the capacity
maximumTests = 10       # Maximum number of times we will check each reservation before giving up.

def getStatringCapacity(reservation_id):
        # Initialize the OCI client from the instance configuration
    config = oci.config.from_file()  # Assumes default config file at ~/.oci/config
    compute_client = oci.core.ComputeClient(config)
    # Get the current reservation details
    reservation = compute_client.get_compute_capacity_reservation(reservation_id).data

    config = reservation.instance_reservation_configs[0]
    return config.reserved_count


def set_compute_reservation_capacity(reservation_id, new_capacity):
    # Initialize the OCI client from the instance configuration
    config = oci.config.from_file()  # Assumes default config file at ~/.oci/config
    compute_client = oci.core.ComputeClient(config)
    # Get the current reservation details
    reservation = compute_client.get_compute_capacity_reservation(reservation_id).data

    config = reservation.instance_reservation_configs[0]
    config.reserved_count = config.reserved_count + new_capacity

    # Update the reservation with the new capacity
    response = compute_client.update_compute_capacity_reservation(reservation_id, reservation)
    return config.reserved_count

# create a function to watch a compute reservation capacity until it gets to a desired level
def watch_compute_reservation_capacity(reservation_id, desired_capacity, minimumCapacity, interval, timeout):
    import time
    compute_client = oci.core.ComputeClient(oci.config.from_file())
    
    for attempt in range(timeout):
        reservation = compute_client.get_compute_capacity_reservation(reservation_id).data
        config = reservation.instance_reservation_configs[0]
        current_capacity = config.reserved_count
        
        if current_capacity >= desired_capacity:
            print(f"Desired capacity of {desired_capacity} reached: Current capacity is {current_capacity}.")
            break        
        time.sleep(interval)
    # If we reach here, we did not reach the desired capacity in time.
    reservation = compute_client.get_compute_capacity_reservation(reservation_id).data
    config = reservation.instance_reservation_configs[0]
    current_capacity = config.reserved_count
    return current_capacity

# Calculate the desired capacity needed for each AD.
perAdDesiredCapacity = int((desiredCapacity / reservationCount) + .9)  # Round to nearest integer
print(f"Setting {perAdDesiredCapacity} capacity for each reservation.")

# Calculate the minimum capacity needed for each AD.
perAdMinimumCapacity = int((minimumCapacity / reservationCount) + .9)  # Round to nearest integer
print(f"Setting {perAdMinimumCapacity} capacity for each reservation.")

#
# Get the starting capacity for each reservation
# so thaat we can calculate how much to add.
#
startingCapacity1 = getStatringCapacity(RESERVATION1)
if (reservationCount > 1):
    startingCapacity2 = getStatringCapacity(RESERVATION2)
if (reservationCount > 2):
    startingCapacity3 = getStatringCapacity(RESERVATION3)
#
# Calculate the new desired capacity for each reservation
#
desiredCapacity1 = startingCapacity1 + perAdDesiredCapacity
if (reservationCount > 1):
    desiredCapacity2 = startingCapacity2 + perAdDesiredCapacity
if (reservationCount > 2):
    desiredCapacity3 = startingCapacity3 + perAdDesiredCapacity
#
# Calculate the new minimum capacity for each reservation
#
minimumCapacity1 = startingCapacity1 + perAdMinimumCapacity
if (reservationCount > 1):
    minimumCapacity2 = startingCapacity2 + perAdMinimumCapacity
if (reservationCount > 2):
    minimumCapacity3 = startingCapacity3 + perAdMinimumCapacity

# Set the new capacity for each reservation
set_compute_reservation_capacity(RESERVATION1, desiredCapacity1)
if (reservationCount > 1):
    set_compute_reservation_capacity(RESERVATION2, desiredCapacity2)
if (reservationCount > 2):
    set_compute_reservation_capacity(RESERVATION3, desiredCapacity3)


updatedCapacity1 = watch_compute_reservation_capacity(RESERVATION1, desiredCapacity1, minimumCapacity1, checkInterval, maximumTests)
if (reservationCount > 1):
    updatedCapacity2 = watch_compute_reservation_capacity(RESERVATION2, desiredCapacity2, minimumCapacity2, checkInterval, maximumTests)
if (reservationCount > 2):
    updatedCapacity3 = watch_compute_reservation_capacity(RESERVATION3, desiredCapacity3, minimumCapacity3, checkInterval, maximumTests)    

addedCapacity1 = updatedCapacity1 - startingCapacity1
if (reservationCount > 1):
    addedCapacity2 = updatedCapacity2 - startingCapacity2
if (reservationCount > 2):
    addedCapacity3 = updatedCapacity3 - startingCapacity3


#
# Determine the save capacity for the cluster
#
# How much capacity have we added to AD1?
perADCapacity = addedCapacity1
if (reservationCount > 1):
    if (addedCapacity2 < perADCapacity):
        perADCapacity = addedCapacity2
if (reservationCount > 2):
    if (addedCapacity3 < perADCapacity):
        perADCapacity = addedCapacity3

safeCapacity = perADCapacity * reservationCount

if (safeCapacity >= desiredCapacity):
    capacityMode = "Desired"
elif (safeCapacity >= minimumCapacity):
    capacityMode = "Minimum"
else:
    capacityMode = "Failed"

outputData = {
    "capacityMode": capacityMode,
    "reservationCount": reservationCount,
    "desiredCapacity": desiredCapacity,
    "minimumCapacity": minimumCapacity1,
    "perADCapacity": perADCapacity,
    "safeCapacity": safeCapacity
}