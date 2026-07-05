# Specification: Security Logging Advisor Plugin

This document outlines the requirements, user stories, and acceptance criteria for the **Security Logging Advisor** plugin. It serves as the single source of truth for the plugin's features and technical scope.

---

## 1. Goal & Intent
Provide software development teams with an automated, cost-conscious, and security-first advisor that audits a codebase's framework footprint and generates direct, actionable recommendations to improve security audit logging posture.

---

## 2. User Stories

- **As a Developer**, I want to scan my repository so that I know what logging packages and configurations are missing or insecure.
- **As a Security Engineer**, I want the advisor to verify that logging statements include critical fields (correlation IDs, timestamps, actor references) without writing sensitive variables to logs.
- **As a Platform Administrator**, I want to deploy this tool organization-wide and ensure developers have cost-aware settings that prevent budget overflows in our SIEM ingestion.

---

## 3. Functional Requirements

### A. Repository Context Scanning
- **Supported Languages**: Auto-detect files and analyze code patterns for:
  - TypeScript / JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`)
  - Python (`.py`)
  - Go (`.go`)
  - Java (`.java`)
  - HashiCorp Configuration Language / HCL (`.tf`, `.tfvars`)
  - Bicep (`.bicep`)
  - PowerShell (`.ps1`, `.psm1`)
  - Shell Script / Bash (`.sh`)
  - Perl (`.pl`, `.pm`)
  - C# / .NET / dotnet (`.cs`, `.csproj`, `.sln`)
- **Supported Cloud & IaC Detections**: Scan configuration, packages, and infra files to identify:
  - **AWS**: Amazon Web Services (via HCL, Docker base, or NPM/pip dependencies)
  - **GCP**: Google Cloud Platform (via HCL, NPM/pip dependencies)
  - **Azure**: Microsoft Azure (via Bicep, ARM templates, HCL, or dependencies)
  - **Oracle Cloud**: Oracle Cloud Infrastructure / OCI (via HCL, NPM/pip dependencies)
- **IaC & Containers**: Detect Docker, Kubernetes, Helm, and Terraform indicators.
- **Data Zones**: Map databases (Redis, Postgres, Mongo) and authentication providers.
- **Secrets Audit**: Scan config files for credentials, reporting their file and line locations while strictly redacting/hiding the credential values.

### B. Logging Recommendation System
- **Tiered Telemetry**: Recommend distinct tiers for Sandbox (low budget, minimal logs), Development (debug support), and Production (structured format, SIEM ingestion).
- **Format Advice**: Direct the implementation of structured JSON logs with correlation IDs.
- **Alerting Guidance**: Suggest triage rules and alarm criteria for high-priority security failures.

### C. Plugin Validation
- Verify JSON formatting of the plugin manifests (`plugin.json`, `marketplace.json`).
- Ensure all required docs, example templates, and scripts are present in the package before release.

---

## 4. Technical Constraints & Security Boundaries
- **Local Boundary**: All scanning logic must run locally to protect intellectual property. Code contents must not be sent to external hosts.
- **License Compliance**: The software must execute under the **PolyForm Noncommercial License 1.0.0**, blocking use in commercial products.
- **Zero-Dependency Core**: Validation and scanning scripts must run using standard libraries in Python 3.

---

## 5. Acceptance Criteria
- [ ] Running `validate-plugin.py` returns code `0` on compliant packages.
- [ ] Running `collect-repository-context.py` yields a complete JSON map of the codebase without listing any hardcoded credential values.
- [ ] The generated report matches the fields laid out in the recommendations markdown template.
