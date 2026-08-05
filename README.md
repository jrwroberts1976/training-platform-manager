# Training Platform Manager v0.5

## Create a course

```bash
python3 training_manager.py create-course docker   --template docker
```

Create a custom course:

```bash
python3 training_manager.py create-course aws   --title "AWS Cloud Engineering"   --level "Beginner to Intermediate"   --hours 40   --modules "Introduction,IAM,Networking,Compute,Storage,Monitoring,Security,Final Project"
```

Optional automation:

```bash
python3 training_manager.py create-course docker   --template docker   --github   --register
```

`--github` requires an authenticated GitHub CLI installation.

The manager intentionally does not deploy immediately after creating a local
repository that has not been pushed. After repository creation and registration,
run:

```bash
python3 training_manager.py build
```
