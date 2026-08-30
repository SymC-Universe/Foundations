# Security Policy

This repository is primarily a scientific research archive and computational reproducibility project. Security reports are still welcome for repository automation, scripts, workflows, dependency handling, generated artifacts, or other software behavior that could expose credentials, execute untrusted code, corrupt evidence, or misrepresent provenance.

## Report privately when appropriate

Do not open a public issue containing:

- passwords, tokens, API keys, private keys, or other credentials;
- exploitable workflow or automation details that could compromise the repository or its users;
- private personal information;
- unpublished third-party confidential data.

Use GitHub's private security-reporting mechanisms if available for the repository. If private reporting is not available, contact the repository maintainer through the GitHub account associated with this project and provide only the minimum information needed to establish a private channel.

## Scientific errors are not security vulnerabilities

Mathematical mistakes, physical-model errors, incorrect citations, data-analysis defects, reproducibility failures, and interpretation concerns should normally use the scientific-correction or reproducibility issue templates rather than a private security report, unless public disclosure would itself expose sensitive information or an exploitable software weakness.

## Scope

Security-relevant repository components may include:

- GitHub Actions workflows;
- dependency installation and execution;
- scripts that read or write evidence-bearing files;
- provenance and hash validation;
- archive extraction;
- externally supplied input handling;
- branch or release automation.

## Response principles

A confirmed security problem should be corrected without changing frozen scientific assumptions unless the scientific impact is explicitly reviewed and recorded. If a vulnerability could have altered evidence, the affected computational results should be treated as held until integrity is re-established.
