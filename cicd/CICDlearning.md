# CI/CD Notes (Zain's DevOps Learning)

## Table of contents
1. [What CI and CD mean](#what-ci-and-cd-mean)
2. [Why CI/CD matters](#why-cicd-matters)
3. [Typical DevOps pipeline stages](#typical-devops-pipeline-stages)
4. [Source control as the starting point](#source-control-as-the-starting-point)
5. [Monitoring and logging in the pipeline](#monitoring-and-logging-in-the-pipeline)
6. [GitHub Actions overview](#github-actions-overview)
7. [GitHub Actions workflow anatomy](#github-actions-workflow-anatomy)
8. [YAML basics for GitHub Actions](#yaml-basics-for-github-actions)
9. [Basic CI workflow example](#basic-ci-workflow-example)
10. [Advanced GitHub Actions concepts](#advanced-github-actions-concepts)
11. [Matrix builds and parallel testing](#matrix-builds-and-parallel-testing)
12. [Secrets and encrypted variables](#secrets-and-encrypted-variables)
13. [Custom actions](#custom-actions)
14. [Reusable actions and consistency](#reusable-actions-and-consistency)
15. [Automated testing and linting](#automated-testing-and-linting)
16. [Deploying to real environments](#deploying-to-real-environments)
17. [Deployment strategies](#deployment-strategies)
18. [Security in CI/CD](#security-in-cicd)
19. [Debugging workflow failures](#debugging-workflow-failures)
20. [Manual triggers with workflow_dispatch](#manual-triggers-with-workflow_dispatch)

---

## What CI and CD mean

### Continuous Integration (CI)
CI is the practice of **automatically integrating code changes** from multiple contributors into a shared repository **frequently** (often multiple times a day).

Key goals:
- catch errors early
- reduce integration headaches
- keep main branch deployable

### Continuous Delivery (CD)
CD is the practice of **automatically preparing every change for release** once it passes the pipeline stages.

Key goals:
- every change that passes checks is always ready to release
- reliable and repeatable release process

---

## Why CI/CD matters

CI/CD helps deliver software faster and safer by providing:
- faster delivery and feedback loops
- improved quality (bugs are caught earlier)
- reduced release risk
- better collaboration across teams
- automation of repetitive tasks
- consistent and repeatable deployments

---

## Typical DevOps pipeline stages

A common pipeline flow looks like:

1. Commit change  
2. Trigger build (automatically)  
3. Build (compile code, resolve dependencies)  
4. Notify build outcome  
5. Run tests (ensure changes do not break functionality)  
6. Notify test outcome  
7. Deliver build to staging  
8. Deploy to production  

This is a general blueprint. The exact stages depend on product and team.

---

## Source control as the starting point

Source control is the foundation of DevOps workflows:
- code is stored and managed in a shared repo (for example GitHub)
- teams collaborate without overwriting each other's work
- history and rollback are possible
- pull requests support review before merging to main

---

## Monitoring and logging in the pipeline

A DevOps pipeline is not complete without monitoring:
- you monitor application and infrastructure continuously
- helps detect issues early after deployment

Examples of tools:
- Prometheus
- Grafana

---

## GitHub Actions overview

GitHub Actions is a CI/CD platform built into GitHub.

High level flow:
- you push or open a pull request
- event triggers a workflow defined in a YAML file
- GitHub Actions spins up a runner and executes jobs
- jobs run steps like build, tests, packaging, and deploy

What it can automate:
- build and test on every push or pull request
- deploy to staging or production after successful checks
- repetitive tasks (for example housekeeping, automation, project board management)

---

## GitHub Actions workflow anatomy

A workflow is defined in a YAML file inside:
- `.github/workflows/` 

Core building blocks:

| Concept | What it means |
| --- | --- |
| `name` | Friendly name shown in the Actions tab |
| `on` | Events that trigger workflow (push, pull_request, schedule, workflow_dispatch) |
| `jobs` | Tasks in the workflow (can run in parallel or sequentially) |
| `steps` | Commands or actions executed inside a job |

### Events
Examples of triggers:
- `push` 
- `pull_request` 
- `schedule` 
- `workflow_dispatch` (manual trigger)

### Jobs
- each job runs in its own runner environment
- jobs can run in parallel unless you define dependencies

### Steps
- steps run in order within a job
- each step can:
  - run a shell command
  - use an action (for example checkout)

---

## YAML basics for GitHub Actions

YAML is used for configuration files and is designed to be human readable.

### Key value pairs
```yaml
key: value
```

### Lists
```yaml
items:
  - item1
  - item2
  - item3
```

### Nested structures
```yaml
parent:
  child: value
```

---

## Basic CI workflow example

A simple CI pipeline that runs tests on code changes:

### Steps to create it
1. Set up a repo
2. Create workflow folder: `.github/workflows/`
3. Add a workflow file like `ci.yml`
4. Define triggers, jobs, and steps

### Example workflow (generic)
```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: |
          echo "Add your test command here"
```

This example shows structure. In real projects you'd install dependencies and run your real test command.

---

## Advanced GitHub Actions concepts

### Conditions and expressions
Conditions let you control when a job or step runs.

Example concepts:
- only deploy if tests passed
- only run a job on a specific branch
- skip steps based on environment

Expressions are used to:
- access context (branch name, event type, actor)
- perform logic (comparisons, string operations)

---

## Matrix builds and parallel testing

Matrix builds let you run the same job across multiple environments in parallel.

Typical use cases:
- test across multiple versions (Python versions, Node versions)
- test across different operating systems

Example structure:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    version: [3.10, 3.11]
```

---

## Secrets and encrypted variables

Secrets are sensitive values you should never commit to source control:
- API keys
- passwords
- credentials

### Managing secrets in GitHub
1. Go to repository Settings
2. Go to Secrets and variables
3. Add a new repository secret

### Using secrets in a workflow
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

---

## Custom actions

Custom actions are reusable units of automation you can run inside workflows.

### Types of custom actions
- JavaScript actions (Node.js)
- Docker actions (run in a container)
- Composite actions (combine multiple steps)

### Typical steps to create a custom action
1. Create a repository for the action (or a folder in a repo)
2. Add an `action.yml` metadata file
3. Write the code (or steps)
4. Publish to GitHub Marketplace (optional)

---

## Reusable actions and consistency

Reusing actions improves:
- **consistency** (all projects follow the same checks)
- **efficiency** (save time and avoid repeating boilerplate)
- **predictability** (fewer surprises in pipelines)

This reduces errors and improves reliability across multiple repos.

---

## Automated testing and linting

### Linting
Linting analyses code for:
- style issues
- potential errors
- consistent formatting

Benefits:
- maintain code quality
- catch syntax errors early
- enforce standards

### Automated testing
Tests run automatically to confirm:
- the system still works after changes
- changes did not break existing functionality

Benefits:
- early issue detection
- improves confidence in releases

---

## Deploying to real environments

Common environment types:
- **dev**: used for experimenting and rapid changes
- **staging**: mirrors production for realistic testing
- **production**: live environment used by real users

---

## Deployment strategies

### Manual deployments
- simple but slower
- prone to human error
- harder to repeat consistently

### Automated deployments
- fast and repeatable
- reduced risk of mistakes
- easier to scale across environments

---

## Security in CI/CD

Key security areas:
- secure secrets (use GitHub Secrets, never hard code credentials)
- control access to pipelines (role based access and branch protections)
- scan dependencies and containers for vulnerabilities
- audit and monitor pipeline activity

---

## Debugging workflow failures

Common causes:
- failing tests
- dependency issues
- YAML configuration errors
- permissions problems
- misconfigured environment variables or secrets

Common fixes:
- review logs in the Actions tab
- rerun the job after fixing issues
- update dependencies
- validate YAML and workflow logic
- check permissions and secret names carefully

---

## Manual triggers with workflow_dispatch

`workflow_dispatch` allows workflows to be started manually.

### Use cases
- manual deployments
- maintenance jobs
- on-demand tasks

### Example trigger
```yaml
on:
  workflow_dispatch:
```

You can add inputs to let users select environment or version at run time.