from math import gcd

def est_premier(n):
    """Vérifie si n est un nombre premier"""
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

def saisie_premier(nom):
    """Demande la saisie d'un nombre premier"""
    while True:
        try:
            nombre = int(input("Nombre premier " + nom + ": "))
            if nombre < 2:
                print(str(nombre) + " est trop petit!")
                continue
            if est_premier(nombre):
                print("Saisie valide: " + str(nombre) + " est un nombre premier!")
                return nombre
            else:
                print(str(nombre) + " n'est pas un nombre premier!")
        except:
            print("Saisie invalide!")

def euclide_etendu(a, b):
    """Calcule le pgcd et les coefficients"""
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = euclide_etendu(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def inverse_mod(e, phi):
    """Calcule l'inverse modulaire"""
    g, x, y = euclide_etendu(e, phi)
    if g != 1:
        return None
    return x % phi

def puissance_mod(base, exposant, module):
    """Exponentiation modulaire rapide"""
    resultat = 1
    base = base % module
    while exposant > 0:
        if exposant % 2 == 1:
            resultat = (resultat * base) % module
        exposant = exposant >> 1
        base = (base * base) % module
    return resultat

def trouve_e(phi):
    """Trouve un e approprié"""
    candidats = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for e in candidats:
        if e < phi and gcd(e, phi) == 1:
            return e
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            return e
    return None

def lettre_vers_nombre(lettre):
    """Convertit une lettre en nombre (A=0, B=1, ...)"""
    lettre = lettre.upper()
    if 'A' <= lettre <= 'Z':
        return ord(lettre) - ord('A')
    return None

def nombre_vers_lettre(nombre):
    """Convertit un nombre en lettre (0=A, 1=B, ...)"""
    if 0 <= nombre <= 25:
        return chr(nombre + ord('A'))
    return None

def rsa():
    """Calcul RSA complet"""
    
    print("=" * 40)
    print("Chiffrement RSA")
    print("=" * 40)
    print()
    
    # ÉTAPE 1
    print("ÉTAPE 1: Choisir les nombres premiers")
    print("-" * 40)
    p = saisie_premier("p")
    
    while True:
        q = saisie_premier("q")
        if q != p:
            break
        print("Erreur: p et q doivent être différents!")
    
    print("Sélectionné: p = " + str(p) + ", q = " + str(q))
    input("Continuer avec Entrée ...")
    
    # ÉTAPE 2
    print()
    print("ÉTAPE 2: Calculer n et phi(n)")
    print("-" * 40)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    print("n = p * q = " + str(p) + " * " + str(q) + " = " + str(n))
    print("phi(n) = (p-1) * (q-1)")
    print("phi(n) = " + str(p-1) + " * " + str(q-1) + " = " + str(phi))
    input("Continuer avec Entrée ...")
    
    # ÉTAPE 3
    print()
    print("ÉTAPE 3: Clé publique e")
    print("-" * 40)
    print("Note: e doit être premier avec phi(n) = " + str(phi))
    print("(pgcd(e, phi(n)) = 1)")
    
    suggestion = trouve_e(phi)
    print("Suggestion: e = " + str(suggestion))
    reponse = input("Utiliser? (o/n): ")
    
    if reponse.lower() == 'o':
        e = suggestion
    else:
        while True:
            e = int(input("Utiliser un e personnalisé: "))
            if e >= phi:
                print("e doit être < " + str(phi) + "!")
                continue
            if gcd(e, phi) == 1:
                print("Saisie valide: pgcd(" + str(e) + ", " + str(phi) + ") = 1")
                break
            else:
                print("pgcd(" + str(e) + ", " + str(phi) + ") != 1")
    
    print("Clé publique: (" + str(e) + ", " + str(n) + ")")
    input("Continuer avec Entrée ...")
    
    # ÉTAPE 4
    print()
    print("ÉTAPE 4: Clé privée d")
    print("-" * 40)
    print("d est l'inverse modulaire de e mod phi(n)")
    print("d * e = 1 (mod " + str(phi) + ")")
    print("Calcul avec l'algorithme d'Euclide étendu:")
    
    d = inverse_mod(e, phi)
    
    print("d = " + str(d))
    print("Vérification: " + str(d) + " * " + str(e) + " mod " + str(phi) + " = " + str((d * e) % phi))
    print("Clé privée: (" + str(d) + ", " + str(n) + ")")
    input("Continuer avec Entrée ...")
    
    # ÉTAPE 5
    print()
    print("ÉTAPE 5: Chiffrer le message")
    print("-" * 40)
    print("Chiffrement: c = m^e mod n")
    print("c = m^" + str(e) + " mod " + str(n))
    print()
    print("Codage des lettres: A=0, B=1, C=2, ..., Z=25")
    print()
    
    while True:
        lettre = input("Entrer une lettre (A-Z): ").strip()
        if len(lettre) == 1:
            m = lettre_vers_nombre(lettre)
            if m is not None:
                if m < n:
                    print("La lettre '" + lettre.upper() + "' correspond au nombre: " + str(m))
                    break
                else:
                    print("Erreur: Le nombre " + str(m) + " est trop grand (>= " + str(n) + ")!")
                    print("Veuillez choisir des nombres premiers plus petits ou une autre lettre!")
            else:
                print("Lettre invalide! Veuillez entrer A-Z.")
        else:
            print("Veuillez entrer une seule lettre!")
    
    c = puissance_mod(m, e, n)
    
    print()
    print("c = " + str(m) + "^" + str(e) + " mod " + str(n))
    print("c = " + str(c))
    print("Chiffré: " + str(c))
    input("Continuer avec Entrée ...")
    
    # ÉTAPE 6
    print()
    print("ÉTAPE 6: Déchiffrer le message")
    print("-" * 40)
    print("Déchiffrement: m = c^d mod n")
    print("m = " + str(c) + "^" + str(d) + " mod " + str(n))
    
    m_nouveau = puissance_mod(c, d, n)
    lettre_nouvelle = nombre_vers_lettre(m_nouveau)
    
    print("m = " + str(c) + "^" + str(d) + " mod " + str(n))
    print("m = " + str(m_nouveau))
    print("Lettre déchiffrée: " + str(lettre_nouvelle))
    
    if m == m_nouveau:
        print("Déchiffrement réussi!")
    else:
        print("Erreur de déchiffrement!")
    
    input("Continuer avec Entrée ...")
    
    # RÉSUMÉ
    print()
    print("=" * 40)
    print("RÉSUMÉ")
    print("=" * 40)
    print("Nombres premiers:       p = " + str(p) + ", q = " + str(q))
    print("Module:                 n = " + str(n))
    print("Fonction d'Euler:       phi(n) = " + str(phi))
    print("Clé publique:           (" + str(e) + ", " + str(n) + ")")
    print("Clé privée:             (" + str(d) + ", " + str(n) + ")")
    print("Texte clair (lettre):   " + lettre.upper())
    print("Texte clair (nombre):   m = " + str(m))
    print("Chiffré:                c = " + str(c))
    print("Déchiffré (nombre):     m = " + str(m_nouveau))
    print("Déchiffré (lettre):     " + str(lettre_nouvelle))
    print("=" * 40)

# Démarrer le programme
while True:
    rsa()
    print()
    encore = input("Relancer? (o/n): ")
    if encore.lower() != 'o':
        print("Programme terminé.")
        break
    print("\n" * 2)
