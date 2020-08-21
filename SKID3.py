import hashlib

def generateRandom():
    r = sage.misc.prandom.getrandbits(64)
    r = bin(r)[2:]
    return r


def mac1(r_a,r_b, name, k):
    ipad = 0x5c
    opad = 0x36
    nick = ''.join(format(ord(i), 'b') for i in name)
    m = str(r_a)+str(r_b)+str(nick)
    j = hashlib.new('sha256')
    j.update(m)

    x = int(k)^int(ipad)
    y = str(x)+str(j.hexdigest())
    
    l = hashlib.new('sha256')
    l.update(str(y))
    
    w = str(int(k)^int(opad))+str(l.hexdigest())
    h = hashlib.new('sha256')
    h.update(w)
    return h

def mac2(r_a, name, k):
    ipad = 0x5c
    opad = 0x36
    nick = ''.join(format(ord(i), 'b') for i in name)
    m = str(r_a)+str(nick)
    j = hashlib.new('sha256')
    j.update(m)
    
    x = int(k)^int(ipad)
    y = str(x)+str(j.hexdigest())
    
    l = hashlib.new('sha256')
    l.update(str(y))
    
    w = str(int(k)^int(opad))+str(l.hexdigest())+str(j.hexdigest())
    h = hashlib.new('sha256')
    h.update(w)
    return h

A = "Alicja"
B = "Bob"
k = sage.misc.prandom.getrandbits(64)
k = bin(k)[2:]

r_a = generateRandom()
print("Uzytkownik " + A + " wygenerowal liczbe losowa: " + r_a)
r_b = generateRandom()
print("Uzytkownik " + B + " wygenerowal liczbe losowa: " + r_b)
print("Klucz tajny to: "+ k)


print(B + " otrzymal liczbe losowa od uzytkownika " + A)
H1 = mac1(r_a,r_b,str(B),k)
print(B + " oblicza wartosc skrotu przy uzyciu swojej liczby losowej, liczby losowej uzytkownika " + A + " oraz swojej nazwy uzytkownika i wspolnego klucza:")
H1.hexdigest()
print(A + " otrzymal liczbe losowa od uzytkownika " + B + " i obliczony przez niego skrot")
print(A + " oblicza swoja wartosc skrotu:")
H2 = mac1(r_a,r_b,str(B),k)
H2.hexdigest()

if(H1.hexdigest() == H2.hexdigest()):
    print("Funkcje skrotu sa identyczne - " + A + " wie, ze komunikuje sie z " + B)
    print(A + " oblicza i wysyla uzytkownikowi " + B + " wartosc skrotu przy uzyciu liczby losowej " + B + ", swojej nazwy uzytkownika oraz wspolnego klucza:")
    H3 = mac2(r_b, str(A),k)
    H3.hexdigest()
    print(B + " otrzymuje wartosc skrotu od " + A + " po czym oblicza swoja wartosc skrotu:")
    H4 = mac2(r_b, str(A),k)
    H4.hexdigest()

    if(H3.hexdigest() == H4.hexdigest()):
        print("Funkcje skrotu sa identyczne - " + B + " wie, ze komunikuje sie z " + A)

else:
    print("Wystapil blad!")