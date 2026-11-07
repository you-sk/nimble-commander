# Nimble Commander Japanese Fork

## Project goal
Create a Japanese-localized and usability-improved
fork of Nimble Commander for macOS.

Upstream:
https://github.com/mikekazakov/nimble-commander

## Core policies
- Preserve the upstream Git history.
- Preserve GPL-3.0 licensing and copyright notices.
- Keep the existing dual-pane file manager architecture.
- Prefer incremental changes over large rewrites.
- Support both Japanese and English interfaces.
- Preserve existing functionality unless explicitly changed.
- Never commit credentials, signing keys, personal data,
  local machine paths, or generated build artifacts.
- Never modify unrelated repositories.
- Never use sudo without explicit approval.
- Do not create releases or publish binaries without approval.

## GitHub workflow
- Use GitHub CLI (gh) for authentication and forking.
- Create a public fork under the authenticated user.
- Keep upstream configured as a Git remote.
- Work in feature branches.
- Commit logical, independently reviewable changes.
- Push only to the user's fork.
- Never push to upstream.
- Do not create pull requests to upstream automatically.

## Development priorities
1. Establish a reproducible baseline build.
2. Analyze existing localization and keyboard support.
3. Add Japanese localization.
4. Improve keyboard-driven file operations.
5. Improve path visibility and navigation.
6. Improve multi-file operations.

## Quality requirements
- Inspect existing implementations before adding features.
- Document assumptions and limitations.
- Run relevant tests for every change.
- Record build and test results.
- Do not claim success without verification.
- Do not silently change file operation semantics.
- Test destructive file operations only on temporary fixtures.
