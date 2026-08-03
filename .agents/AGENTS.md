# Custom Agent Rules

## GitHub CLI Tag and Release Management
- **Tag & Release**: Use the GitHub CLI (`gh release create <tag> --title "<tag>" --notes "<body_text>"`) or standard git commands (`git tag <tag> && git push origin <tag>`) to create tags and releases. Never store or embed personal access tokens in `.git/config` or remote URLs.

## GitHub Release Notes Format
- **Format**: When publishing releases on GitHub, the release description (`body`) must use the standard release notes format:
  - Uses `## What's Changed` as the primary section header.
  - Lists changed items using bullet points.
  - Starts each bullet point with a bold term describing the feature/fix (e.g. `**Feature Name**: Description...`).
  - Codes/symbols should be highlighted in backticks (e.g. `__del__`, `close()`).

## Critically Evaluate Audits and Suggestions
- **Rule**: When presented with an external code audit, linter warnings, or suggestions from other AI models, do **not** blindly apply all recommendations.
- **Action**: Critically evaluate each suggestion against the existing codebase's architecture and historical design choices. 
- **Pushback**: If an audit recommendation conflicts with an intentional design decision, seems unnecessary, or introduces regressions, you must push back. Do not apply the change, state your reasoning clearly to the user, and ask for confirmation before proceeding.

## Explain Before Code Changes
- **Rule**: Always explain clearly to the user what changes are being made and why **before** editing code or modifying files.
