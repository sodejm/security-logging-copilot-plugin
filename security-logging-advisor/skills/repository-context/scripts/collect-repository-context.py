#!/usr/bin/env python3
"""
collect-repository-context.py
Enterprise Security Logging Advisor - Repository Scanner

Scans a repository to identify languages, frameworks, IaC config, databases,
authentication mechanisms, CI/CD configurations, and potential secrets patterns.
Outputs findings as a structured JSON object.
"""

import os
import sys
import json
import re

# Directory and file ignore patterns
IGNORE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "dist", "build", "target", 
    ".gemini", "__pycache__", ".pytest_cache", ".mypy_cache", ".idea"
}

# Regex patterns for secret detection (high-confidence only)
SECRETS_PATTERNS = {
    "AWS Access Key ID": re.compile(r"([^A-Z0-9]|^)(AKIA[A-Z0-9]{16})([^A-Z0-9]|$)"),
    "Generic Secret / Password Assignment": re.compile(
        r"(?i)(password|passwd|secret|api[-_]?key|private[-_]?key|auth[-_]?token)\s*[:=]\s*['\"][a-zA-Z0-9_\-\.\/\+\=\!@#\$%\^&\*\(\)]{8,}['\"]"
    ),
    "Private Key Header": re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
    "Database Connection String": re.compile(r"(mongodb(?:\+srv)?|postgres|mysql|redis):\/\/[a-zA-Z0-9_]+:[^@]+@[a-zA-Z0-9_\-\.]+"),
}

def is_ignored(path, root_dir):
    """Checks if a given path should be ignored."""
    parts = os.path.relpath(path, root_dir).split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    return False

def scan_repository(root_dir):
    """Performs static analysis on the repository files."""
    results = {
        "repository_path": os.path.abspath(root_dir),
        "languages": {},
        "frameworks_and_libraries": [],
        "databases": [],
        "identity_and_auth": [],
        "iac_and_cloud": [],
        "cicd": [],
        "secrets_findings": [],
        "scanned_files_count": 0
    }

    # Configuration file detections
    for root, dirs, files in os.walk(root_dir):
        if is_ignored(root, root_dir):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            results["scanned_files_count"] += 1

            # Language and core tech detection
            ext = os.path.splitext(file)[1].lower()
            if ext in {".ts", ".tsx", ".js", ".jsx"}:
                results["languages"]["TypeScript/JavaScript"] = results["languages"].get("TypeScript/JavaScript", 0) + 1
            elif ext == ".py":
                results["languages"]["Python"] = results["languages"].get("Python", 0) + 1
            elif ext == ".go":
                results["languages"]["Go"] = results["languages"].get("Go", 0) + 1
            elif ext == ".java":
                results["languages"]["Java"] = results["languages"].get("Java", 0) + 1
            elif ext in {".tf", ".tfvars"}:
                results["languages"]["HashiCorp Configuration Language (HCL)"] = results["languages"].get("HashiCorp Configuration Language (HCL)", 0) + 1
                if "Terraform" not in results["iac_and_cloud"]:
                    results["iac_and_cloud"].append("Terraform")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "aws_" in content:
                            if "AWS" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("AWS")
                        if "google_" in content:
                            if "GCP" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("GCP")
                        if "azurerm_" in content or "azure_" in content:
                            if "Azure" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("Azure")
                        if "oci_" in content:
                            if "Oracle Cloud" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("Oracle Cloud")
                except Exception:
                    pass
            elif ext == ".bicep":
                results["languages"]["Bicep"] = results["languages"].get("Bicep", 0) + 1
                if "Azure Bicep" not in results["iac_and_cloud"]:
                    results["iac_and_cloud"].append("Azure Bicep")
            elif ext in {".ps1", ".psm1"}:
                results["languages"]["PowerShell"] = results["languages"].get("PowerShell", 0) + 1
            elif ext == ".sh":
                results["languages"]["Shell Script (Bash)"] = results["languages"].get("Shell Script (Bash)", 0) + 1
            elif ext in {".pl", ".pm"}:
                results["languages"]["Perl"] = results["languages"].get("Perl", 0) + 1
            elif ext in {".cs", ".csproj", ".sln"}:
                results["languages"]["C# (.NET)"] = results["languages"].get("C# (.NET)", 0) + 1
            elif ext == ".json":
                # Check for ARM template schema
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        header = f.read(1024)
                        if "schema.management.azure.com" in header:
                            if "Azure ARM Template" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("Azure ARM Template")
                except Exception:
                    pass

            # Project manifests & dependencies detection
            if file == "package.json":
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        data = json.load(f)
                        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                        # Scan dependencies for libraries
                        for dep in deps:
                            if dep in {"express", "koa", "nest", "fastify"}:
                                results["frameworks_and_libraries"].append(f"Node.js Framework: {dep}")
                            if dep in {"pg", "mysql2", "mongoose", "redis", "ioredis", "sequelize", "typeorm"}:
                                results["databases"].append(f"Node.js DB Client: {dep}")
                            if dep in {"jsonwebtoken", "passport", "auth0", "keycloak-connect", "firebase-admin"}:
                                results["identity_and_auth"].append(f"Node.js Auth: {dep}")
                            if dep in {"winston", "pino", "bunyan", "morgan"}:
                                results["frameworks_and_libraries"].append(f"Logging Library: {dep}")
                            if "aws-sdk" in dep or "@aws-sdk" in dep:
                                if "AWS" not in results["iac_and_cloud"]:
                                    results["iac_and_cloud"].append("AWS")
                            if "google-cloud" in dep or "@google-cloud" in dep:
                                if "GCP" not in results["iac_and_cloud"]:
                                    results["iac_and_cloud"].append("GCP")
                            if "azure" in dep or "@azure" in dep:
                                if "Azure" not in results["iac_and_cloud"]:
                                    results["iac_and_cloud"].append("Azure")
                            if "oci" in dep:
                                if "Oracle Cloud" not in results["iac_and_cloud"]:
                                    results["iac_and_cloud"].append("Oracle Cloud")
                except Exception:
                    pass

            elif file == "requirements.txt" or file == "Pipfile" or file == "pyproject.toml":
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "django" in content.lower():
                            results["frameworks_and_libraries"].append("Python Framework: Django")
                        if "flask" in content.lower():
                            results["frameworks_and_libraries"].append("Python Framework: Flask")
                        if "fastapi" in content.lower():
                            results["frameworks_and_libraries"].append("Python Framework: FastAPI")
                        if "sqlalchemy" in content.lower() or "psycopg2" in content.lower() or "pymongo" in content.lower() or "redis" in content.lower():
                            results["databases"].append("Python DB Client")
                        if "jwt" in content.lower() or "oauth" in content.lower() or "auth0" in content.lower():
                            results["identity_and_auth"].append("Python Auth Library")
                        if "structlog" in content.lower():
                            results["frameworks_and_libraries"].append("Logging Library: structlog")
                        if "boto3" in content.lower() or "aws" in content.lower():
                            if "AWS" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("AWS")
                        if "google-cloud" in content.lower():
                            if "GCP" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("GCP")
                        if "azure" in content.lower():
                            if "Azure" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("Azure")
                        if "oci" in content.lower():
                            if "Oracle Cloud" not in results["iac_and_cloud"]:
                                results["iac_and_cloud"].append("Oracle Cloud")
                except Exception:
                    pass

            # IaC, Containers and Configs
            if file == "Dockerfile":
                results["iac_and_cloud"].append("Docker containerization")
            elif file == "docker-compose.yml" or file == "docker-compose.yaml":
                results["iac_and_cloud"].append("Docker Compose orchestration")
            elif file == "Chart.yaml":
                results["iac_and_cloud"].append("Kubernetes Helm Chart")
            elif "kubernetes" in root.lower() or file == "deployment.yaml" or file == "deployment.yml":
                if "Kubernetes YAML" not in results["iac_and_cloud"]:
                    results["iac_and_cloud"].append("Kubernetes YAML definitions")

            # CI/CD pipelines
            if ".github/workflows" in root:
                if "GitHub Actions" not in results["cicd"]:
                    results["cicd"].append("GitHub Actions")
            elif ".gitlab-ci.yml" in file:
                results["cicd"].append("GitLab CI")
            elif "Jenkinsfile" in file:
                results["cicd"].append("Jenkins Pipeline")

            # File scanning for credentials (text files only)
            if ext in {".json", ".yaml", ".yml", ".tf", ".conf", ".properties", ".ini", ".env", ".py", ".ts", ".js", ".go", ".java", ".md", ".bicep", ".ps1", ".psm1", ".sh", ".pl", ".pm", ".cs", ".csproj", ".sln"}:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            for name, pattern in SECRETS_PATTERNS.items():
                                if pattern.search(line):
                                    # Masked alert log entry
                                    results["secrets_findings"].append({
                                        "file": rel_path,
                                        "line": line_num,
                                        "issue_type": f"Potential {name} detected",
                                        "remediation": "Do not commit plain text secrets. Move key/credentials to vault/secrets manager or set as environment variables."
                                    })
                except Exception:
                    pass

    return results

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(target_dir):
        print(json.dumps({"error": f"Path '{target_dir}' is not a valid directory."}, indent=2))
        sys.exit(1)

    scan_data = scan_repository(target_dir)
    print(json.dumps(scan_data, indent=2))

if __name__ == "__main__":
    main()
