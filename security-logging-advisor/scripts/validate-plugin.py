#!/usr/bin/env python3
"""
validate-plugin.py
Enterprise Security Logging Advisor - Plugin Schema and Structure Validator

Checks the directory layout, manifest JSON files, skill markdown frontmatters,
and documentation presence to ensure the plugin package is valid for internal marketplace distribution.
"""

import os
import sys
import json
import re

REQUIRED_FILES = [
    "security-logging-advisor/plugin.json",
    "security-logging-advisor/agents/security-logging-advisor.agent.md",
    "security-logging-advisor/skills/repository-context/SKILL.md",
    "security-logging-advisor/skills/logging-recommendations/SKILL.md",
    "security-logging-advisor/scripts/collect-repository-context.py",
    "security-logging-advisor/scripts/validate-plugin.py",
    "security-logging-advisor/templates/repository-context.md",
    "security-logging-advisor/templates/logging-recommendations.md",
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
]

def check_json_file(file_path, required_keys):
    """Parses JSON file and checks for existence of required keys."""
    if not os.path.isfile(file_path):
        return [f"File {file_path} is missing."]
    
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in required_keys:
                if key not in data:
                    errors.append(f"{file_path} is missing key: '{key}'")
    except json.JSONDecodeError as e:
        errors.append(f"Failed to parse {file_path} as JSON: {str(e)}")
    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")
    
    return errors

def check_skill_markdown(file_path):
    """Validates that a SKILL.md file has a valid YAML frontmatter containing 'name' and 'description'."""
    if not os.path.isfile(file_path):
        return [f"File {file_path} is missing."]
    
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Frontmatter regex: matches standard YAML block bounded by ---
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if not match:
                errors.append(f"Skill file {file_path} does not contain standard YAML frontmatter bounded by ---")
                return errors
            
            frontmatter_text = match.group(1)
            name_match = re.search(r"^name:\s*(.+)$", frontmatter_text, re.MULTILINE)
            desc_match = re.search(r"^description:\s*(.+)$", frontmatter_text, re.MULTILINE)
            
            if not name_match:
                errors.append(f"Skill file {file_path} frontmatter is missing 'name'")
            if not desc_match:
                errors.append(f"Skill file {file_path} frontmatter is missing 'description'")
    except Exception as e:
        errors.append(f"Error reading skill file {file_path}: {str(e)}")
        
    return errors

def main():
    print("Starting plugin verification and validation...")
    errors = []
    
    # 1. Check file existence
    for path in REQUIRED_FILES:
        if not os.path.exists(path):
            errors.append(f"Missing required file/path: {path}")
            
    # 2. Validate manifest json schema
    plugin_manifest = "security-logging-advisor/plugin.json"
    plugin_keys = ["id", "name", "version", "description", "publisher", "agents", "skills"]
    errors.extend(check_json_file(plugin_manifest, plugin_keys))
    
    # 3. Validate GitHub marketplace metadata schema
    gh_marketplace = ".github/plugin/marketplace.json"
    gh_keys = ["id", "name", "version", "publisher", "compatibility"]
    errors.extend(check_json_file(gh_marketplace, gh_keys))
    
    # 4. Validate Claude marketplace metadata schema
    claude_marketplace = ".claude-plugin/marketplace.json"
    claude_keys = ["id", "name", "version", "compatibility"]
    errors.extend(check_json_file(claude_marketplace, claude_keys))
    
    # 5. Validate skill markdown frontmatter
    skills = [
        "security-logging-advisor/skills/repository-context/SKILL.md",
        "security-logging-advisor/skills/logging-recommendations/SKILL.md"
    ]
    for skill in skills:
        errors.extend(check_skill_markdown(skill))
        
    if errors:
        print("\nValidation failed with errors:")
        for err in errors:
            print(f" - [ERROR] {err}")
        sys.exit(1)
        
    print("\nAll checks passed successfully! Plugin structure, manifests, and frontmatters are valid.")

if __name__ == "__main__":
    main()
