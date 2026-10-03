"""Task 3: predefined code snippets. Each returns (result, operation_count)."""


def single_loop(n):
    total = 0
    for i in range(n):
        total += i
    return total, n


def nested_loop(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total, n * n


def recursive_factorial(n):
    ops = 0

    def fact(k):
        nonlocal ops
        ops += 1
        if k <= 1:
            return 1
        return k * fact(k - 1)

    return fact(n), ops


def iterative_factorial(n):
    result = 1
    ops = 0
    for i in range(2, n + 1):
        result *= i
        ops += 1
    return result, ops


LOOPS = {"Single Loop": single_loop, "Nested Loop": nested_loop}
FACTORIAL = {"Recursive Factorial": recursive_factorial,
             "Iterative Factorial": iterative_factorial}
SNIPPETS = {**LOOPS, **FACTORIAL}
