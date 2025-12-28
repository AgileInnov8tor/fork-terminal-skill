---
title: Forked Session Context
type: conversation-summary
version: 1.0.0
---

# Forked Session Context

You are continuing work from a previous conversation session. Below is the summarized context from that session.

## Conversation History

{{conversation_history}}

## Summary of User's Request

{{summarized_user_prompt}}

## Summary of Assistant's Response

{{response_summary}}

## Current Working Directory

{{working_directory}}

## Relevant Files

{{#if relevant_files}}
{{#each relevant_files}}
- {{this}}
{{/each}}
{{else}}
_No specific files mentioned_
{{/if}}

## Key Decisions Made

{{#if key_decisions}}
{{#each key_decisions}}
- {{this}}
{{/each}}
{{else}}
_No key decisions documented_
{{/if}}

## Next Steps

{{next_steps}}

---

**Instructions**: Continue the work described above. You have full context from the previous session and should pick up where it left off.
