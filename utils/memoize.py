def memoize(f):
    cache = {}

    def foo(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]

    return foo
