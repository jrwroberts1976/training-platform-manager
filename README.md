# Training Platform Manager v0.2

## Commands

```bash
python3 training_manager.py sync
python3 training_manager.py validate
python3 training_manager.py nav
python3 training_manager.py stats
python3 training_manager.py build
```

`build` performs:

1. Course repository synchronisation
2. Structural validation
3. Central MkDocs navigation generation
4. Course statistics generation

## Central MkDocs markers

```yaml
      # BEGIN AUTOMATED COURSES
      # END AUTOMATED COURSES
```

## Add a course

Add one object to `config/courses.json`, commit it, and push the manager repository.
