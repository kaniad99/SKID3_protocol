import hashlib
import time
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
    l = hashlib.new('sha256')
    l.update(str(int(k)^int(ipad)))
    
    w = str(int(k)^int(opad))+str(l.hexdigest())+str(j.hexdigest())
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
    
    l = hashlib.new('sha256')
    l.update(str(int(k)^int(ipad)))
    
    w = str(int(k)^int(opad))+str(l.hexdigest())+str(j.hexdigest())
    h = hashlib.new('sha256')
    h.update(w)
    return h

def testy(l):
        s = 0
        p = 0
        for x in xrange(l):
            k = sage.misc.prandom.getrandbits(64)
            k = bin(k)[2:]
            r_a = generateRandom()
            r_b = generateRandom()

            H1 = mac1(r_a,r_b,str(B),k)
            H2 = mac1(r_a,r_b,str(B),k)

            if(H1.hexdigest() == H2.hexdigest()):
                H3 = mac2(r_b, str(A),k)
                H4 = mac2(r_b, str(A),k)

                if(H3.hexdigest() == H4.hexdigest()):
                    s = s + 1

            else:
                p = p + 1

        print("Wykonano " + str(l) + " testow dzialania.")
        print("Udane uwierzytelniania: " + str(s))
        print("Nieudane uwierzytelniania: "+ str(p))


A = raw_input("Podaj nazwe pierwszego uzytkownika:")
B = raw_input("Podaj nazwe drugiego uzytkownika:")
p = raw_input("Ile serii pomiarow chcesz wykonac?")
l = raw_input("Ile testow chcesz wykonywac w jednej serii?")
p = int(p)
l = int(l)
def pomiar(l,p):
    while(p > 0):
        start_time = time.time()
        testy(int(l))
        print("Czas dzialania programu: %s sekund." % (time.time() - start_time))
        print("\n")
        p = p - 1

pomiar(l,p)