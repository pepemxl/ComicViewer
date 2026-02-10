---
name: license-header-adder
description: Adds the standard corporate license header to new source files.
---

# License Header Adder

This skill ensures that all new source files have the correct copyright header.

## Instructions
1. **Read the Template**: Read the content of `resources/HEADER.txt`.
2. **Apply to File**: When creating a new file, prepend this exact content.
3. **Adapt Syntax**: 
   - For Python, convert to `""" """` block.
   - For Svelte, convert to `/* */` block.
   - For Kotlin, convert to `/* */` block.
   - For Swift, convert to `/* */` block.