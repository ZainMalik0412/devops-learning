# AWS Notes (Zain's DevOps Learning)

## Table of contents
1. [AWS global infrastructure](#aws-global-infrastructure)
2. [AWS global services](#aws-global-services)
3. [IAM fundamentals](#iam-fundamentals)
4. [Accessing AWS](#accessing-aws)
5. [IAM security and best practices](#iam-security-and-best-practices)
6. [Amazon compute overview](#amazon-compute-overview)
7. [EC2 fundamentals](#ec2-fundamentals)
8. [EC2 sizing and instance types](#ec2-sizing-and-instance-types)
9. [EC2 user data and bootstrapping](#ec2-user-data-and-bootstrapping)
10. [EC2 purchasing options](#ec2-purchasing-options)
11. [Security groups](#security-groups)
12. [Ports cheat sheet](#ports-cheat-sheet)
13. [Public vs private IPs and Elastic IPs](#public-vs-private-ips-and-elastic-ips)
14. [Storage basics (EBS, AMI, EFS)](#storage-basics-ebs-ami-efs)
15. [Scalability and high availability](#scalability-and-high-availability)
16. [Load balancing (ELB)](#load-balancing-elb)
17. [Application load balancer (ALB)](#application-load-balancer-alb)
18. [Network load balancer (NLB)](#network-load-balancer-nlb)
19. [Sticky sessions](#sticky-sessions)
20. [SSL and TLS basics with load balancers](#ssl-and-tls-basics-with-load-balancers)
21. [Connection draining](#connection-draining)
22. [Auto Scaling Groups (ASG)](#auto-scaling-groups-asg)
23. [Containers on AWS](#containers-on-aws)
24. [ECS basics](#ecs-basics)
25. [ECR basics](#ecr-basics)
26. [EKS basics](#eks-basics)
27. [Serverless on AWS](#serverless-on-aws)
28. [AWS networking essentials (VPC, subnets, CIDR)](#aws-networking-essentials-vpc-subnets-cidr)
29. [Internet gateway, bastion host, and NAT gateway](#internet-gateway-bastion-host-and-nat-gateway)
30. [NACL vs security groups](#nacl-vs-security-groups)
31. [VPC peering and VPC endpoints](#vpc-peering-and-vpc-endpoints)
32. [IPv6 in a VPC and egress-only internet gateway](#ipv6-in-a-vpc-and-egress-only-internet-gateway)
33. [Route 53 fundamentals](#route-53-fundamentals)
34. [Route 53 records, TTL, and alias vs CNAME](#route-53-records-ttl-and-alias-vs-cname)
35. [Route 53 routing policies and health checks](#route-53-routing-policies-and-health-checks)
36. [CloudFront fundamentals](#cloudfront-fundamentals)
37. [Putting it together (example mental model)](#putting-it-together-example-mental-model)
38. [Quick self test](#quick-self-test)

---

## AWS global infrastructure

AWS global infrastructure matters because:
- **Proximity** reduces latency when customers are closer to an AWS region
- **Compliance** may require data to stay in certain locations
- Each **Region** has multiple **Availability Zones (AZs)** for high availability
- Each AZ is one or more discrete data centres with redundant power, networking, and connectivity
- AZs are isolated from each other but connected with high bandwidth and low latency links
- **Edge locations** cache content closer to users for faster delivery (CloudFront)

---

## AWS global services

Some AWS services are global (not tied to a single region), including:
- **IAM** (Identity and Access Management)
- **Route 53** (DNS)
- **CloudFront** (CDN)
- **WAF** (Web Application Firewall)

---

## IAM fundamentals

IAM controls **who** can access **which** AWS resources and **what** they can do.

### IAM entities

| IAM concept | What it is |
| --- | --- |
| Root account | Full access account used to create the AWS account (should not be used day to day) |
| User | A person or system identity that can sign in |
| Group | A collection of users with shared permissions |
| Role | Temporary permissions assumed by services or users (no long term keys required) |

### Policies and least privilege

- Permissions are defined using **JSON policies**
- Always follow **least privilege** (only grant what is needed)

### Policy inheritance and inline policies
- A user can belong to multiple groups and receives the combined permissions
- Inline policies can be attached directly to a user or role outside of a group structure

### IAM policy structure (high level)

| Field | Meaning |
| --- | --- |
| Version | Policy language version |
| Id | Identifier for the policy (optional) |
| Statement | One or more permission statements |

Within a statement you commonly see:
- `Sid` (statement ID)
- `Principal` (who the policy applies to)
- `Action` (allowed or denied actions)
- `Resource` (resources the actions apply to)
- `Effect` (Allow or Deny)

### Password policy
Examples of what password policies can enforce:
- minimum length
- required character types

### MFA devices in AWS

| MFA type | Example |
| --- | --- |
| Virtual MFA | Google Authenticator |
| U2F security key | Physical key |
| Hardware key fob | Code generating device |
| GovCloud hardware MFA | Supports multiple tokens per device |

---

## Accessing AWS

| Method | What it is protected by |
| --- | --- |
| AWS Management Console | Password + MFA |
| AWS CLI | Access keys |
| AWS SDK | Access keys (used by applications and services) |

### AWS CLI commands

Check CLI version:
```bash
aws --version
```

Configure your keys:
```bash
aws configure
```

Confirm the current identity:
```bash
aws sts get-caller-identity
```

List IAM users:
```bash
aws iam list-users
```

---

## IAM security and best practices

### IAM security tools

| Tool | What it does |
| --- | --- |
| Credential report | Snapshot of all users and their credential status |
| Access Advisor | Shows which services a user has used, helps tighten policies |

### Best practices
- Do not use the root account except for initial setup
- Use groups for permissions where possible
- Enforce strong password policies
- Use MFA
- Use roles for temporary access instead of long term keys
- Regularly review permissions (least privilege)

---

## Amazon compute overview

Core compute options:
- **EC2**: classic virtual machines
- **ECS**: container orchestration (AWS native)
- **EKS**: Kubernetes orchestration (managed Kubernetes)

---

## EC2 fundamentals

EC2 is Infrastructure as a Service (IaaS):
- you rent virtual machines
- you control OS and configuration

Typical building blocks around EC2:
- EBS for storage
- ELB for distributing traffic
- ASG for scaling instances up and down

---

## EC2 sizing and instance types

When launching EC2 you choose:
- OS (Linux, Windows, etc)
- CPU and cores
- RAM
- storage (EBS, EFS, instance store)
- network performance
- firewall rules (security groups)
- bootstrap scripts (user data)

### Instance type naming convention
Example: `m5.2xlarge`

| Part | Meaning |
| --- | --- |
| m | instance family (general purpose) |
| 5 | generation |
| 2xlarge | size (more resources as size increases) |

### Instance families

| Family | Best for |
| --- | --- |
| General purpose | Balanced workloads, web servers, small databases |
| Compute optimised | High CPU workloads |
| Memory optimised | Large in-memory workloads |
| Storage optimised | High performance storage, large datasets |
| Accelerated computing | GPU, ML workloads |
| HPC optimised | Intensive compute + fast networking |

---

## EC2 user data and bootstrapping

User data lets you run commands at instance startup:
- script runs once
- runs as the root user
- used to install packages, configure services, pull files

Example (Amazon Linux web server bootstrap):
```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello CoderCo from $(hostname -f)</h1>" > /var/www/html/index.html
```

---

## EC2 purchasing options

| Option | Best for | Notes |
| --- | --- | --- |
| On demand | Short workloads | Pay by the second |
| Spot instances | Cheap + flexible | Can be interrupted |
| Dedicated hosts | Compliance, control placement | Entire physical server |
| Dedicated instances | Isolation | No other customers share hardware |
| Capacity reservations | Guarantee capacity | In a specific AZ |

---

## Security groups

Security groups act like a firewall around instances:
- control inbound and outbound traffic
- rules allow by IP range or by other security groups
- tied to region and VPC
- can attach one security group to multiple instances
- if traffic is blocked by a security group, the instance never sees it

Common pattern:
- one security group for SSH access (restricted to your IP)
- one security group for app traffic (HTTP or HTTPS)

Security group to security group rules:
- you can allow SG1 to communicate with SG2 without maintaining changing IP allow lists

---

## Ports cheat sheet

| Port | Use |
| --- | --- |
| 22 | SSH |
| 21 | FTP |
| 22 | SFTP |
| 80 | HTTP |
| 443 | HTTPS |
| 53 | DNS |
| 3389 | RDP (Windows) |

---

## Public vs private IPs and Elastic IPs

### IPv4 vs IPv6 (basic)
- IPv4 is most common, limited public address space
- IPv6 solves scale problems (especially IoT)

### Public vs private IP

| Type | What it means |
| --- | --- |
| Public IP | Internet routable and must be globally unique |
| Private IP | Only routable inside a private network, must be unique within that network |

Private networking often requires:
- Internet gateway and NAT to reach the internet safely

### Elastic IPs
Elastic IPs are static public IPv4 addresses you can attach to an instance.

Notes:
- an EC2 public IP can change after stop and start
- an Elastic IP can be re-mapped to another instance to mask failures
- they often indicate poor architecture decisions
- a better approach is usually DNS with Route 53 pointing to a stable endpoint like a load balancer

---

## Storage basics (EBS, AMI, EFS)

| Service | What it is |
| --- | --- |
| EBS | Network drive attached to an instance, persists data beyond instance lifecycle depending on configuration |
| AMI | Preconfigured template used to launch instances consistently |
| EFS | Managed network file system shared across multiple instances, multi-AZ and scalable, but more expensive |

---

## Scalability and high availability

### Vertical scalability
- increase instance size (more CPU or RAM)
- common for non-distributed systems like databases
- has hardware limits

### Horizontal scalability (elasticity)
- add more instances
- spreads workload
- common for web and modern apps

### High availability
- run across multiple locations (multi-AZ)
- designed to survive data centre or AZ loss

---

## Load balancing (ELB)

A load balancer forwards traffic to multiple instances and:
- spreads load to avoid overload
- provides one DNS entry point
- performs health checks
- can do SSL termination
- improves availability across AZs
- helps separate public and private traffic

AWS provides managed load balancers (ELB), which reduces maintenance overhead.

### Health checks
- health checks run against a port and path
- if target does not return 200 OK, it can be marked unhealthy

### Types of load balancers
- Classic Load Balancer (older)
- Application Load Balancer (ALB, layer 7)
- Network Load Balancer (NLB, layer 4)
- Gateway Load Balancer (layer 3)

---

## Application load balancer (ALB)

ALB:
- operates at layer 7 (HTTP and HTTPS)
- supports routing by hostname, path, and query string
- supports routing to multiple target groups
- useful for microservices and container workloads
- supports dynamic port mapping for ECS

### Target groups
Target groups are sets of destinations for traffic:
- EC2 instances
- ECS tasks
- Lambda
- IP addresses

Health checks are configured at the target group level.

Good to know:
- clients IP is passed via headers like X-Forwarded-For
- your instances see the load balancer IP directly, not the original client IP

---

## Network load balancer (NLB)

NLB:
- operates at layer 4 (TCP and UDP)
- designed for high performance and low latency
- can handle very high request volumes
- supports one static IP per AZ and can use Elastic IPs

Use cases:
- high throughput TCP or UDP workloads (for example gaming)

NLB does not inspect HTTP headers.

---

## Sticky sessions

Sticky sessions (session affinity):
- route a client consistently to the same backend instance
- supported by CLB, ALB, and NLB
- typically uses cookies for ALB and CLB
- can cause uneven load distribution, so only use when necessary

---

## SSL and TLS basics with load balancers

SSL and TLS encrypt traffic in transit.
- TLS is the modern standard, but people still say SSL
- Public SSL certificates come from certificate authorities and expire

### Using SSL with ELB
- managed using ACM (AWS Certificate Manager)
- HTTPS listeners require a certificate
- SNI (Server Name Indication) enables multiple certificates on one load balancer for multiple domains

Elastic load balancer certificate support:
- CLB: typically one certificate
- ALB and NLB: multiple certificates using SNI

---

## Connection draining

Connection draining allows in-flight requests to complete when:
- instances are deregistering
- instances are unhealthy

It stops sending new requests while allowing existing requests to finish.

---

## Auto Scaling Groups (ASG)

ASG automatically adjusts the number of EC2 instances to match load:
- maintains minimum, desired, and maximum capacity
- replaces unhealthy instances
- registers new instances with the load balancer automatically

### ASG attributes
- launch template
- AMI
- instance type
- user data
- EBS volumes
- security groups
- SSH key pair
- IAM roles
- subnet placement
- load balancer attachment

### ASG scaling policies

| Policy | What it does |
| --- | --- |
| Target tracking | Keeps a metric (like CPU) at a target value |
| Step scaling | Scales based on CloudWatch alarm thresholds |
| Scheduled scaling | Scales at set times for predictable traffic spikes |

CloudWatch alarms can trigger scaling actions based on metrics like CPU utilisation.

---

## Containers on AWS

### Docker image recap
- Docker image is the blueprint for an app
- stored in a registry like Docker Hub or AWS ECR

### VM vs container (recap)

| VM | Container |
| --- | --- |
| Full virtual OS per VM | Shares host kernel |
| Heavier and slower | Lightweight and fast |
| Higher resource overhead | Lower overhead |

### Dockerfile recap

| Instruction | What it does |
| --- | --- |
| FROM | Base image |
| COPY | Copy code into the image |
| RUN | Run build or install commands |
| CMD | Default command when container starts |

---

## ECS basics

ECS is a managed container orchestration service.

### ECS launch types

#### EC2 launch type
- you provision and maintain EC2 instances
- each instance runs the ECS agent
- you control the underlying infrastructure

#### Fargate launch type
- serverless containers
- no instance management
- define task CPU and memory, AWS provisions everything
- scale by increasing task count

### ECS IAM roles

| Role type | Purpose |
| --- | --- |
| EC2 instance profile | Used by ECS agent to call ECS APIs, send logs, pull images, access secrets |
| Task role | Per task permissions, defined in task definition |

### ECS and load balancers
- ALB is ideal for HTTP services with routing
- NLB is ideal for high performance TCP or UDP
- CLB is supported but generally not recommended, and not used with Fargate commonly

### ECS service auto scaling
Scales the number of ECS tasks based on demand using:
- target tracking
- step scaling
- scheduled scaling

---

## ECR basics

Amazon ECR is a container image registry:
- private and public repositories
- IAM controlled access
- supports vulnerability scanning
- supports image tags and lifecycle policies

---

## EKS basics

EKS is managed Kubernetes on AWS.
- runs Kubernetes control plane as managed service
- worker nodes run in your VPC
- supports EC2 worker nodes or Fargate

Common architecture ideas:
- worker nodes in private subnets
- multi-AZ for high availability
- load balancer distributing traffic to services
- NAT gateway enables private nodes to pull images without direct internet exposure

### EKS node types

| Type | What it means |
| --- | --- |
| Managed node groups | AWS manages node groups with ASG integration |
| Self-managed nodes | You manage nodes and ASG yourself |
| Fargate | No nodes to manage, serverless pods based on requirements |

---

## Serverless on AWS

Serverless means:
- you do not manage servers
- services scale automatically
- you focus on code and configuration

### Examples of serverless AWS services
- Lambda
- DynamoDB
- Cognito
- API Gateway
- S3
- SNS and SQS
- Kinesis Data Firehose
- Aurora Serverless
- Step Functions
- Fargate

### EC2 vs Lambda (quick comparison)

| EC2 | Lambda |
| --- | --- |
| Always running servers | Runs on demand |
| Limited by instance size | Limited by runtime duration |
| You manage scaling | Scaling is automatic |
| You manage infrastructure | Focus mainly on code |

### Lambda benefits:
- pay per request and compute time
- integrates with AWS services
- supports common languages
- monitoring via CloudWatch
- increasing RAM can improve CPU and networking performance

### Serverless example: S3 thumbnail generation
1. image uploaded to S3 triggers an event
2. Lambda runs, generates thumbnail
3. thumbnail saved back to S3
4. metadata can be stored in DynamoDB

### Serverless cron job
- EventBridge schedules a trigger (every hour, daily, etc)
- triggers Lambda for backups or cleanup tasks
- no server required

---

## AWS networking essentials (VPC, subnets, CIDR)

### VPC
A VPC is a private network in AWS where you isolate and control resources.

### CIDR
CIDR defines an IP range in the format:
```
base_ip/prefix_length
```

Example:
```
192.168.0.0/24 (256 IPs)
0.0.0.0/0 (all IPs)
```

#### Subnet mask intuition
As the prefix gets smaller, the range gets larger.

| Prefix | Approx IPs |
| --- | --- |
| /32 | 1 |
| /31 | 2 |
| /30 | 4 |
| /24 | 256 |
| /0 | all |

Private IPv4 ranges:
- 10.0.0.0/8
- 172.16.0.0/12 (AWS default VPC range)
- 192.168.0.0/16

### Subnets
Subnets are smaller networks inside a VPC.
- each subnet is tied to an AZ
- used to segment resources

AWS reserves 5 IP addresses per subnet (first 4 and last 1):

Example for 10.0.0.0/24:
- 10.0.0.0 network address
- 10.0.0.1 VPC router
- 10.0.0.2 DNS
- 10.0.0.3 future use
- 10.0.0.255 reserved (AWS does not support broadcast)

---

## Internet gateway, bastion host, and NAT gateway

### Internet gateway (IGW)
- connects a VPC to the internet
- highly available and scalable
- must be attached to the VPC
- one IGW per VPC

An IGW alone does not grant internet access unless route tables are configured.

### Bastion host
A bastion host is a secure bridge for SSH into private instances:
- bastion sits in a public subnet
- private instances remain in private subnets
- bastion SG allows inbound SSH from a restricted IP range
- private instance SG allows inbound SSH from the bastion SG

### NAT gateway
A NAT gateway allows private subnet instances to reach the internet while blocking inbound connections from the internet.
- requires an internet gateway
- created in a specific AZ using an Elastic IP
- for high availability you deploy NAT gateways across multiple AZs

#### NAT gateway vs NAT instance

| NAT gateway | NAT instance |
| --- | --- |
| managed by AWS | managed by you |
| scalable bandwidth | limited by instance size |
| per hour cost | EC2 pricing |
| HA requires multi-AZ deployment | you manage failover |
| no SG on NATGW | NAT instance has SG |
| cannot be used as bastion | NAT instance can be used as bastion |

---

## NACL vs security groups

| Feature | Security groups | NACLs |
| --- | --- | --- |
| Level | instance | subnet |
| Stateful | yes | no |
| Default behaviour | return traffic allowed automatically | inbound and outbound rules must both allow |
| Rule processing | evaluates all rules | first match wins based on rule number |

---

## VPC peering and VPC endpoints

### VPC peering
VPC peering privately connects two VPCs using AWS internal networking.

Important:
- peering is not transitive
- CIDR ranges must not overlap
- can peer across accounts and regions
- can reference security groups across peered VPCs

### VPC endpoints
Endpoints allow private connectivity to AWS services without using the public internet.

Benefits:
- traffic stays inside AWS network
- no need for NAT gateway or internet gateway for that service path
- scales and is redundant

#### Endpoint types

| Type | What it is |
| --- | --- |
| Interface endpoint | ENI with private IP as an entry point to a service |
| Gateway endpoint | route table target, used for services like S3 and DynamoDB |

---

## IPv6 in a VPC and egress-only internet gateway

- IPv4 cannot be disabled for VPCs
- you can enable IPv6 for dual stack (both IPv4 and IPv6)
- EC2 can have private IPv4 for internal VPC traffic and public IPv6 for internet routable access

### Egress-only internet gateway
Egress-only IGW allows:
- outbound IPv6 internet access from private subnets
- blocks inbound IPv6 connections from the internet

It is like NAT for IPv6, but without translation.

#### Dual stack routing pattern (high level)
- public subnet route table sends IPv4 and IPv6 to internet gateway
- private subnet route table sends IPv4 to NAT gateway and IPv6 to egress-only gateway

---

## Route 53 fundamentals

Route 53 is AWS managed DNS:
- highly available and scalable
- manages DNS records and traffic routing
- supports health checks and failover
- can register domain names
- designed to be resilient

### Hosted zones
Hosted zones hold DNS records for a domain and its subdomains.

| Type | Used for |
| --- | --- |
| Public hosted zone | DNS for internet accessible domains |
| Private hosted zone | internal DNS resolution within one or more VPCs |

---

## Route 53 records, TTL, and alias vs CNAME

### Route 53 record fields
A record includes:
- name
- type (A, AAAA, CNAME, NS, etc)
- value
- routing policy
- TTL

### Record types
- **A**: hostname to IPv4
- **AAAA**: hostname to IPv6
- **CNAME**: hostname alias to another hostname
- **NS**: hosted zone name servers

### TTL (time to live)

| TTL choice | Effect |
| --- | --- |
| High TTL | fewer queries, lower cost, but records take longer to update globally |
| Low TTL | more queries, higher cost, but faster changes |

Note: alias records do not require TTL.

### CNAME vs Alias

| CNAME | Alias |
| --- | --- |
| points to any hostname | points to AWS resources |
| cannot be used at root domain | works at root and non-root |
| standard DNS | Route 53 feature |
| TTL applies | no TTL |

Alias targets can include:
- ELB
- CloudFront
- API Gateway
- Elastic Beanstalk
- S3 website
- VPC interface endpoints
- Route 53 records in the same hosted zone

Alias cannot target an EC2 DNS name directly.

---

## Route 53 routing policies and health checks

Routing policies control how Route 53 responds to DNS queries.

### Routing policies

| Policy | What it does |
| --- | --- |
| Simple | returns the same record(s) |
| Weighted | split traffic by percentage |
| Failover | primary and secondary for outages |
| Latency based | routes users to lowest latency region |
| Geolocation | routes based on user location |
| Geoproximity | like geolocation with adjustable bias |
| IP based | routes based on client IP CIDR blocks |
| Multi value | returns multiple healthy records (up to 8) |

### Health checks
Health checks help Route 53 detect failures and route traffic accordingly.

Types:
- endpoint health checks (public HTTP)
- calculated health checks (based on other checks)
- CloudWatch alarm based checks (useful for private resources)

---

## CloudFront fundamentals

CloudFront is a CDN that improves performance by caching content at edge locations.

Key points:
- caches content close to users at edge locations
- helps reduce load on backend origins
- integrates with WAF and DDoS protections

### Origins
Origins are where CloudFront retrieves content from:
- S3 (static files, can lock down access using OAC)
- ALB or EC2 (custom HTTP origins)
- S3 website endpoints
- other HTTP backends

### How CloudFront works (simple)
1. client requests content
2. CloudFront edge location checks cache
3. if cached, serves instantly
4. if not cached, fetches from origin
5. caches response at the edge for next time

---

## Putting it together (example mental model)

*This section appears to be incomplete - you may want to add an example architecture diagram or walkthrough here.*

---

## Quick self test

*This section appears to be incomplete - you may want to add some practice questions here.*