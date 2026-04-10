---
description: Orchestrator Delegation Workflow
---

# 🔱 Orchestrator Delegation Workflow

This workflow defines how the **Orchestrator Integrator Master** handles complex tasks by decomposing them and delegating to specialized subagents.

## 1. Task Decomposition
Break down the main USER_REQUEST into atomic subtasks:
- **Research**: Scavenging data from external sources.
- **Engineering**: Writing code or configuring tools.
- **Verification**: Testing and validating results.

## 2. Team Assignment
Assign tasks to the appropriate team:
- `Team Research` -> Data extraction and synthesis.
- `Team Engineering` -> Implementation and MCP config.
- `Team Deployment` -> Syncing and automation.

## 3. Parallel Execution
// turbo
Run parallel subagents for independent tasks (e.g., research and environment setup).

## 4. Context Synthesis
Collect subagent outputs and synthesize them into the final response or the `MASTER_THESIS_HUB_V4.md`.

## 5. Verification & Review
// turbo
Run verification skills (e.g., `local_mesh_connector.py`) before completing the task.
