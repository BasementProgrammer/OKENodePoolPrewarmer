import oci
import sys
import time


def printUssage():
    print("NodePoolStepper - Python tool to stagger the scale up of an OKE node pool.")
    print("")
    print("This will add nodes to the node pool in steps, reducing the impoct to other services such as OCIR and Onject Storage")
    print("For nodes that have cloud init script that hit these services a lot.")
    print("")
    print("Usage: NodePoolStepper.py NodePoolID DesiredSize StepSize StepTime")
    print("  NodePoolID - The OCID of the node pool to step up.")
    print("  AdditionalCapacity - The number of nodes to add to the pool.")
    print("  StepSize - The numner of nodes to add in each step.")
    print("  StepTime - The time to wait between checks.")
    print("Example: NodePoolStepper.py ocid1.nodepool.oc1..aaaaaaaaxxxxx 500 100 30")
    print("")

if (len(sys.argv) != 5):
    printUssage()
    exit(1)

NodePoolId = sys.argv[1]
AdditionalCapacity = int(sys.argv[2])
StepSize = int(sys.argv[3])
StepTime = int(sys.argv[4])

#NodePoolId = "ocid1.nodepool"
#AdditionalCapacity = 10
#StepSize = 2
#StepTime = 5

config = oci.config.from_file()  # Assumes default config file at ~/.oci/config
container_client = oci.container_engine.ContainerEngineClient(config)

# By default this will hit the auth service in the region the instance is running.
#signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
#container_client = oci.container_engine.ContainerEngineClient(config={}, signer=signer)

steps = int(AdditionalCapacity / StepSize + .9)  # Round to nearest integer
print(f"Stepping up node pool: {NodePoolId}.")
print(f"Adding an additional {AdditionalCapacity} nodes in {steps} steps of {StepSize} nodes every {StepTime} seconds.")



nodePoolDetails = container_client.get_node_pool(NodePoolId).data
currentSize = nodePoolDetails.node_config_details.size
DesiredSize = currentSize + AdditionalCapacity

for step in range(steps):
    # Figure out what the new size should be based on the current size and the step size.
    NewSize = StepSize + currentSize
    # The new size could exceed the desired size if the additional capacity is not evenly divisable by the step size.
    # so make sure we don't exceed it the desired size
    if (NewSize > DesiredSize):
        NewSize = DesiredSize
    print(f"Setting node pool size to {NewSize}.")

    # Create an update command for the node pool to add one step worth of capacity to the node pool
    # at each step
    update_details = oci.container_engine.models.UpdateNodePoolDetails(
        node_config_details=oci.container_engine.models.UpdateNodePoolNodeConfigDetails(
            size=NewSize
        )
    )
    # Trigger the update
    response = container_client.update_node_pool(
        node_pool_id=NodePoolId,
        update_node_pool_details=update_details
    )
    # Update the current size to reflect the update we just made.
    # You could make an API call to be more confdent of the update but this is close enough for this example.
    currentSize = NewSize
    # Wait for the node pool to complete the update before proceeding to the next step.
    # This will control the number of new nodes that attempt to spin up at one time.
    while True:
        nodePoolDetails = container_client.get_node_pool(NodePoolId).data
        if nodePoolDetails.lifecycle_state == "ACTIVE":
            break
        print("Waiting for node pool to become ACTIVE...")
        time.sleep(StepTime)

print("Node pool step up complete.")
print("Exiting.")


