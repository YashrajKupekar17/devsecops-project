

# DevSecOps CI/CD Pipeline for FastAPI Application

This repository contains a complete example of a **CI/CD pipeline** built using **GitHub Actions**, **Docker**, and **Kubernetes**, with security and quality checks included.

The purpose of this project is to show how an application can be automatically tested, secured, containerized, and deployed using modern DevOps and DevSecOps practices.
The focus is not on using many tools, but on using the **right stages in the right order** and understanding why each stage is important.

---

## Why This Project Exists

In real software projects, code is constantly changing.
If builds and deployments are done manually, it often leads to:

* Bugs reaching production
* Security issues being found too late
* Inconsistent deployments
* High manual effort

This project solves those problems by introducing:

* Automated testing and quality checks
* Security scanning built into the pipeline
* Container-based packaging
* Kubernetes deployment
* Runtime verification after deployment

This approach follows **DevSecOps principles**, where security is included from the beginning of the development lifecycle.

---

## About the Application

The application used in this project is a simple **FastAPI** web service written in Python.

It is intentionally kept small so that the focus remains on the CI/CD pipeline rather than on business logic.

### Available Endpoints

* **`/health`**
  Used to check if the application is running correctly.
  This endpoint is used in both CI and CD pipelines for runtime validation.

* **`/echo/{msg}`**
  Returns the same message that is sent.
  This helps confirm that request handling works properly.

---

## CI/CD Pipeline Overview

The pipeline is divided into two parts:

### Continuous Integration (CI)

Runs automatically on every push to the `main` branch and ensures that only clean, tested, and secure code is allowed to move forward.

### Continuous Deployment (CD)

Runs after CI succeeds (and can also be triggered manually) and deploys the application to Kubernetes with runtime validation.

---

## Continuous Integration (CI) – What Happens and Why

### 1. Code Checkout

The pipeline downloads the latest code from GitHub so that it always works on the correct version.

### 2. Setup Runtime

Python is installed so the application and tests run in a consistent environment.

### 3. Linting (flake8)

Checks code formatting and style.
This prevents messy code and reduces technical debt.

### 4. Unit Tests (pytest)

Verifies that the application behaves correctly.
This helps catch bugs early and prevents regressions.

### 5. Static Security Scan (CodeQL)

Scans the source code for security vulnerabilities.
This detects insecure coding patterns before deployment.

### 6. Dependency Scan (Trivy FS)

Scans project files and dependencies for known vulnerabilities.
This protects against unsafe third-party libraries.

### 7. Docker Build

Packages the application into a Docker image.
This ensures the application runs the same way everywhere.

### 8. Docker Image Security Scan (Trivy)

Scans the built image for OS and library vulnerabilities.
This prevents unsafe images from being deployed.

### 9. Runtime Container Test

Runs the container and calls the `/health` endpoint.
This confirms that the image actually works.

### 10. Push to DockerHub

Only after all checks pass is the image pushed to DockerHub.
This ensures only trusted images are released.

---

## Continuous Deployment (CD) – What Happens and Why

### 1. Trigger

The CD pipeline is triggered automatically after CI succeeds or manually for controlled deployment.

### 2. Deploy to Kubernetes

The Docker image is deployed to a Kubernetes cluster using Minikube.

### 3. Wait for Pods

The pipeline waits until the application pods are ready.
This avoids testing before the app is fully started.

### 4. Runtime Test in Kubernetes

The service is accessed using port forwarding and the `/health` endpoint is tested.
This confirms that the application works after deployment.

### 5. Dummy DAST Stage

A simple placeholder stage represents Dynamic Application Security Testing.
This shows where runtime security testing would occur in a real production pipeline.

### 6. Verify Resources

Kubernetes resources are listed to confirm successful deployment.

---

## Security and Quality Built Into the Pipeline

This project does not treat security as an afterthought.

### Quality Controls

* Code linting keeps code clean
* Unit tests prevent bugs
* Runtime tests confirm correct behavior

### Security Controls

* CodeQL finds vulnerabilities in source code
* Trivy scans dependencies and container images

Security is enforced **before deployment**, not after.

---

## How to Run the Application Locally

### Prerequisites

* Python 3.11+
* Docker (optional)
* Minikube (optional, for Kubernetes testing)

### Run Without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Test:

```bash
curl http://localhost:8000/health
```

---

### Run Using Docker

```bash
docker build -t devsecops-fastapi .
docker run -p 8000:8000 devsecops-fastapi
```

Test:

```bash
curl http://localhost:8000/health
```

---

### Run on Kubernetes Locally

```bash
minikube start
kubectl apply -f k8s/
minikube service fastapi-service
```

---

## GitHub Secrets Configuration

To allow Docker image publishing, configure the following secrets in GitHub:

Go to:
**Repository → Settings → Secrets and variables → Actions**

Add:

| Secret Name        | Purpose                |
| ------------------ | ---------------------- |
| DOCKERHUB_USERNAME | DockerHub username     |
| DOCKERHUB_TOKEN    | DockerHub access token |

⚠️ Never hardcode secrets in workflow files or code.

---

## Repository Structure

```
project-root/
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
├── app/
│   └── main.py
├── tests/
│   └── test_api.py
├── k8s/
│   ├── deployment.yml
│   └── service.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Limitations and Future Improvements

### Current Limitations

* Uses Minikube instead of a cloud Kubernetes cluster
* No database
* Single environment only

### Possible Improvements

* Deploy to a cloud Kubernetes cluster
* Add monitoring and logging
* Add multiple environments (dev/staging/prod)
* Add full DAST using OWASP ZAP
* Improve secrets management

---
