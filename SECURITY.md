# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT open a public GitHub issue.**
2. Email your findings to the repository maintainers via the contact information on the [yao-care organization profile](https://github.com/yao-care).
3. Include a description of the vulnerability, steps to reproduce, and potential impact.

We will acknowledge your report within 72 hours and work to address confirmed vulnerabilities promptly.

## Scope

This project provides **research-only** drug repurposing predictions. It does not process or store protected health information (PHI). The SMART on FHIR integration operates as a client-side application and does not persist any patient data.

## Security Measures

- All external CDN scripts include Subresource Integrity (SRI) hashes.
- The SMART on FHIR app uses OAuth 2.0 with PKCE for authorization.
- No secrets or credentials are stored in the repository.
- Python dependencies are locked via `uv.lock` (managed by [uv](https://docs.astral.sh/uv/)).
- Ruby/Jekyll dependencies are locked via `docs/Gemfile.lock` (managed by Bundler).
- This project does not use npm or any JavaScript package manager — all client-side scripts are loaded from CDN with SRI hashes or vendored directly.
