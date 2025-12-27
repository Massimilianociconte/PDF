
import pytest
from app.api.auth import authenticate_user, verify_password, get_password_hash
from app.config import settings

def test_password_hashing():
    password = "secret"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_authenticate_user_success():
    # Use the default hash in settings (which corresponds to 'changeme123')
    user = authenticate_user(settings.admin_username, "changeme123")
    assert user is not None
    assert user.username == settings.admin_username

def test_authenticate_user_failure():
    user = authenticate_user(settings.admin_username, "wrongpassword")
    assert user is None

def test_authenticate_user_wrong_username():
    user = authenticate_user("wronguser", "changeme123")
    assert user is None
