# Upgrade to v0.2

Back up the existing manager:

```bash
cd ~/docker/stacks/training-platform
mv training-platform-manager training-platform-manager.backup
```

Extract or clone v0.2 into:

```text
~/docker/stacks/training-platform/training-platform-manager
```

Preserve the current `config/courses.json`, then run:

```bash
cd ~/docker/stacks/training-platform/training-platform-manager
python3 training_manager.py build
```
