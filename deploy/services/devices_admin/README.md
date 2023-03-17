### Definition

This worker docker image is utilized for constructing ECS services and ECS tasks, based on the controller command. An ECS service represents an agent in the TESS project, while a task includes a VTN and multiple VENs, each of which is a device.

Each ECS service possesses its own Terraform remote state and lock, consisting of an S3 bucket and a DynamoDB table. The purpose of individual Terraform remote state is to avoid blocking Terraform actions by frequently adding, deleting, or updating devices (task definitions).

Another advantage is that the individual Terraform state and lock ensures the security of device actions. Each agent's devices are separated in its own state, which reduces the risk of accidentally deleting or updating unrelated agents' devices.

#### System diagram

### process time

update: 54 sec
delete: 200 sec
create: 137 sec
