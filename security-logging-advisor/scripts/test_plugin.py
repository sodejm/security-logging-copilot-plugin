#!/usr/bin/env python3
"""
test_plugin.py
Automated test suite for Security Logging Advisor plugin validation and scanning capabilities.
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import unittest

# Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VALIDATE_SCRIPT = os.path.join(REPO_ROOT, "security-logging-advisor", "scripts", "validate-plugin.py")
SCAN_SCRIPT = os.path.join(REPO_ROOT, "security-logging-advisor", "skills", "repository-context", "scripts", "collect-repository-context.py")

class TestPluginValidation(unittest.TestCase):
    """Verifies features defined in specs/features/plugin_validation.feature"""

    def test_manifest_and_marketplace_parsing_success(self):
        """Runs the validation script on the current valid repository structure."""
        res = subprocess.run(
            [sys.executable, VALIDATE_SCRIPT],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Validator failed: {res.stderr}\nStdout: {res.stdout}")
        self.assertIn("All checks passed successfully", res.stdout)

    def test_validation_fails_on_missing_files(self):
        """Checks that validation fails and reports errors when files are missing or broken."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run validate-plugin from a directory with no files
            res = subprocess.run(
                [sys.executable, VALIDATE_SCRIPT],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            # It should fail because required files like security-logging-advisor/plugin.json are missing
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("Validation failed with errors", res.stdout)
            self.assertIn("Missing required file/path", res.stdout)

    def test_validation_fails_on_invalid_skill_frontmatter(self):
        """Checks that validator catches bad frontmatter formats in SKILL.md files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Recreate partial repo structure in temp_dir
            plugin_dir = os.path.join(temp_dir, "security-logging-advisor")
            os.makedirs(os.path.join(plugin_dir, "scripts"))
            os.makedirs(os.path.join(plugin_dir, "agents"))
            os.makedirs(os.path.join(plugin_dir, "docs"))
            os.makedirs(os.path.join(plugin_dir, "skills", "repository-context", "scripts"))
            os.makedirs(os.path.join(plugin_dir, "skills", "repository-context", "assets"))
            os.makedirs(os.path.join(plugin_dir, "skills", "logging-recommendations", "assets"))
            os.makedirs(os.path.join(temp_dir, ".github", "plugin"))
            os.makedirs(os.path.join(temp_dir, ".claude-plugin"))
            os.makedirs(os.path.join(temp_dir, ".specify", "memory"))
            os.makedirs(os.path.join(temp_dir, "specs", "features"))

            # Create mock versions of all required files
            for path in [
                "security-logging-advisor/plugin.json",
                "security-logging-advisor/agents/security-logging-advisor.agent.md",
                "security-logging-advisor/skills/repository-context/scripts/collect-repository-context.py",
                "security-logging-advisor/skills/repository-context/assets/repository-context.md",
                "security-logging-advisor/skills/logging-recommendations/assets/logging-recommendations.md",
                "security-logging-advisor/docs/INSTALL.md",
                "security-logging-advisor/docs/ENTERPRISE_ROLLOUT.md",
                "security-logging-advisor/docs/SECURITY_PRIVACY.md",
                "security-logging-advisor/docs/TROUBLESHOOTING.md",
                "security-logging-advisor/docs/MAINTAINERS.md",
                "security-logging-advisor/CHANGELOG.md",
                ".github/plugin/marketplace.json",
                ".claude-plugin/marketplace.json",
                ".specify/memory/constitution.md",
                ".specify/project-context.md",
                "specs/features/repository_scanning.feature",
                "specs/features/plugin_validation.feature",
            ]:
                full_path = os.path.join(temp_dir, path)
                if path.endswith(".json"):
                    with open(full_path, "w") as f:
                        if "plugin.json" in path:
                            json.dump({
                                "id": "test",
                                "name": "test",
                                "version": "1.0.0",
                                "description": "test desc",
                                "publisher": "test",
                                "agents": [],
                                "skills": [
                                    {"id": "repository-context", "name": "test", "description": "test", "path": "skills/repository-context"},
                                    {"id": "logging-recommendations", "name": "test", "description": "test", "path": "skills/logging-recommendations"}
                                ]
                            }, f)
                        else:
                            json.dump({
                                "name": "test-marketplace",
                                "owner": {
                                    "name": "test-owner",
                                    "email": "test@example.com"
                                },
                                "plugins": [
                                    {
                                        "name": "test-plugin",
                                        "description": "test description",
                                        "version": "1.0.0",
                                        "source": "./test-plugin"
                                    }
                                ]
                            }, f)
                else:
                    with open(full_path, "w") as f:
                        f.write("mock content")

            # Copy validate-plugin.py to temp structure
            shutil.copy(VALIDATE_SCRIPT, os.path.join(plugin_dir, "scripts", "validate-plugin.py"))

            # Write invalid SKILL.md for repository-context (missing description attribute)
            with open(os.path.join(plugin_dir, "skills", "repository-context", "SKILL.md"), "w") as f:
                f.write("---\nname: repository-context\n# missing description\n---\nbody")

            with open(os.path.join(plugin_dir, "skills", "logging-recommendations", "SKILL.md"), "w") as f:
                f.write("---\nname: logging-recommendations\ndescription: test desc\n---\nbody")

            # Run validator from temp_dir
            res = subprocess.run(
                [sys.executable, os.path.join(plugin_dir, "scripts", "validate-plugin.py")],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("frontmatter is missing 'description'", res.stdout)


class TestRepositoryScanning(unittest.TestCase):
    """Verifies features defined in specs/features/repository_scanning.feature"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def run_scanner(self):
        res = subprocess.run(
            [sys.executable, SCAN_SCRIPT, self.temp_dir],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Scanner failed: {res.stderr}")
        return json.loads(res.stdout)

    def test_detect_technology_and_cloud_from_hcl(self):
        """Scenario: Detect technology stack and cloud platform from HCL configuration"""
        # Create a Terraform file main.tf referencing aws provider
        tf_content = """
        provider "aws" {
          region = "us-east-1"
        }
        resource "aws_s3_bucket" "b" {
          bucket = "my-tf-test-bucket"
        }
        """
        with open(os.path.join(self.temp_dir, "main.tf"), "w") as f:
            f.write(tf_content)

        output = self.run_scanner()
        
        # Verify languages
        self.assertIn("HashiCorp Configuration Language (HCL)", output["languages"])
        # Verify cloud / iac
        self.assertIn("AWS", output["iac_and_cloud"])
        self.assertIn("Terraform", output["iac_and_cloud"])

    def test_prevent_credential_leakage(self):
        """Scenario: Prevent credential leakage in scanner output"""
        secret_val = "SuperSecretPassword123!"
        env_content = f"db_password = '{secret_val}'\n"
        with open(os.path.join(self.temp_dir, "config.env"), "w") as f:
            f.write(env_content)

        output = self.run_scanner()

        # Check secrets findings lists config.env
        findings = output["secrets_findings"]
        self.assertTrue(len(findings) > 0, "No secrets findings detected")
        
        finding = findings[0]
        self.assertEqual(finding["file"], "config.env")
        self.assertIn("remediation", finding)
        self.assertIn("vault", finding["remediation"].lower())

        # Ensure raw secret is not leaked in output json
        output_str = json.dumps(output)
        self.assertNotIn(secret_val, output_str)

    def test_detect_multi_language_and_cloud_indicators(self):
        """Scenario: Detect multi-language and Cloud provider indicators"""
        # Create a Bicep file
        with open(os.path.join(self.temp_dir, "deploy.bicep"), "w") as f:
            f.write("// Bicep deployments")

        # Create package.json with dependency "aws-sdk"
        package_json = {
            "dependencies": {
                "aws-sdk": "^2.1000.0"
            }
        }
        with open(os.path.join(self.temp_dir, "package.json"), "w") as f:
            json.dump(package_json, f)

        output = self.run_scanner()

        self.assertIn("Bicep", output["languages"])
        self.assertIn("Azure Bicep", output["iac_and_cloud"])
        self.assertIn("AWS", output["iac_and_cloud"])


if __name__ == "__main__":
    unittest.main()
