# Training Platform Manager

Synchronises registered course repositories, validates their structure, and generates the central MkDocs navigation.

## Commands

```bash
python3 training_manager.py sync
python3 training_manager.py validate
python3 training_manager.py nav
python3 training_manager.py build
```

The `build` command performs sync, validation, and navigation generation.

The central MkDocs file must include:

```yaml
      # BEGIN AUTOMATED COURSES
      # END AUTOMATED COURSES
```
