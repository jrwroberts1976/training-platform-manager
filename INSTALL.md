# Installation

```bash
cd ~/projects/training-platform-manager
git init
git branch -M main
git add .
git commit -m "Add training platform manager"
git remote add origin git@github.com:jrwroberts1976/training-platform-manager.git
git push -u origin main
```

Clone it into the platform:

```bash
cd ~/docker/stacks/training-platform
git clone git@github.com:jrwroberts1976/training-platform-manager.git training-platform-manager
python3 training-platform-manager/training_manager.py build
```
