import time


def decorator_cache(func):
    '''Декоратор кэширует ответ для входных значений, чтобы не вычислять повторно'''
    cache = {}

    def wrapper(*args, **kwargs):
        value_in_cache = cache.get(args)
        if value_in_cache is None:
            print("вычисляем и добавляем в кэш")
            result = func(*args, **kwargs)
            cache[args] = result
        else:
            print("взяли из кэша")
            result = value_in_cache
        return result

    return wrapper


def decorator_multicall(call_count, start_sleep_time, border_sleep_time):
    '''
    В качестве параметров декоратор будет получать:

    call_count - число, описывающее кол-во раз запуска функций;

    start_sleep_time - в секундах начальное время повтора;

    border_sleep_time - в секундах граничное время ожидания.

    Декоратор для повторного выполнения декорируемой функции через некоторое время.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time).

    '''

    def real_decorator(func):
        def func_info_print(iter_num, t, res):
            real_time = time.perf_counter()
            s = f'{real_time}: Запуск номер {iter_num}. Ожидание: {t} secs. '
            s1 = f'Результат декорируемой функций = {res}.'
            s = s + s1
            print(s)

        def wrapper(*args, **kwargs):
            time_to_sleep = 0

            for iter_num in range(0, call_count):
                time.sleep(time_to_sleep)
                result = func(*args)
                time_to_sleep = min(start_sleep_time * 2 ** iter_num, border_sleep_time)
                func_info_print(iter_num + 1, time_to_sleep, result)

            print("Конец работы")
            return result

        return wrapper

    return real_decorator


@decorator_cache
def multiplier(number: int):
    return number * 2


@decorator_multicall(7, 1, 10)
def multiplier1(number: int):
    return number * 2


if __name__ == '__main__':
    n = 5
    print("Работа первого декоратора")
    print(multiplier(6))
    print(multiplier(6))
    print(multiplier(7))
    print(multiplier(9))
    print(multiplier(7))
    print(multiplier(9))
    print("Работа второго декортора")

    multiplier1(10)
