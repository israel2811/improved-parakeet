---
name: Research Synthesis Skill
description: Synthesizes data from Perplexity, NotebookLM, and Scholar into the Master Thesis Hub.
---

# Research Synthesis Skill

This skill is used by **Team Research** to synthesize harvested data into the unified thesis context.

## 📋 Instructions
1. Read the input files from `omni_harvest/` or the Bridge Server.
2. Filter for APA 7 relevant citations.
3. Compare against existing entries in `MASTER_THESIS_HUB_V3.md`.
4. Append new insights to the scratchpad or the next version of the hub.

## 🛠️ Tools
- `read_url_content`: For cross-referencing online sources.
- `grep_search`: To avoid duplicate entries.
- `multi_replace_file_content`: To update the Master Hub.

## 🔄 Workflow
1. **Ingest**: Read raw harvested data.
2. **De-duplicate**: Check if the topic exists.
3. **Format**: Convert to APA 7 style.
4. **Append**: Update the Master Thesis Hub.
