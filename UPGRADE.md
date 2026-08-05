# Upgrade to v0.4

## Back up the current manager

```bash
cd ~/docker/stacks/training-platform
cp -a training-platform-manager training-platform-manager-v0.2-backup
```

## Copy v0.4 files into the existing Git checkout

Preserve:

```text
config/courses.json
```

Then run:

```bash
cd ~/docker/stacks/training-platform/training-platform-manager
python3 training_manager.py build
```

## Add generated pages to central navigation

Recommended entries under Training:

```yaml
      - Platform Summary: training/course-statistics.md
      - Skill Matrix: training/skill-matrix.md
      - Learning Paths: training/learning-paths.md
      - Recent Updates: training/recent-updates.md
```
