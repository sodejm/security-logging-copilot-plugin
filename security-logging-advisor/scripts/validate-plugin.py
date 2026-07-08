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

REQUIRED_STATIC_FILES = [
    "security-logging-advisor/plugin.json",
    "security-logging-advisor/agents/security-logging-advisor.agent.md",
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

def check_marketplace_json(file_path):
    """Parses and validates marketplace.json according to CLI expectations."""
    if not os.path.isfile(file_path):
        return [f"File {file_path} is missing."]
    
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Check required top-level keys
            required_keys = ["name", "owner", "plugins"]
            for key in required_keys:
                if key not in data:
                    errors.append(f"{file_path} is missing required key: '{key}'")
            
            # Check owner is an object with a name
            if "owner" in data:
                if not isinstance(data["owner"], dict):
                    errors.append(f"{file_path} 'owner' must be an object (received {type(data['owner']).__name__})")
                else:
                    if "name" not in data["owner"]:
                        errors.append(f"{file_path} 'owner' is missing required subkey: 'name'")
            
            # Check plugins is a list of objects
            if "plugins" in data:
                if not isinstance(data["plugins"], list):
                    errors.append(f"{file_path} 'plugins' must be a list (received {type(data['plugins']).__name__})")
                else:
                    for i, plugin in enumerate(data["plugins"]):
                        if not isinstance(plugin, dict):
                            errors.append(f"{file_path} 'plugins[{i}]' must be an object")
                        else:
                            plugin_keys = ["name", "description", "version", "source"]
                            for pk in plugin_keys:
                                if pk not in plugin:
                                    errors.append(f"{file_path} 'plugins[{i}]' is missing required key: '{pk}'")
    except json.JSONDecodeError as e:
        errors.append(f"Failed to parse {file_path} as JSON: {str(e)}")
    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")
        
    return errors

def check_skill_markdown(file_path):
    """Validates that a SKILL.md file has a valid YAML frontmatter adhering to the agentskills.io spec."""
    if not os.path.isfile(file_path):
        return [f"File {file_path} is missing."]
    
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Match standard YAML block bounded by ---
        match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
        if not match:
            errors.append(f"Skill file {file_path} does not contain standard YAML frontmatter bounded by ---")
            return errors
        
        frontmatter_text = match.group(1)
        lines = frontmatter_text.splitlines()
        yaml_data = {}
        in_metadata = False
        metadata_dict = {}
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            
            # Check indentation
            indent = len(line) - len(line.lstrip())
            
            if in_metadata:
                if indent > 0:
                    meta_match = re.match(r"^([\w-]+):\s*(.+)$", stripped)
                    if meta_match:
                        k, v = meta_match.group(1), meta_match.group(2).strip()
                        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                            v = v[1:-1]
                        metadata_dict[k] = v
                    else:
                        errors.append(f"Skill file {file_path}: Invalid metadata entry at line {line_num}: '{line}'")
                    continue
                else:
                    in_metadata = False
                    yaml_data["metadata"] = metadata_dict
            
            kv_match = re.match(r"^([\w-]+):\s*(.*)$", stripped)
            if not kv_match:
                errors.append(f"Skill file {file_path}: Invalid frontmatter YAML syntax at line {line_num}: '{line}'")
                continue
                
            key, val = kv_match.group(1), kv_match.group(2).strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
                
            if key == "metadata":
                if val == "":
                    in_metadata = True
                    metadata_dict = {}
                else:
                    errors.append(f"Skill file {file_path}: metadata field must start a nested dictionary block")
            else:
                yaml_data[key] = val
                
        if in_metadata:
            yaml_data["metadata"] = metadata_dict
            
        # Validate name
        if "name" not in yaml_data:
            errors.append(f"Skill file {file_path} frontmatter is missing 'name'")
        else:
            name = yaml_data["name"]
            if not (1 <= len(name) <= 64):
                errors.append(f"Skill file {file_path} 'name' length must be between 1 and 64 characters (current length: {len(name)})")
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
                errors.append(f"Skill file {file_path} 'name' ('{name}') must only contain lowercase alphanumeric characters and hyphens, and must not start, end, or have consecutive hyphens")
            
            parent_dir = os.path.basename(os.path.dirname(file_path))
            if name != parent_dir:
                errors.append(f"Skill file {file_path} 'name' ('{name}') must match the parent directory name ('{parent_dir}')")
                
        # Validate description
        if "description" not in yaml_data:
            errors.append(f"Skill file {file_path} frontmatter is missing 'description'")
        else:
            description = yaml_data["description"]
            if not (1 <= len(description) <= 1024):
                errors.append(f"Skill file {file_path} 'description' length must be between 1 and 1024 characters (current length: {len(description)})")
                
        # Validate optional fields
        valid_keys = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        for key in yaml_data:
            if key not in valid_keys:
                errors.append(f"Skill file {file_path} frontmatter contains invalid/unknown key: '{key}'")
                
        if "compatibility" in yaml_data:
            compatibility = yaml_data["compatibility"]
            if not (1 <= len(compatibility) <= 500):
                errors.append(f"Skill file {file_path} 'compatibility' length must be between 1 and 500 characters (current length: {len(compatibility)})")
                
        if "metadata" in yaml_data:
            meta = yaml_data["metadata"]
            if not isinstance(meta, dict):
                errors.append(f"Skill file {file_path} 'metadata' must be a key-value mapping")
            else:
                for k, v in meta.items():
                    if not isinstance(k, str) or not isinstance(v, str):
                        errors.append(f"Skill file {file_path} 'metadata' entry ('{k}': '{v}') must have string keys and values")
                        
    except Exception as e:
        errors.append(f"Error reading skill file {file_path}: {str(e)}")
        
    return errors

def main():
    print("Starting plugin verification and validation...")
    errors = []
    
    # 1. Check static file existence
    for path in REQUIRED_STATIC_FILES:
        if not os.path.exists(path):
            errors.append(f"Missing required file/path: {path}")
            
    # 2. Validate manifest json schema
    plugin_manifest = "security-logging-advisor/plugin.json"
    plugin_keys = ["id", "name", "version", "description", "publisher", "agents", "skills"]
    errors.extend(check_json_file(plugin_manifest, plugin_keys))
    
    # 3. Validate GitHub marketplace metadata schema
    gh_marketplace = ".github/plugin/marketplace.json"
    errors.extend(check_marketplace_json(gh_marketplace))
    
    # 4. Validate Claude marketplace metadata schema
    claude_marketplace = ".claude-plugin/marketplace.json"
    errors.extend(check_marketplace_json(claude_marketplace))
    
    # 5. Dynamically validate skill markdown frontmatter based on plugin.json
    skills = []
    if os.path.exists(plugin_manifest):
        try:
            with open(plugin_manifest, "r", encoding="utf-8") as f:
                data = json.load(f)
                for skill in data.get("skills", []):
                    path = skill.get("path")
                    if path:
                        skills.append(f"security-logging-advisor/{path}/SKILL.md")
        except Exception as e:
            errors.append(f"Could not parse plugin.json to find skills: {e}")
            
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
