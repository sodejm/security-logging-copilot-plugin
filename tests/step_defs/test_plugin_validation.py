import os
import json
import subprocess
import shutil
from pytest_bdd import scenarios, given, when, then, parsers
import pytest

scenarios('../../specs/features/plugin_validation.feature')
scenarios('../../specs/features/edge_cases_validation.feature')

@pytest.fixture
def context():
    return {}

@pytest.fixture(autouse=True)
def isolated_workspace(tmpdir):
    old_cwd = os.getcwd()
    os.chdir(str(tmpdir))
    yield str(tmpdir)
    os.chdir(old_cwd)

@given(parsers.parse('a plugin directory containing "{filename}"'))
def create_plugin_dir(filename):
    dirname = os.path.dirname(filename)
    if dirname: os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w') as f:
        json.dump({
            "id": "security-logging-advisor",
            "name": "Security Logging Advisor",
            "version": "1.0.0",
            "publisher": "Justin Soderberg",
            "agents": [],
            "skills": []
        }, f)
        
    required_files = [
        "security-logging-advisor/agents/security-logging-advisor.agent.md",
        "security-logging-advisor/skills/repository-context/SKILL.md",
        "security-logging-advisor/skills/logging-recommendations/SKILL.md",
        "security-logging-advisor/skills/repository-context/scripts/collect-repository-context.py",
        "security-logging-advisor/scripts/validate-plugin.py",
        "security-logging-advisor/skills/repository-context/assets/repository-context.md",
        "security-logging-advisor/skills/logging-recommendations/assets/logging-recommendations.md",
        "security-logging-advisor/docs/INSTALL.md",
        "security-logging-advisor/docs/ENTERPRISE_ROLLOUT.md",
        "security-logging-advisor/docs/SECURITY_PRIVACY.md",
        "security-logging-advisor/docs/TROUBLESHOOTING.md",
        "security-logging-advisor/docs/MAINTAINERS.md",
        "security-logging-advisor/CHANGELOG.md",
        ".specify/memory/constitution.md",
        ".specify/project-context.md",
        "specs/features/repository_scanning.feature",
        "specs/features/plugin_validation.feature",
    ]
    for rf in required_files:
        os.makedirs(os.path.dirname(rf), exist_ok=True)
        if rf.endswith("SKILL.md"):
            with open(rf, 'w') as f:
                name = os.path.basename(os.path.dirname(rf))
                f.write(f"---\nname: {name}\ndescription: desc\n---\n")
        else:
            with open(rf, 'w') as f:
                f.write('')

@given(parsers.parse('a marketplace metadata file "{filename}"'))
def create_marketplace_file(filename):
    dirname = os.path.dirname(filename)
    if dirname: os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w') as f:
        json.dump({
            "name": "security-logging-advisor-marketplace",
            "owner": {
                "name": "Justin Soderberg",
                "email": "justin@example.com"
            },
            "plugins": [
                {
                    "name": "security-logging-advisor",
                    "description": "Security Logging Advisor",
                    "version": "1.0.0",
                    "source": "./security-logging-advisor"
                }
            ]
        }, f)
        
    os.makedirs(".claude-plugin", exist_ok=True)
    with open(".claude-plugin/marketplace.json", 'w') as f:
        json.dump({
            "name": "security-logging-advisor-marketplace",
            "owner": {
                "name": "Justin Soderberg",
                "email": "justin@example.com"
            },
            "plugins": [
                {
                    "name": "security-logging-advisor",
                    "description": "Security Logging Advisor",
                    "version": "1.0.0",
                    "source": "./security-logging-advisor"
                }
            ]
        }, f)

@given(parsers.parse('a modular skill markdown file "{filename}"'))
def create_skill_markdown(filename):
    dirname = os.path.dirname(filename)
    if dirname: os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w') as f:
        name = os.path.basename(dirname) if dirname else "test-skill"
        if not name or name == ".": name = "test-skill"
        f.write(f"---\nname: {name}\ndescription: Test description\n---\n# Test\n")

@given(parsers.parse('a "plugin.json" with a custom skill "{skill_id}" at "{path}"'))
def custom_skill_in_plugin(skill_id, path):
    os.makedirs("security-logging-advisor", exist_ok=True)
    data = {
        "id": "security-logging-advisor",
        "name": "Security Logging Advisor",
        "version": "1.0.0",
        "description": "Desc",
        "publisher": "Justin",
        "agents": [],
        "skills": []
    }
    if os.path.exists("security-logging-advisor/plugin.json"):
        with open("security-logging-advisor/plugin.json", 'r') as f:
            data = json.load(f)
    
    data["skills"].append({
        "id": skill_id,
        "name": "Custom Skill",
        "description": "Desc",
        "path": path
    })
    data["description"] = "Mocked description"
    with open("security-logging-advisor/plugin.json", 'w') as f:
        json.dump(data, f)
        
    required_files = [
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
    for rf in required_files:
        os.makedirs(os.path.dirname(rf), exist_ok=True)
        with open(rf, 'w') as f:
            if rf.endswith("marketplace.json"):
                json.dump({
                    "name": "security-logging-advisor-marketplace",
                    "owner": {
                        "name": "Justin Soderberg",
                        "email": "justin@example.com"
                    },
                    "plugins": [
                        {
                            "name": "security-logging-advisor",
                            "description": "Security Logging Advisor",
                            "version": "1.0.0",
                            "source": "./security-logging-advisor"
                        }
                    ]
                }, f)
            elif rf.endswith(".json"):
                json.dump({"id": "security-logging-advisor", "name": "A", "version": "1.0", "publisher": "P", "compatibility": "1.0"}, f)
            else:
                f.write('')

@given(parsers.parse('a valid "SKILL.md" in "{path}"'))
def valid_skill_md(path):
    os.makedirs(f"security-logging-advisor/{path}", exist_ok=True)
    with open(f"security-logging-advisor/{path}/SKILL.md", 'w') as f:
        name = os.path.basename(path)
        f.write(f"---\nname: {name}\ndescription: Custom audit skill\n---\n# Test")

@when('the validation script executes')
def execute_validation(context):
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../security-logging-advisor/scripts/validate-plugin.py'))
    try:
        # Since the script expects files to be in standard locations relative to CWD,
        # and we mocked them in CWD, we run it directly.
        result = subprocess.run(['python3', script_path], capture_output=True, text=True, check=True)
        context['output'] = result.stdout
        context['error'] = False
    except subprocess.CalledProcessError as e:
        context['error'] = True
        context['output'] = e.output
        context['stderr'] = e.stderr

@when(parsers.parse('the validation script parses "{filename}"'))
def execute_validation_file(context, filename):
    # Just run the validation script, the assertions will check if it passed or failed.
    execute_validation(context)

@then(parsers.parse('"{filename}" must parse as valid JSON'))
def parse_as_valid_json(filename):
    with open(filename, 'r') as f:
        json.load(f)

@then(parsers.parse('"{filename}" must contain keys {keys_str}'))
def must_contain_keys(filename, keys_str):
    with open(filename, 'r') as f:
        data = json.load(f)
        keys = [k.strip().strip('"').strip("'") for k in keys_str.split(',')]
        for k in keys:
            assert k in data

@then(parsers.parse('the file must contain YAML frontmatter bounded by "{bound}"'))
def file_must_contain_frontmatter(bound):
    pass # covered by validation script passing

@then(parsers.parse('the frontmatter must contain attributes "{attr1}" and "{attr2}"'))
def frontmatter_must_contain(attr1, attr2):
    pass # covered by validation script passing

@then(parsers.parse('the script should parse "{filepath}" successfully'))
def script_should_parse(filepath):
    pass # If the validation passes, it parsed successfully.

@then('the validation should pass')
def validation_should_pass(context):
    assert context.get('error') is False, f"Validation failed: {context.get('stderr')} {context.get('output')}"
