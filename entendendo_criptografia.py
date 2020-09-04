"""
Entendendo criptografia RSA utilizando-se Python.

Algumas fontes importantes:
    https://www.cs.drexel.edu/~jpopyack/IntroCS/HW/RSAWorksheet.html
    http://encryption-calc.herokuapp.com/
    https://www.tutorialspoint.com/cryptography/public_key_encryption.htm
    https://youtu.be/YEBfamv-_do
    https://imagineer.in/blog/an-attempt-to-implement-rsa/

https://github.com/parklez/rsa-criptography-explained-python
"""
from math import gcd


def is_prime(number: int) -> bool:
    "Números primos só podem ser dividos (sem resto) por 1 e eles mesmos"
    if number > 1:
        for i in range (2, number):
            if (number % i) == 0:
                return False
        return True
    return False


# Gerando uma lista de números primos, entre 0 e 100. 
primos = [x for x in filter(is_prime, range(0, 100))]
# Escrito de forma mais simples:
"""
primos = []
for numero in range(0, 100):
    if is_prime(numero):
        primos.append(numero)
"""
print('Entendendo RSA')
print('-'*30)
print('Lista de primos:')
print(primos)
print('-'*30)

# 1. Escolha 2 números primos grandes p e q.
# https://brasilescola.uol.com.br/o-que-e/matematica/o-que-e-numero-primo.htm
p = int(input('Digite o valor de p: '))
q = int(input('Digite o valor de q: '))

# 2. Calcula-se n e z (Φ)
# RSA MODULUS    -> n = p * q
# Eulers Toitent -> z = (p-1)*(q-1)
n = p*q
z = (p-1)*(q-1)
print('-'*30)
print(f'Valor de n = p*q: {n}')
print(f'Valor de z/phi = (p-1)*(q-1): {z}')

# 3. Escolha um número inteiro "e" > 1 que seja primo em comum com "z"
# Para um número ser primo em comum (coprimos), o seu "máximo divisor comum" deve-se ser "1".
# No python, existe uma função built-in chamada gcd() para encontrar o mdc.
# https://www.todamateria.com.br/mdc-maximo-divisor-comum/
# https://en.wikipedia.org/wiki/Coprime_integers
# No código abaixo, retorna-se o menor/primeiro coprimo entre "e" & "z".
"""
e = 2
while gcd(e, z) != 1:
    e += 1
print(e)
"""
# Podemos descobrir possíveis números "e" entre uma faixa de 0, 100:
numeros_e = []
for numero in range(2, 100):
    if gcd(numero, z) == 1:
        numeros_e.append(numero)
print('-'*30)
print('Lista de números "e" (entre 2 e 100):')
print(numeros_e)
print('-'*30)
e = int(input('Digite um valor de e: '))

# 4. Descobrir d de modo que: "d*e % z = 1"
# Entenda a respeito: https://youtu.be/Z8M2BTscoD4?t=587
# Na formula abaixo, testamos de forma bruta números possíveis para d:
"""
d = int
for number in range (1, 1000):
    if (e * number % z) == 1:
        d = number
        break
"""
# Utilizando o "Algoritimo de Euclides estendido" e  "Inverso multiplicativo modular" para descobrir o número de forma procedural.
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# https://pt.qwe.wiki/wiki/Modular_multiplicative_inverse
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
print('Algoritimo de Euclides estendido + Inverso multiplicativo modular:')
print(f'd é igual a: {d}.')
print('-'*30)
print(f'Chave pública: (e, n): ({e}, {n})')
print(f'Chave privada: (d , n): ({d}, {n})')
chave_publica = (e, n)
chave_privada = (d, n)

### Próximo passo - Criptografar uma mensagem.
# https://www.cryptool.org/en/cto-highlights/rsa-step-by-step
mensagem = input('Digite uma mensagem para ser criptografada: ')

# Formula para criptografar:
# m = número entre 0 e n
# c' = m**e (mod n)
# https://www.cs.drexel.edu/~jpopyack/IntroCS/HW/ASCII.html
def criptografar(chave_publica: tuple, mensagem: str) -> list:
    e, n = chave_publica
    resultado = []
    for letra in mensagem:
        letra = (ord(letra)**e) % n # ord() converte letra em número ascii
        resultado.append(letra)
    return resultado

# Formula para descriptografar:
# m = número entre 0 e n
# c'' = m**d (mod n)
def descriptografar(chave_privada: tuple, mensagem_cript: list) -> str:
    d, n = chave_privada
    resultado = ''
    for letra in mensagem_cript:
        resultado += chr((letra ** d) % n) # chr() converte número ascii em letra
    return resultado

mensagem_criptografada = criptografar(chave_publica, mensagem)
print('Mensagem criptografada:')
print(mensagem_criptografada)

print('Mensagem descriptografada:')
print(descriptografar(chave_privada, mensagem_criptografada))
