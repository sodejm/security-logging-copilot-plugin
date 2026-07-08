Feature: Plugin Validation Edge Cases
  As an internal marketplace maintainer
  I want the validation script to dynamically read plugin.json
  So that newly added skills are automatically validated without hardcoded paths.

  Scenario: Dynamic validation of custom skills
    Given a "plugin.json" with a custom skill "custom-audit" at "skills/custom-audit"
    And a valid "SKILL.md" in "skills/custom-audit"
    When the validation script executes
    Then the script should parse "skills/custom-audit/SKILL.md" successfully
    And the validation should pass
