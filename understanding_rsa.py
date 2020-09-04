"""
Understanding RSA cryptography using Python

Noteworthy sources:
    https://www.cs.drexel.edu/~jpopyack/IntroCS/HW/RSAWorksheet.html
    http://encryption-calc.herokuapp.com/
    https://www.tutorialspoint.com/cryptography/public_key_encryption.htm
    https://youtu.be/YEBfamv-_do
    https://imagineer.in/blog/an-attempt-to-implement-rsa/

https://github.com/parklez/rsa-criptography-explained-python
"""
from math import gcd


def is_prime(number: int) -> bool:
    if number > 1:
        for i in range (2, number):
            if (number % i) == 0:
                return False
        return True
    return False


# Generating a list of prime numbers
# https://en.wikipedia.org/wiki/Prime_number
# Numbers of 2048 bits are usually chosen in actual use.
primes = [x for x in filter(is_prime, range(0, 100))]
# The above expression written in easier to read form:
"""
primes = []
for number in range(0, 100):
    if is_prime(number):
        primes.append(number)
"""
print('Understanding RSA')
print('-'*30)
print('Primes list:')
print(primes)
print('-'*30)

# 1. Choose 2 prime numbers p and q
p = int(input('Value for p: '))
q = int(input('Value for q: '))

# 2. Calculating n and Φ
# RSA MODULUS    -> n = p * q
# Eulers Toitent -> Φ = (p-1)*(q-1)
n = p*q
z = (p-1)*(q-1)
print('-'*30)
print(f'Value for n = p*q: {n}')
print(f'Value for Φ = (p-1)*(q-1): {z}')

# 3. Choose e, for e > 0 and is coprime with Φ
# For a number to be coprime to another, their greatest common divisor must be equal to "1".
# https://en.wikipedia.org/wiki/Greatest_common_divisor
# https://en.wikipedia.org/wiki/Coprime_integers
# The commented code below finds the lowest/first value for e:
"""
e = 2
while gcd(e, z) != 1:
    e += 1
print(e)
"""
# We can choose from a range of possible values, ideally bigger is better.
numbers_e = []
for number in range(2, 100):
    if gcd(number, z) == 1:
        numbers_e.append(number)
print('-'*30)
print('List of numbers "e" between (2, 100):')
print(numbers_e)
print('-'*30)
e = int(input('Value for e: '))

# 4. Find d such that: "d*e % z = 1"
# https://youtu.be/Z8M2BTscoD4?t=587
# The code below checks for a range of possible values, not great solution:
"""
d = int
for number in range (1, 1000):
    if (e * number % z) == 1:
        d = number
        break
"""
# Using "Extended Euclidean algorithm" & "Modular multiplicative inverse" to find d in a procedural way:
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# https://stackoverflow.com/a/9758173
# https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Modular_inverse
def extended_euclidean_algorithm(a: int, b: int) -> tuple:
    # Base Case  
    if a == 0 :   
        return b, 0, 1
             
    gcd, x1, y1 = extended_euclidean_algorithm(b%a, a)  
    # Update x and y using results of recursive  
    # call  
    x = y1 - (b//a) * x1  
    y = x1  
     
    return gcd, x, y 
 
def multiplicative_inverse(a: int, b: int) -> int:
    gcd, x, y = extended_euclidean_algorithm(a, b)
    if (gcd != 1):
        return None
    else:
        return x % b


d = multiplicative_inverse(e, z)

print('-'*30)
print(f'Value for d: d*e % z = 1: {d}')
print(f'Public key: (e, n): ({e}, {n})')
print(f'Private key: (d , n): ({d}, {n})')
print('-'*30)
public_key = (e, n)
private_key = (d, n)

### Next step - encrypt and decrypt a message
# https://www.cryptool.org/en/cto-highlights/rsa-step-by-step
message = input('Type in a message to be encrypted: ')

# Formula to encrypt:
# m = 0 < m < n
# c' = m**e (mod n)
# https://www.cs.drexel.edu/~jpopyack/IntroCS/HW/ASCII.html
def encrypt(public_key: tuple, message: str) -> list:
    e, n = public_key
    result = []
    for char in message:
        char = (ord(char)**e) % n # ord() converts ascii char into its numerical representation
        result.append(char)
    return result

# Formula to decrypt:
# m = 0 < m < n
# c'' = m**d (mod n)
def decrypt(private_key: tuple, encrypted_msg: list) -> str:
    d, n = private_key
    result = ''
    for char in encrypted_msg:
        result += chr((char ** d) % n) # chr() converts ascii number into char
    return result

message_encrypted = encrypt(public_key, message)
print('Encrypted message:')
print(message_encrypted)

print('Decrypted message:')
print(decrypt(private_key, message_encrypted))
