import unittest


def strict(func):
    """
    Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, 
    объявленным в прототипе функции.
    
    Parameters:
        func (callable): Функция, которую нужно декорировать.

    Returns:
        callable: Декорированная функция-обёртка `wrapper`.

    Raises:
        TypeError: Если тип аргумента не соответствует аннотации.
    """
    def wrapper(*args, **kwargs):
        # получаем анотацию типов аргументов
        annotations = func.__annotations__
        # проверяем тип для позиционных аргументов
        # создаем пары 'имя аргумента': 'значение' 
        for arg_name, arg_value in zip(func.__code__.co_varnames, args):
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' expected type {expected_type.__name__}, "
                        f"got {type(arg_value).__name__}"
                    )
        # проверяем тип для именовыанных аргументов
        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' expected type {expected_type.__name__}, "
                        f"got {type(arg_value).__name__}"
                    )
        
        return func(*args, **kwargs)
    return wrapper

# ТЕСТЫ
class TestDercorator(unittest.TestCase):
    def test_correct_types(self):
        """Проверка, что функция работает с корректными типами"""
        @strict
        def sum_two(a: int, b: int) -> int:
            return a + b
        
        self.assertEqual(sum_two(1, 2), 3)

    def test_incorrect_positional_arg(self):
        """Проверка TypeError для позиционных аргументов"""
        @strict
        def sum_two(a: int, b: int) -> int:
            return a + b
        
        with self.assertRaises(TypeError) as context:
            sum_two(1, 2.4)
            
        self.assertIn("Argument 'b' expected type int", str(context.exception))

if __name__ == "__main__":
    unittest.main()