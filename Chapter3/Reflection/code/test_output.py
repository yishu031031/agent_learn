def find_primes(n):
    """
    Find all prime numbers between 1 and n using the Sieve of Eratosthenes.

    Parameters:
    n (int): The upper limit of the range to find prime numbers.

    Returns:
    list: A list of prime numbers between 1 and n.
    """
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i:n + 1:i] = [False] * len(range(i * i, n + 1, i))

    return [i for i in range(2, n + 1) if is_prime[i]]

print(find_primes(10))