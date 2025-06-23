import pytest
from collections import defaultdict
import solution

"""
Для выполнения тестов должны быть установленны библиотеки:
	pytest
    pytest-mock
Для запуска в папке task2 запустить `pytest test.py` в терминале
"""

@pytest.fixture
def test_html():
    return """
    <div class="mw-category mw-category-columns">
        <h3>А</h3>
        <ul><li><a href="/wiki/Аист">Аист</a></li></ul>
	</div>
    <div class="mw-category mw-category-columns">
        <h3>Б</h3>
        <ul><li><a href="/wiki/Барсук">Барсук</a></li></ul>
    </div>
    """

def test_parse_page(mocker, test_html):
    # подменяем HTTP-запрос моком
    mock_get = mocker.patch('solution.requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = test_html

    animals = defaultdict(int)
    solution.parse_page('http://test.url', animals)

    assert animals == {'А': 1, 'Б': 1}


# Тест сохранения в CSV
def test_save_to_csv(tmp_path):
    test_data = {'А': 5}
    test_file = tmp_path / "animals.csv"
    
    solution.save_to_csv(test_data, test_file)
    
    content = test_file.read_text(encoding='utf-8')
    assert 'А,5' in content