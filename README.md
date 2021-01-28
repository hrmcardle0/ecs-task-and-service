# Automated Provisioning of Tasks and Services

Creating tasks and services in ECS can be somewhat confusing at first. This template is a simple deployment of a service onto an ECS EC2 cluster. The cluster is only one EC2 instance for testing purposes. The task definition is used to
create a task, which is used to create a service that is deployed on the cluster. A Lambda function is also created, which is scheduled to run every minute based on a CloudWatch event. The lambda function tests the HTTP endpoint of the application
and sends an SNS topic of it's status. 

A task definition represents a definition of a task, or a container and it's environment. Here we load a simple PHP app from the AWS ECS base container image from the AWS repository. 

A service is created from the task, and represents a persistent state of that task on the cluster. We set our service to ensure there is always one container running. If the container stops, another one is automatically started on the cluster
without user intervention.

The final piece is the lambda function, which is invoked each minute upon template creation. The function tests the container endpoint by cURLing the public IP of the cluster instance. It proceeds to send an sns message to a topic about the curent
status. This function gets the public IP from AWS Parameter Store, which is updated by the cloudformation template.

## **Solution Overview**