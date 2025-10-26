def multiply_all(*args: int) -> int:
    product = 1
    for nums in args:
        product *= nums

    return product 