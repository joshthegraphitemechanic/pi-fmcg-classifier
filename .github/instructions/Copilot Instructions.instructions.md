---
applyTo: '**'
---
Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.

Project Context:
- The project is a Raspberry Pi-based image classifier for factory line quality control.
- The system captures images, classifies them, and provides a GUI for monitoring and control.
- The codebase is structured into several modules, including GUI, image processing, and configuration management.
- The goal here is that I can deploy this system on any client site, and it should be easy for any of our manufactuiring engineers to use.

Coding Guidelines:
- Never use emojis in code or comments. Even when the user asks for the layout to be more visually appealing - LLM's commonly use emojis and t tends to cause encoding issues; we need this system to be fully compatible with older machines.
- Use descriptive variable and function names.
- Include docstrings for all public modules, classes, and functions.
- Keep the GUI responsive by using threading for long-running tasks.
- Handle exceptions gracefully and provide user feedback in the GUI.