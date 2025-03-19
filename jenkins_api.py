import pytest
import requests
import json
import re

BASE_URL = "https://jsonplaceholder.typicode.com/users"


# Test 1: Kullanıcı listesini getirme ve en az 5 kullanıcının olması
def test_users_list():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, "API isteği başarısız"
    users = response.json()
    assert len(users) >= 5, "Beklenen kadar kullanıcı yok"


# Test 2: Kullanıcı bilgilerinin belirli alanları içerip içermediğini kontrol etme
def test_user_data():
    response = requests.get(f"{BASE_URL}/1")
    assert response.status_code == 200, "Kullanıcı getirilemedi"

    user = response.json()
    assert "id" in user, "id eksik"
    assert "name" in user, "name eksik"
    assert "email" in user, "email eksik"
    assert "phone" in user, "phone eksik"



# Test 3: Yeni kullanıcı ekleme
@pytest.fixture
def create_user():
    new_user = {
        "name": "Test Kullanıcısı",
        "username": "testuser",
        "email": "test@example.com",
        "phone": "123-456-7890"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(BASE_URL, data=json.dumps(new_user), headers=headers)
    return response


def test_create_user(create_user):
    response = create_user
    assert response.status_code == 201, "Kullanıcı eklenemedi"
    user_data = response.json()
    assert user_data["name"] == "Test Kullanıcısı", "Kullanıcı adı yanlış"
    assert user_data["email"] == "test@example.com", "E-posta yanlış"


# Test 4: Kullanıcı güncelleme (PATCH ile düzeltildi)
def test_update_user(create_user):
    user_id = create_user.json().get("id")
    updated_data = {"name": "Güncellenmiş Kullanıcı"}

    response = requests.patch(f"{BASE_URL}/{user_id}", data=json.dumps(updated_data),
                              headers={'Content-Type': 'application/json'})
    assert response.status_code == 200, "Kullanıcı güncellenemedi"

    updated_user = response.json()
    assert updated_user["name"] == "Güncellenmiş Kullanıcı", "Kullanıcı adı güncellenmedi"


# Test 5: Kullanıcı silme
def test_delete_user(create_user):
    user_id = create_user.json().get("id")
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200, "Kullanıcı silinemedi"
