Feature: Plugin Architecture and Schema Validation
  As an internal marketplace maintainer
  I want to run a validation script on the plugin package
  So that I can verify all schemas, agents, and required files conform to standards.

  Scenario: Validate manifest and marketplace files parsing
    Given a plugin directory containing "plugin.json"
    And a marketplace metadata file ".github/plugin/marketplace.json"
    When the validation script executes
    Then "plugin.json" must parse as valid JSON
    And "plugin.json" must contain keys "id", "name", "version", "publisher", "agents", "skills"
    And ".github/plugin/marketplace.json" must parse as valid JSON

  Scenario: Validate skills frontmatter triggers
    Given a modular skill markdown file "SKILL.md"
    When the validation script parses "SKILL.md"
    Then the file must contain YAML frontmatter bounded by "---"
    And the frontmatter must contain attributes "name" and "description"
