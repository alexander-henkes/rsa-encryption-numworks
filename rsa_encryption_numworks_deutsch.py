from math import gcd

def ist_prim(n):
    """Prüft, ob n eine Primzahl ist"""
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

def eingabe_primzahl(name):
    """Fordert die Eingabe einer Primzahl"""
    while True:
        try:
            zahl = int(input("Primzahl " + name + ": "))
            if zahl < 2:
                print(str(zahl) + " ist zu klein!")
                continue
            if ist_prim(zahl):
                print("Gültige Eingabe: " + str(zahl) + " ist eine Primzahl!")
                return zahl
            else:
                print(str(zahl) + " ist keine Primzahl!")
        except:
            print("Ungültige Eingabe!")

def erweiterter_euklid(a, b):
    """Berechnet ggT und Koeffizienten"""
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = erweiterter_euklid(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def mod_inverse(e, phi):
    """Berechnet modulares Inverse"""
    g, x, y = erweiterter_euklid(e, phi)
    if g != 1:
        return None
    return x % phi

def potenz_mod(basis, exponent, modul):
    """Schnelle modulare Potenzierung"""
    ergebnis = 1
    basis = basis % modul
    while exponent > 0:
        if exponent % 2 == 1:
            ergebnis = (ergebnis * basis) % modul
        exponent = exponent >> 1
        basis = (basis * basis) % modul
    return ergebnis

def finde_e(phi):
    """Findet geeignetes e"""
    kandidaten = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for e in kandidaten:
        if e < phi and gcd(e, phi) == 1:
            return e
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            return e
    return None

def buchstabe_zu_zahl(buchstabe):
    """Wandelt einen Buchstaben in eine Zahl um (A=0, B=1, ...)"""
    buchstabe = buchstabe.upper()
    if 'A' <= buchstabe <= 'Z':
        return ord(buchstabe) - ord('A')
    return None

def zahl_zu_buchstabe(zahl):
    """Wandelt eine Zahl in einen Buchstaben um (0=A, 1=B, ...)"""
    if 0 <= zahl <= 25:
        return chr(zahl + ord('A'))
    return None

def rsa():
    """Vollständige RSA-Berechnung"""
    
    print("=" * 40)
    print("RSA-Verschlüsselung")
    print("=" * 40)
    print()
    
    # SCHRITT 1
    print("SCHRITT 1: Primzahlen wählen")
    print("-" * 40)
    p = eingabe_primzahl("p")
    
    while True:
        q = eingabe_primzahl("q")
        if q != p:
            break
        print("Fehler: p und q müssen verschieden sein!")
    
    print("Gewählt: p = " + str(p) + ", q = " + str(q))
    input("Weiter mit Enter ...")
    
    # SCHRITT 2
    print()
    print("SCHRITT 2: n und phi(n) berechnen")
    print("-" * 40)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    print("n = p * q = " + str(p) + " * " + str(q) + " = " + str(n))
    print("phi(n) = (p-1) * (q-1)")
    print("phi(n) = " + str(p-1) + " * " + str(q-1) + " = " + str(phi))
    input("Weiter mit Enter ...")
    
    # SCHRITT 3
    print()
    print("SCHRITT 3: Öffentlicher Schlüssel e")
    print("-" * 40)
    print("Hinweis: e muss teilerfremd sein zu phi(n) = " + str(phi))
    print("(ggT(e, phi(n)) = 1)")
    
    vorschlag = finde_e(phi)
    print("Vorschlag: e = " + str(vorschlag))
    antwort = input("Verwenden? (j/n): ")
    
    if antwort.lower() == 'j':
        e = vorschlag
    else:
        while True:
            e = int(input("Eigenes e verwenden: "))
            if e >= phi:
                print("e muss < " + str(phi) + " sein!")
                continue
            if gcd(e, phi) == 1:
                print("Gültige Eingabe: ggT(" + str(e) + ", " + str(phi) + ") = 1")
                break
            else:
                print("ggT(" + str(e) + ", " + str(phi) + ") != 1")
    
    print("Öffentlicher Schlüssel: (" + str(e) + ", " + str(n) + ")")
    input("Weiter mit Enter ...")
    
    # SCHRITT 4
    print()
    print("SCHRITT 4: Privater Schlüssel d")
    print("-" * 40)
    print("d ist modulares Inverse von e mod phi(n)")
    print("d * e = 1 (mod " + str(phi) + ")")
    print("Berechne mit erweitertem euklidischen Algorithmus:")
    
    d = mod_inverse(e, phi)
    
    print("d = " + str(d))
    print("Prüfung: " + str(d) + " * " + str(e) + " mod " + str(phi) + " = " + str((d * e) % phi))
    print("Privater Schlüssel: (" + str(d) + ", " + str(n) + ")")
    input("Weiter mit Enter ...")
    
    # SCHRITT 5
    print()
    print("SCHRITT 5: Nachricht verschlüsseln")
    print("-" * 40)
    print("Verschlüsselung: c = m^e mod n")
    print("c = m^" + str(e) + " mod " + str(n))
    print()
    print("Buchstaben-Codierung: A=0, B=1, C=2, ..., Z=25")
    print()
    
    while True:
        buchstabe = input("Buchstabe eingeben (A-Z): ").strip()
        if len(buchstabe) == 1:
            m = buchstabe_zu_zahl(buchstabe)
            if m is not None:
                if m < n:
                    print("Buchstabe '" + buchstabe.upper() + "' entspricht der Zahl: " + str(m))
                    break
                else:
                    print("Fehler: Die Zahl " + str(m) + " ist zu groß (>= " + str(n) + ")!")
                    print("Bitte wähle kleinere Primzahlen oder einen anderen Buchstaben!")
            else:
                print("Ungültiger Buchstabe! Bitte A-Z eingeben.")
        else:
            print("Bitte nur einen Buchstaben eingeben!")
    
    c = potenz_mod(m, e, n)
    
    print()
    print("c = " + str(m) + "^" + str(e) + " mod " + str(n))
    print("c = " + str(c))
    print("Verschlüsselt: " + str(c))
    input("Weiter mit Enter ...")
    
    # SCHRITT 6
    print()
    print("SCHRITT 6: Nachricht entschlüsseln")
    print("-" * 40)
    print("Entschlüsselung: m = c^d mod n")
    print("m = " + str(c) + "^" + str(d) + " mod " + str(n))
    
    m_neu = potenz_mod(c, d, n)
    buchstabe_neu = zahl_zu_buchstabe(m_neu)
    
    print("m = " + str(c) + "^" + str(d) + " mod " + str(n))
    print("m = " + str(m_neu))
    print("Entschlüsselter Buchstabe: " + str(buchstabe_neu))
    
    if m == m_neu:
        print("Erfolgreich entschlüsselt!")
    else:
        print("Fehler bei Entschlüsselung!")
    
    input("Weiter mit Enter ...")
    
    # ZUSAMMENFASSUNG
    print()
    print("=" * 40)
    print("ZUSAMMENFASSUNG")
    print("=" * 40)
    print("Primzahlen:             p = " + str(p) + ", q = " + str(q))
    print("Modul:                  n = " + str(n))
    print("Euler-Funktion:         phi(n) = " + str(phi))
    print("Öffentlicher Schlüssel: (" + str(e) + ", " + str(n) + ")")
    print("Privater Schlüssel:     (" + str(d) + ", " + str(n) + ")")
    print("Klartext (Buchstabe):   " + buchstabe.upper())
    print("Klartext (Zahl):        m = " + str(m))
    print("Verschlüsselt:          c = " + str(c))
    print("Entschlüsselt (Zahl):   m = " + str(m_neu))
    print("Entschlüsselt (Buchst.):" + str(buchstabe_neu))
    print("=" * 40)

# Programm starten
while True:
    rsa()
    print()
    nochmal = input("Nochmal starten? (j/n): ")
    if nochmal.lower() != 'j':
        print("Programm beendet.")
        break
    print("\n" * 2)
