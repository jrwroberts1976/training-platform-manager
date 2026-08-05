# Training Platform Manager v0.4

Training Platform Manager synchronises course repositories and generates the central engineering learning platform.

## Commands

```bash
python3 training_manager.py sync
python3 training_manager.py validate
python3 training_manager.py nav
python3 training_manager.py catalog
python3 training_manager.py build
```

`build` performs:

1. Repository synchronisation
2. Structural validation
3. MkDocs navigation generation
4. Homepage generation
5. Course statistics generation
6. Skill matrix generation
7. Learning-path generation
8. Recent-update generation

## Course manifests

Each course may provide a metadata object in `course-manifest.json`.

See:

```text
templates/course-manifest.example.json
```

Existing lesson-list manifests are handled safely using fallback metadata.
