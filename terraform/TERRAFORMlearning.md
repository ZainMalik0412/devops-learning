# Terraform Notes (Zain's DevOps Learning)

## Table of contents
1. [What is Infrastructure as Code](#what-is-infrastructure-as-code)
2. [Terraform overview](#terraform-overview)
3. [Orchestration vs configuration management](#orchestration-vs-configuration-management)
4. [Terraform workflow](#terraform-workflow)
5. [Terraform state](#terraform-state)
6. [Providers and required providers](#providers-and-required-providers)
7. [Core commands and what they do](#core-commands-and-what-they-do)
8. [Reading a plan and resource actions](#reading-a-plan-and-resource-actions)
9. [Resource blocks](#resource-blocks)
10. [Terraform import](#terraform-import)
11. [Local vs remote state](#local-vs-remote-state)
12. [Backends and S3 remote state](#backends-and-s3-remote-state)
13. [State locking and state security](#state-locking-and-state-security)
14. [Variables](#variables)
15. [Input variables and tfvars](#input-variables-and-tfvars)
16. [Local variables](#local-variables)
17. [Output values](#output-values)
18. [Variable precedence hierarchy](#variable-precedence-hierarchy)
19. [Variable types](#variable-types)
20. [Terraform modules](#terraform-modules)
21. [Module best practices](#module-best-practices)
22. [Modules in practice](#modules-in-practice)
23. [Common interview topics](#common-interview-topics)

---

## What is Infrastructure as Code

**Infrastructure as Code (IaC)** is the practice of defining and managing infrastructure using code rather than manual clicks.

Benefits:
- Automation and repeatability
- Consistency across environments
- Version control and review (treat infrastructure like software)
- Faster provisioning and safer changes

---

## Terraform overview

Terraform is an **IaC orchestration tool** that can deploy infrastructure across:
- cloud providers (AWS, Azure, GCP)
- other providers (GitHub, Datadog, Cloudflare)
- Kubernetes resources

Terraform uses:
- `.tf` files to define the **desired state**
- a **state file** to track the **current state**
- providers to interact with APIs

Terraform modules and providers are published via the **Terraform Registry**.

---

## Orchestration vs configuration management

Terraform is primarily used for **infrastructure orchestration**.

Configuration management tools (for example Ansible) are used for **configuring software on servers**.

### Simple analogy
- **Orchestration (Terraform)**: getting to transport and tents ready for Hajj (setting up infrastructure)
- **Configuration management (Ansible)**: supporting each pilgrim with what they need (configuring systems and applications on infrastructure)

### Practical examples
- Terraform: provision VPCs, subnets, EC2 instances, load balancers
- Ansible: configure an EC2 instance to run NGINX or host WordPress

---

## Terraform workflow

A typical Terraform workflow:

1. `terraform init`  
2. `terraform validate`  
3. `terraform plan`  
4. `terraform apply`  
5. `terraform destroy` (when you need to tear down)

---

## Terraform state

The Terraform **state file** is a record of existing infrastructure managed by Terraform.

Key ideas:
- **Desired state**: what you define in `.tf` files
- **Current state**: what Terraform believes exists, stored in `.tfstate` file

Terraform compares desired state to current state to decide what changes to make.

### Idempotency
Terraform aims for **idempotent** behaviour: applying the same configuration should result in the same infrastructure unless you change the code.

---

## Providers and required providers

A **provider** is a plugin that allows Terraform to interact with a platform's API (for example AWS).

### Required providers
You define:
- which providers you need
- where they come from
- what version to use

This ensures consistent and repeatable deployments.

---

## Core commands and what they do

| Command | What it does |
| --- | --- |
| `terraform init` | Initialises the working directory, installs providers, configures backend |
| `terraform validate` | Validates configuration syntax and internal consistency |
| `terraform plan` | Previews changes required to reach desired state |
| `terraform apply` | Applies the plan and updates infrastructure |
| `terraform destroy` | Destroys resources managed by the current configuration |

---

## Reading a plan and resource actions

Terraform plan output shows the actions it will take.

| Symbol | Meaning |
| --- | --- |
| `+` | create |
| `~` | update in-place |
| `-` | destroy |

Example interpretation:
- `aws_instance.example` will be created
- `aws_security_group.example` will be modified in place
- `aws_s3_bucket.example` will be destroyed

---

## Resource blocks

A **resource block** defines a piece of infrastructure Terraform manages.

Example concept (EC2 instance):
- resource type: `aws_instance` 
- resource name: `test` 
- attributes: AMI, instance type, tags, etc

Key attributes explained:
- `ami`: AMI used to launch the instance (template)
- `instance_type`: hardware specification (CPU, memory)
- `tags`: labels for organisation and identification

Typical workflow:
1. configure provider (AWS credentials and region)
2. write the resource block
3. run `terraform plan` 
4. run `terraform apply` 

---

## Terraform import

Terraform import lets you bring **existing resources** under Terraform management.

When you import:
- you must create a matching resource block in code
- desired state should match the real resource
- after import, `terraform plan` should ideally show **no changes**

### Import steps (typical)
1. Identify the existing resource (instance, VPC, bucket, etc)
2. Create a corresponding resource block in Terraform
3. Run the import command using the real resource ID
4. Run `terraform plan` to confirm no drift

Example pattern:
```bash
terraform import aws_instance.import i-09c0dde38e6203366
```

If the plan shows changes after import:
- update attributes (for example tags) in your `.tf` so code matches reality
- aim for a clean plan (no creates or destroys)

---

## Local vs remote state

### Local state
Terraform stores state in the project directory by default.

**Pros:**
- quick setup
- good for single person learning projects

**Cons:**
- not safe for collaboration
- no locking by default

### Remote state
State stored in a shared location (for example S3).

**Pros:**
- collaboration friendly
- supports state locking
- centralised and backed up
- better security controls

---

## Backends and S3 remote state

A backend defines where Terraform stores state and how operations are performed.

Common remote backend on AWS:
- S3 bucket for state storage
- DynamoDB for state locking (recommended)

Backend config commonly includes:
- `bucket`: S3 bucket name
- `key`: path to the state file inside the bucket
- `region`: region of the bucket

After setting a backend:
- run `terraform init` to initialise it
- Terraform can migrate local state to the remote backend
- ensure IAM permissions allow access to the bucket and lock table

---

## State locking and state security

State file safety matters because it can contain sensitive information.

Good practices:
- enable state locking (prevents concurrent updates corrupting state)
- encrypt state at rest (S3 encryption)
- restrict access via IAM
- enable S3 versioning for rollback and audit
- avoid storing secrets in plain text state where possible

---

## Variables

Variables help you:
- manage different environments with the same code
- reduce repetition (DRY)
- make modules reusable
- change values without rewriting code

---

## Input variables and tfvars

### Input variables
- define in `variables.tf`
- referenced across your configuration
- example use case: define `instance_type` once and reuse it

### tfvars
`.tfvars` files supply values to input variables
- helps keep environment-specific values separate from code

---

## Local variables

Local variables are internal helper values:
- defined once and reused
- reduce duplication
- improve readability and consistency

---

## Output values

Output values display useful information after `terraform apply`.

### Why outputs matter
- show important values (instance ID, load balancer DNS name)
- pass values into other configurations or tooling

### Good practice
- use descriptive output names
- include clear descriptions

---

## Variable precedence hierarchy

Terraform picks variable values in this order (highest first):
1. Command line flags (`-var`)
2. Environment variables (`TF_VAR_*`)
3. `.tfvars` files
4. Default values in variable blocks (lowest)

Example CLI override:
```bash
terraform apply -var="instance_type=t3.micro"
```

---

## Variable types

### Primitive types

| Type | Meaning |
| --- | --- |
| string | text values |
| number | whole or fractional numbers |
| bool | true or false |

### Complex types

| Type | Meaning |
| --- | --- |
| list | ordered sequence of the same type |
| map | key value pairs |
| object | attributes with different types |

---

## Terraform modules

A module is a collection of Terraform files grouped into a reusable unit.

Think of modules like:
- infrastructure blueprints
- Lego blocks you can reuse across projects

Modules help with:
- reusability
- organisation
- consistency
- collaboration

---

## Module best practices

Good modules should:
- output useful values (for example instance ID)
- be documented clearly
- avoid hard coding values (use variables)
- avoid mixing unrelated resources (keep modules focused)
- be tested across environments where possible

---

## Modules in practice

Important behaviour:
- Terraform only manages resources that are referenced by your root configuration
- if you remove a module call, Terraform may plan to destroy the resources it created

Typical pattern:
1. create a module directory with its own `main.tf`, `variables.tf`, `outputs.tf`
2. call the module from root `main.tf`
3. run `terraform init` to download and initialise modules
4. run `terraform plan` and `terraform apply`

---

## Common interview topics

*This section appears to be incomplete - you may want to add common Terraform interview questions here.*