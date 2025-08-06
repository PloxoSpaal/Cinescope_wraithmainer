def filter_kwargs(**kwargs):
    kwargs = filter(lambda x: True if x[1]>10 else False, kwargs.items())
    return dict(kwargs)

print(filter_kwargs(a=5, b=20, c=15, d=3))
# Вывод: {'b': 20, 'c': 15}