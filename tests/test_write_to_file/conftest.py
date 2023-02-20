import pytest
import os

@pytest.fixture(autouse=True)
def clean_text_file():
    with open('test_tmp_file.txt', 'w') as f:
        pass
    # Removing test files
    yield
    os.remove('test_tmp_file.txt')

# Сделать чтобы после выполнения теста данные удалялись