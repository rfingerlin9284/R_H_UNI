# Personas and routing

This document describes how different assistant personas can be activated based on message content, objects, or tasks, and provides recommended patterns for this repository.

1) What is a persona?
- A persona is a focused behavior profile for the assistant (examples: "pair-programmer", "ops-runner", "security-auditor", "doc-writer").

2) Activation triggers
- Keyword-based: if a message contains words like "deploy", "run demo", "wire creds" -> activate "ops-runner".
- File-type/object-based: if the task edits code files -> "pair-programmer"; edits docs only -> "doc-writer".
- Task intent: if user asks to review security or secrets -> "security-auditor" (use stricter redaction rules).
- Manual override: user can explicitly request persona with "use persona: <name>".

3) Implementation patterns
- Router: preprocess incoming message to pick persona, set context flags (e.g., redact=true for security-auditor).
- Persona modules: small sets of rules and tone-of-voice templates used by the assistant when replying.

4) Recommendations for this project
- Default persona: "pair-programmer" for code edits and demos.
- Enable "ops-runner" for demo runs, CI edits, or deployment steps.
- Use "security-auditor" when handling credentials or redaction-sensitive work.

5) Notes and limits
- Persona selection should never bypass safety policies.
- Persona behaviour is enforced by assistant logic (e.g., use more cautious wording, require confirmations for destructive actions).
