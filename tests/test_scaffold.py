from training_manager.utils import slugify

def test_slugify():
    assert slugify("Docker Compose") == "docker-compose"
