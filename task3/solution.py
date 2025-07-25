def merge(intervals: list[int]):
    """Объединяет пересекающиеся интервалы."""
    intervals.sort()
    result = []
    for start, end in intervals:
        if not result or start > result[-1][1]:
            result.append([start, end])
        else:
            result[-1][1] = max(result[-1][1], end)
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.

    Parameters:
        intervals (dict): Словарь с ключами:
            'lesson' (list[int]): Интервал урока [start, end].
            'pupil' (list[int]): Чётные элементы — вход ученика, нечётные — выход.
            'tutor' (list[int]): Аналогично 'pupil' для учителя.

    Returns:
        int: Время общего присутствия ученика и учителя на уроке (в секундах).
    """
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    # преобразуем списки в пары (вход на урок, выход c урока)
    pupil = list(zip(pupil[::2], pupil[1::2]))
    tutor = list(zip(tutor[::2], tutor[1::2]))
    
    # сливаем пересекающиеся интервалы
    pupil = merge(pupil)
    tutor = merge(tutor)

    # находим пересечения pupil и tutor в рамках урока
    result = 0
    i = j = 0
    while i < len(pupil) and j < len(tutor):
        start = max(pupil[i][0], tutor[j][0], lesson[0])
        end = min(pupil[i][1], tutor[j][1], lesson[1])
        if start < end:
            result += end - start
        if pupil[i][1] < tutor[j][1]:
            i += 1
        else:
            j += 1
    return result

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
