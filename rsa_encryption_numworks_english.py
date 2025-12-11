from math import gcd

def is_prime(n):
    """Check if n is a prime number"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def input_prime(name):
    """Request input of a prime number"""
    while True:
        try:
            number = int(input("Prime number " + name + ": "))
            if number < 2:
                print(str(number) + " is too small!")
                continue
            if is_prime(number):
                print("Valid input: " + str(number) + " is a prime number!")
                return number
            else:
                print(str(number) + " is not a prime number!")
        except:
            print("Invalid input!")

def extended_euclid(a, b):
    """Calculate gcd and coefficients"""
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_euclid(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def mod_inverse(e, phi):
    """Calculate modular inverse"""
    g, x, y = extended_euclid(e, phi)
    if g != 1:
        return None
    return x % phi

def power_mod(base, exponent, modulus):
    """Fast modular exponentiation"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def find_e(phi):
    """Find suitable e"""
    candidates = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for e in candidates:
        if e < phi and gcd(e, phi) == 1:
            return e
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            return e
    return None

def letter_to_number(letter):
    """Convert a letter to a number (A=0, B=1, ...)"""
    letter = letter.upper()
    if 'A' <= letter <= 'Z':
        return ord(letter) - ord('A')
    return None

def number_to_letter(number):
    """Convert a number to a letter (0=A, 1=B, ...)"""
    if 0 <= number <= 25:
        return chr(number + ord('A'))
    return None

def rsa():
    """Complete RSA calculation"""
    
    print("=" * 40)
    print("RSA Encryption")
    print("=" * 40)
    print()
    
    # STEP 1
    print("STEP 1: Choose prime numbers")
    print("-" * 40)
    p = input_prime("p")
    
    while True:
        q = input_prime("q")
        if q != p:
            break
        print("Error: p and q must be different!")
    
    print("Selected: p = " + str(p) + ", q = " + str(q))
    input("Continue with Enter ...")
    
    # STEP 2
    print()
    print("STEP 2: Calculate n and phi(n)")
    print("-" * 40)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    print("n = p * q = " + str(p) + " * " + str(q) + " = " + str(n))
    print("phi(n) = (p-1) * (q-1)")
    print("phi(n) = " + str(p-1) + " * " + str(q-1) + " = " + str(phi))
    input("Continue with Enter ...")
    
    # STEP 3
    print()
    print("STEP 3: Public key e")
    print("-" * 40)
    print("Note: e must be coprime to phi(n) = " + str(phi))
    print("(gcd(e, phi(n)) = 1)")
    
    suggestion = find_e(phi)
    print("Suggestion: e = " + str(suggestion))
    answer = input("Use this? (y/n): ")
    
    if answer.lower() == 'y':
        e = suggestion
    else:
        while True:
            e = int(input("Use custom e: "))
            if e >= phi:
                print("e must be < " + str(phi) + "!")
                continue
            if gcd(e, phi) == 1:
                print("Valid input: gcd(" + str(e) + ", " + str(phi) + ") = 1")
                break
            else:
                print("gcd(" + str(e) + ", " + str(phi) + ") != 1")
    
    print("Public key: (" + str(e) + ", " + str(n) + ")")
    input("Continue with Enter ...")
    
    # STEP 4
    print()
    print("STEP 4: Private key d")
    print("-" * 40)
    print("d is the modular inverse of e mod phi(n)")
    print("d * e = 1 (mod " + str(phi) + ")")
    print("Calculate using extended Euclidean algorithm:")
    
    d = mod_inverse(e, phi)
    
    print("d = " + str(d))
    print("Verification: " + str(d) + " * " + str(e) + " mod " + str(phi) + " = " + str((d * e) % phi))
    print("Private key: (" + str(d) + ", " + str(n) + ")")
    input("Continue with Enter ...")
    
    # STEP 5
    print()
    print("STEP 5: Encrypt message")
    print("-" * 40)
    print("Encryption: c = m^e mod n")
    print("c = m^" + str(e) + " mod " + str(n))
    print()
    print("Letter encoding: A=0, B=1, C=2, ..., Z=25")
    print()
    
    while True:
        letter = input("Enter letter (A-Z): ").strip()
        if len(letter) == 1:
            m = letter_to_number(letter)
            if m is not None:
                if m < n:
                    print("Letter '" + letter.upper() + "' corresponds to number: " + str(m))
                    break
                else:
                    print("Error: The number " + str(m) + " is too large (>= " + str(n) + ")!")
                    print("Please choose smaller prime numbers or a different letter!")
            else:
                print("Invalid letter! Please enter A-Z.")
        else:
            print("Please enter only one letter!")
    
    c = power_mod(m, e, n)
    
    print()
    print("c = " + str(m) + "^" + str(e) + " mod " + str(n))
    print("c = " + str(c))
    print("Encrypted: " + str(c))
    input("Continue with Enter ...")
    
    # STEP 6
    print()
    print("STEP 6: Decrypt message")
    print("-" * 40)
    print("Decryption: m = c^d mod n")
    print("m = " + str(c) + "^" + str(d) + " mod " + str(n))
    
    m_new = power_mod(c, d, n)
    letter_new = number_to_letter(m_new)
    
    print("m = " + str(c) + "^" + str(d) + " mod " + str(n))
    print("m = " + str(m_new))
    print("Decrypted letter: " + str(letter_new))
    
    if m == m_new:
        print("Successfully decrypted!")
    else:
        print("Decryption error!")
    
    input("Continue with Enter ...")
    
    # SUMMARY
    print()
    print("=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print("Prime numbers:          p = " + str(p) + ", q = " + str(q))
    print("Modulus:                n = " + str(n))
    print("Euler function:         phi(n) = " + str(phi))
    print("Public key:             (" + str(e) + ", " + str(n) + ")")
    print("Private key:            (" + str(d) + ", " + str(n) + ")")
    print("Plaintext (letter):     " + letter.upper())
    print("Plaintext (number):     m = " + str(m))
    print("Encrypted:              c = " + str(c))
    print("Decrypted (number):     m = " + str(m_new))
    print("Decrypted (letter):     " + str(letter_new))
    print("=" * 40)

# Start program
while True:
    rsa()
    print()
    again = input("Run again? (y/n): ")
    if again.lower() != 'y':
        print("Program terminated.")
        break
    print("\n" * 2)
