import matplotlib.pyplot as plt
#import numpy as np
from numpy import linspace
from numpy import arange
import math
import string
import random
from scipy.stats import qmc
import time
import os
import re

class Funktion:
    def __init__(self,funktion,dimensionen):
        self.funktion = funktion
        self.dimensionen = dimensionen

    def wertBerechnen(self,punkt):
        tmp = string.ascii_lowercase
        for _ in range(self.dimensionen-1):
            exec(str(tmp[_])+"=punkt[_]")
        return eval(self.funktion)

def konvergenzDirekteMcIntegration(funktion,grenzen,anzahlStützen,exakterWert):
    x = []
    y = []
    summe = 0
    for i in range(anzahlStützen):
        x.append(i)
        punkt = []
        for j in grenzen:
            punkt.append(random.uniform(j[0],j[1]))
        summe += funktion.wertBerechnen(punkt)
        integral = summe
        for j in grenzen:
            integral *= j[1]-j[0]

        integral /= i+1
        y.append(integral)
    plt.plot(x,y)
    plt.axhline(y=exakterWert,label="y="+str(exakterWert),color="black")
    plt.grid(alpha=.4,linestyle="--")
    plt.xlabel("Anzahl der Stützstellen")
    plt.ylabel("Approximierter Wert")
    plt.legend(loc="upper left")
    if len(grenzen)==1:
        plt.title("Konvergenz: $f(a)="+funktion.funktion+"$; Intervall ["+str(grenzen[0][0])+";"+str(grenzen[0][1])+"]")
    else:
        plt.title("Konvergenz: $"+funktion.funktion+"$")

    plt.savefig("konvergenz.png")
    plt.show()

def konvergenzHitOrMiss(funktion,grenzen,grenzeFunktion,anzahlStützen,exakterWert):
    x = []
    y = []
    hit = 0
    _abs = abs
    for i in range(1,anzahlStützen+1):
        x.append(i)
        punkt = []
        for j in grenzen:
            punkt.append(random.uniform(j[0],j[1]))

        if _abs(funktion.wertBerechnen(punkt))>=_abs(random.uniform(0,grenzeFunktion)):
            hit += 1
        ergebnis = hit/i
        for j in grenzen:
            ergebnis *= j[1]-j[0]
        ergebnis *= grenzeFunktion
        y.append(ergebnis)
    plt.plot(x,y)
    plt.axhline(y=exakterWert,label="y="+str(exakterWert),color="black")
    plt.grid(alpha=.4,linestyle="--")
    plt.xlabel("Anzahl der Punkte")
    plt.ylabel("Approximierter Wert")
    plt.legend(loc="upper left")
    if len(grenzen)==1:
        plt.title("Konvergenz: $f(a)="+funktion.funktion+"$; Intervall ["+str(grenzen[0][0])+";"+str(grenzen[0][1])+"]")
    else:
        plt.title("Konvergenz: $"+funktion.funktion+"$")

    plt.savefig("konvergenz.png")
    plt.show()

def mcDirektZeit(funktion,grenzen,zeit,quasi=False):
    summe = 0
    anzahlStützen = 0
    if quasi:
        sampler = qmc.Sobol(d=funktion.dimensionen-1)
    
        lowerBounds = []
        upperBounds = []
        for i in grenzen:
            lowerBounds.append(i[0])
            upperBounds.append(i[1])

    start = time.time()
    while time.time()-start<zeit:
        anzahlStützen += 1
        punkt = []
        if quasi:
                punktTmp = sampler.random(1)
                punkt=qmc.scale(punktTmp,lowerBounds,upperBounds)
        else:
            for i in grenzen:
                punkt.append(random.uniform(i[0],i[1]))
            
        if not quasi:
            summe += funktion.wertBerechnen(punkt)
        else:
            summe += funktion.wertBerechnen(punkt[0])
    for i in grenzen:
        summe *= i[1]-i[0]
    summe /= anzahlStützen
    return summe

def direkteMcIntegration(funktion,grenzen,anzahlStützen,quasi=False):
    summe = 0
    if quasi:
        sampler = qmc.Sobol(d=funktion.dimensionen-1)
        lowerBounds = []
        upperBounds = []
        for i in grenzen:
            lowerBounds.append(i[0])
            upperBounds.append(i[1])
        
        punkte = sampler.random(anzahlStützen)
        punkte = qmc.scale(punkte,lowerBounds,upperBounds)
        for punkt in punkte:
            summe += funktion.wertBerechnen(punkt)
    else:
        for i in range(anzahlStützen):
                punkt = []
                for i in grenzen:
                    punkt.append(random.uniform(i[0],i[1]))
                summe += funktion.wertBerechnen(punkt)
    ergebnis = summe
    for i in grenzen:
        ergebnis *= i[1]-i[0]
    ergebnis /= anzahlStützen
    return ergebnis

def hitOrMiss(funktion,grenzen,grenzeFunktion,anzahlPunkte):
    hit = 0
    _abs = abs
    for i in range(anzahlPunkte):
        punkt = []
        for i in grenzen:
            punkt.append(random.uniform(i[0],i[1]))
        if _abs(funktion.wertBerechnen(punkt))>=_abs(random.uniform(0,grenzeFunktion)):
            hit += 1
    ergebnis = hit/anzahlPunkte

    for i in grenzen:
        ergebnis *= i[1]-i[0]
    return ergebnis*grenzeFunktion

def hitOrMiss2d(funktion,anzahlPunkte,grenzeUnten,grenzeOben,grenzeFunktion,quasi=False):
    xHit = []
    yHit = []
    xMiss = []
    yMiss = []
    _abs = abs
    if quasi:
        lowerBounds = [grenzeUnten,0]
        upperBounds = [grenzeOben,grenzeFunktion]
        sobol = qmc.Sobol(2)
        #anzahlPunkteLog = math.ceil(math.log(anzahlPunkte,2))
        #anzahlPunkte = 2**anzahlPunkteLog
        #punkte = sobol.random_base2(anzahlPunkteLog)
        punkte = sobol.random(anzahlPunkte)

        punkte = qmc.scale(punkte,lowerBounds,upperBounds)
        for punkt in punkte:
            if _abs(funktion.wertBerechnen([punkt[0]]))>= _abs(punkt[1]):
                xHit.append(punkt[0])
                yHit.append(punkt[1])
            else:
                xMiss.append(punkt[0])
                yMiss.append(punkt[1])
    else:
        for i in range(anzahlPunkte):
            x = random.uniform(grenzeUnten,grenzeOben)
            y = random.uniform(0,grenzeFunktion)
            if _abs(funktion.wertBerechnen([x]))>= _abs(y):
                xHit.append(x)
                yHit.append(y)
            else:
                xMiss.append(x)
                yMiss.append(y)
    plt.plot(xHit,yHit,".",color="green")
    plt.plot(xMiss,yMiss,".",color="red")

    plt.xlabel("x-Achse (Intervall: ["+str(grenzeUnten)+"; "+str(grenzeOben)+"])")
    plt.ylabel("y-Achse")
    plt.title("Punkte: "+str(anzahlPunkte)+'; Hit: '+str(len(xHit))+"; $\int_{"+str(grenzeUnten)+"}^{"+str(grenzeOben)+"}f(x)dx\\approx"+str(round(len(xHit)/anzahlPunkte*((grenzeOben-grenzeUnten)*grenzeFunktion),2))+"$",fontweight="bold")
    xFunktion = linspace(grenzeUnten,grenzeOben,(grenzeOben-grenzeUnten)*10)
    yFunktion = []
    for i in xFunktion:
        yFunktion.append(funktion.wertBerechnen([i]))
    plt.plot(xFunktion,yFunktion,label=str(funktion.funktion))
    plt.legend(loc="upper left")
    plt.grid(alpha=.4,linestyle="--")
    plt.savefig('hitOrMiss.png')
    plt.show()

def direkteMcIntegration2d(funktion,anzahlStellen,grenzeUnten,grenzeOben,quasi=False):
    xStellen = []
    summe = 0
    if quasi:
        sobol = qmc.Sobol(1)
        #anzahlPunkteLog = math.ceil(math.log(anzahlStellen,2))
        #anzahlStellen = 2**anzahlPunkteLog
        #punkte = sobol.random_base2(anzahlPunkteLog)
        punkte = sobol.random(anzahlStellen)
        punkte = qmc.scale(punkte,[grenzeUnten],[grenzeOben])
        for punkt in punkte:
            xStellen.append(punkt[0])
            summe += funktion.wertBerechnen([punkt[0]])
        print(type(summe))
    else:
        for i in range(anzahlStellen):
            x = random.uniform(grenzeUnten,grenzeOben)
            xStellen.append(x)
            summe += funktion.wertBerechnen([x])
    
    for x in xStellen:
        plt.vlines(x = x, ymin = 0, ymax = funktion.wertBerechnen([x]),colors = 'purple')
    plt.xlabel("x-Achse (Intervall: ["+str(grenzeUnten)+"; "+str(grenzeOben)+"])")
    plt.ylabel("y-Achse")
    xFunktion = linspace(grenzeUnten,grenzeOben,(grenzeOben-grenzeUnten)*10)
    yFunktion = []
    for i in xFunktion:
        yFunktion.append(funktion.wertBerechnen([i]))
    plt.plot(xFunktion,yFunktion,label=str(funktion.funktion))
    plt.legend(loc="upper left")
    plt.title("Punkte: "+str(anzahlStellen)+'; $\sum_{i=1}^N f(x_i)$= '+str(round(summe,2))+"; $\int_{"+str(grenzeUnten)+"}^{"+str(grenzeOben)+"}f(x)dx\\approx"+str(round(summe/anzahlStellen*(grenzeOben-grenzeUnten),2))+"$",fontweight="bold")
    plt.grid(alpha=.4,linestyle="--")
    plt.savefig('direkteMcIntegration.png')
    plt.show()


def piDirekt(zeit):
    start = time.time()
    ergebnis = 0
    counter = 0
    while(time.time()-start<zeit):
        counter += 1
        ergebnis += math.sqrt(1-(random.uniform(0,1)**2))
    ergebnis /= counter
    return round(ergebnis*4,7),round(abs(math.pi-ergebnis*4),7),counter

def piHitOrMiss(zeit):
    start = time.time()
    hit = 0
    counter = 0
    while(time.time()-start<zeit):
        counter += 1
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        if x**2+y**2<=1:
            hit += 1
    hit /= counter
    return round(hit*4,7),round(abs(math.pi-hit*4),7),counter

def gaußverteilung(funktion,grenzen,anzahlStützstellen,anzahlSimulationen):
    werte = []
    for i in range(anzahlSimulationen):
        werte.append(direkteMcIntegration(funktion,grenzen,anzahlStützstellen))

    plt.hist(werte,bins=arange(min(werte), max(werte) + 5, 5))
    plt.title(str(anzahlSimulationen)+" Approximationen mit jeweils "+str(anzahlStützstellen)+" Stichproben")
    plt.xlabel("Approximation")
    plt.ylabel("Häufigkeit der Approximationen")
    plt.savefig('histogramm.png')
    plt.show()

#Der Code ab hier ist für die Eingabe des Benutzers
if __name__ == "__main__":
    
    def cls():
        os.system('cls' if os.name=='nt' else 'clear')
    
    def standardAbfrage(hitOrMiss=False,quasizufallszahlen=False):
            variablen = input("Anzahl an Variablen: ")
            variablen = int(variablen)
            funktion = Funktion(input("Funktion (in Pythonschreibweise, Variablen in der Reihenfolge des Alphabets): "),variablen+1)
            grenzen = []
            for i in range(variablen):
                a = int(input("untereGrenze von Variable "+ str(i+1) + ": "))
                b = int(input("obereGrenze von Variable "+ str(i+1) + ": "))
                grenzen.append([a,b])
            if hitOrMiss:
                funktionsGrenze = int(input("Das Maximum im Integrationsbereich: "))
            stichproben = int(input("Anzahl der Stichproben: "))
            if quasizufallszahlen:
                quasi = input("Quasi-Zufallszahlen? (j/n): ")
                if quasi == "j":
                    quasi = True
                else:
                    quasi = False
            if hitOrMiss and quasizufallszahlen:
                return funktion, grenzen, funktionsGrenze, stichproben, quasi
            elif hitOrMiss:
                return funktion, grenzen, funktionsGrenze, stichproben
            elif quasizufallszahlen:
                return funktion, grenzen, stichproben, quasi
            else:
                return funktion, grenzen, stichproben

    cls()
    print("Bitte wähle:")
    print("--------------------")
    print("1 direkteMcIntegration")
    print("2 hitOrMiss")
    print("3 mcDirektZeit")
    print("4 hitOrMiss2d")
    print("5 direkteMcIntegration2d")
    print("6 konvergenzDirekteMcIntegration")
    print("7 konvergenzHitOrMiss")
    print("8 piDirekt")
    print("9 piHitOrMiss")
    print("10 Gaußverteilung")
    print("Um zu erfahren was die Funktionen machen gebe 'help' ein.")
    print("--------------------")
    eingabe = input("Nummer eingeben: ")
    if eingabe == "help":
        cls()
        print("""direkteMcIntegration
Input: Die Funktion, Integrationsgrenzen, Anzahl der Stützstellen, Quasi
Output: Approximiert mit der gegeben Anzahl an Stützstellen das Integral mit der
        direkten MC-Integration und gibt das Ergebnis zurück. Wenn Quasi gleich True ist werden
        Quasi-Zufallszahlen verwendet.\n""")
        print("""hitOrMiss
Input: Die Funktion, Integrationsgrenzen, höchster Funktionswert in dem Integrationsbereich,Anzahl der Punkte
Output: Approximiert mit dem hitOrMiss Verfahren den Wert des Integrals und gibt dieApproximation zurück. Es werden so viele Zufallspunkte generiert wie es in dem Inputangegeben""")
        print("""\nmcDirektZeit
Input: Die Funktion, Integrationsgrenzen, Zeit (in Sekunden), Quasi
Output: Approximiert Zeit lang das Integral der Funktion und gibt am Ende das Ergebnis zurück. 
        Wenn Quasi gleich True ist werden Quasi-Zufallszahlen verwendet.""")
        print("""\nhitOrMiss2d
Input: Die Funktion, Anzahl der Punkte, untere Integrationsgrenze, obere Integrationsgrenze, höchster Funktionswert in dem Integrationsbereich, Quasi
Output: Hit-Or-Miss Integration für eine Funktion mit einer Variable mit der gegebenen
        Anzahl an Punkten. Die Ergebnisse werden Grafisch dargestellt und in einer Datei namens
        hitOrMiss.png gespeichert. Wenn Quasi gleich T rue ist werden Quasi-Zufallszahlen verwendet.""")
        print("""\ndirekteMcIntegration2d
Input: Die Funktion, Anzahl der Punkte, untere Integrationsgrenze, obere Integrationsgrenze, Quasi
Output: Das selbe wie hitOrMiss2d, mit dem Unterschied dass die direkte MC-Integration
        benutzt wird anstatt dem hitOrMiss Verfahren.""")
        print("""\nkonvergenzDirekteMcIntegration
Input: Die Funktion, Integrationsgrenzen, Anzahlstützen, exakter Wert des Integrals
Output: Erstellt eine Grafik namens Konvergenz.png. Die Grafik zeigt einen Graphen,
        bei welcher die x-Achse die Anzahl der benutzten Stützstellen angibt und die y-Achse die
        Approximation des Integrals. Zum approximieren wird die direkte MC-Integration mit
        Pseudozufallszahlen verwendet. Außerdem ist der angegebene exakte Wert des Integrals
        als Gerade im Graphen gekennzeichnet.""")
        print("""\nkonvergenzHitOrMiss
Input: Die Funktion, Integrationsgrenzen, höchster (oder niedrigster) Funktionswert in dem Integrationsbereich ,Anzahlstützen, exakter Wert des Integrals
Output: Genau das selbe wie bei konvergenzDirekteMcIntegration, nur mit dem Unterschied
        dass das hit-or-miss Verfahren anstatt der direkten MC-Integration verwendet wird.""")
        print("""\npiDirekt
Input: Zeit (in Sekunden)
Output: Approximiert Pi mit der direkten MC-Integrations. Der Input Zeit gibt an wie
        lange die Approximierung läuft. Gibt die Approximation, den Fehler und die Anzahl der
        gemachten Stichproben zurück.""")
        print("""\npiHitOrMiss
Input: Zeit (in Sekunden)
Output: Das selbe wie piDirekt, mit dem Unterschied dass das HitOrMiss Verfahren
        verwendet wird.""")
        input("\nEnter drücken um das Programm zu verlassen...")
        print("""\nGaußverteilung
Input: Funktion, Grenzen, anzahlSimulationen, stichprobenProSimulation
Output: Erstellt ein Histogramm welches auf der x-Achse die Approximationen zeigt und
        auf der y-Achse die Häufigkeiten der Approximation.""")
        input("\nEnter drücken um das Programm zu verlassen...")
    else:
        cls()
        if not re.match("[1-9]$|10",eingabe):
            print("Ungültige Eingabe")
        eingabe = int(eingabe)
        
        if eingabe == 1:
            funktion, grenzen, anzahlStützstellen, quasi = standardAbfrage(quasizufallszahlen=True)
            print("Ergebnis: "+ str(direkteMcIntegration(funktion,grenzen,anzahlStützstellen,quasi)))
        elif eingabe == 2:
            funktion, grenzen, funktionsgrenze, anzahlPunkte = standardAbfrage(True)
            print("Ergebnis: "+ str(hitOrMiss(funktion,grenzen,funktionsgrenze,anzahlPunkte)))
        elif eingabe == 3:
            variablen = input("Anzahl an Variablen: ")
            variablen = int(variablen)
            funktion = Funktion(input("Funktion (in Pythonschreibweise, Variablen in der Reihenfolge des Alphabets): "),variablen+1)
            grenzen = []
            for i in range(variablen):
                a = int(input("untereGrenze von Variable "+ str(i+1) + ": "))
                b = int(input("obereGrenze von Variable "+ str(i+1) + ": "))
                grenzen.append([a,b])
            zeit = int(input("Zeit (in sekunden): "))
            quasi = input("Quasi-Zufallszahlen? (j/n): ")
            if quasi == "j":
                quasi = True
            else:
                quasi = False
            print("Ergebnis: "+str(mcDirektZeit(funktion,grenzen,zeit,quasi)))
        elif eingabe == 4:
            funktion = Funktion(input("Funktion (in Pythonschreibweise): "),2)
            stichproben = int(input("Anzahl der Stichproben: "))
            untereGrenze = int(input("Untere Integrationsgrenze: "))
            obereGrenze = int(input("Obere Integrationsgrenze: "))
            funktionsgrenze = int(input("Maximum im Integrationsbereich: "))
            quasi = input("Quasi-Zufallszahlen? (j/n): ")
            if quasi == "j":
                quasi = True
            else:
                quasi = False
            hitOrMiss2d(funktion,stichproben,untereGrenze,obereGrenze,funktionsgrenze,quasi)
        elif eingabe == 5:
            funktion = Funktion(input("Funktion (in Pythonschreibweise): "),2)
            stichproben = int(input("Anzahl der Stichproben: "))
            untereGrenze = int(input("Untere Integrationsgrenze: "))
            obereGrenze = int(input("Obere Integrationsgrenze: "))
            quasi = input("Quasi-Zufallszahlen? (j/n): ")
            if quasi == "j":
                quasi = True
            else:
                quasi = False
            direkteMcIntegration2d(funktion,stichproben,untereGrenze,obereGrenze,quasi)
        elif eingabe == 6:
            variablen = input("Anzahl an Variablen: ")
            variablen = int(variablen)
            funktion = Funktion(input("Funktion (in Pythonschreibweise, Variablen in der Reihenfolge des Alphabets): "),variablen+1)
            grenzen = []
            for i in range(variablen):
                a = int(input("untereGrenze von Variable "+ str(i+1) + ": "))
                b = int(input("obereGrenze von Variable "+ str(i+1) + ": "))
                grenzen.append([a,b])
            stichproben = int(input("Anzahl der Stützstellen: "))
            exakt = float(input("Exakter Wert des Integrals: "))
            konvergenzDirekteMcIntegration(funktion,grenzen,stichproben,exakt)
        elif eingabe == 7:
            variablen = input("Anzahl an Variablen: ")
            variablen = int(variablen)
            funktion = Funktion(input("Funktion (in Pythonschreibweise, Variablen in der Reihenfolge des Alphabets): "),variablen+1)
            grenzen = []
            for i in range(variablen):
                a = int(input("untereGrenze von Variable "+ str(i+1) + ": "))
                b = int(input("obereGrenze von Variable "+ str(i+1) + ": "))
                grenzen.append([a,b])
            funktionsgrenze = int(input("Maximum (oder Minimum) im Integrationsbereich: "))
            stichproben = int(input("Anzahl der Stichproben: "))
            exakt = float(input("Exakter Wert des Integrals: "))
            konvergenzHitOrMiss(funktion,grenzen,funktionsgrenze,stichproben,exakt)
        elif eingabe == 8:
            zeit = int(input("Zeit (in Sekunden): "))
            ergebnis = piDirekt(zeit)
            print("Approximation: " + str(ergebnis[0]))
            print("Fehler: " + str(ergebnis[1]))
            print("Stichproben: " + str(ergebnis[2]))
        elif eingabe == 9:
            zeit = int(input("Zeit (in Sekunden): "))
            ergebnis = piDirekt(zeit)
            print("Approximation: " + str(ergebnis[0]))
            print("Fehler: " + str(ergebnis[1]))
            print("Stichproben: " + str(ergebnis[2]))
        elif eingabe == 10:
            variablen = input("Anzahl an Variablen: ")
            variablen = int(variablen)
            funktion = Funktion(input("Funktion (in Pythonschreibweise, Variablen in der Reihenfolge des Alphabets): "),variablen+1)
            grenzen = []
            for i in range(variablen):
                a = int(input("untereGrenze von Variable "+ str(i+1) + ": "))
                b = int(input("obereGrenze von Variable "+ str(i+1) + ": "))
                grenzen.append([a,b])
            approximationen = int(input("Anzahl an Approximationen: "))
            stichproben = int(input("Zufallsstichproben pro Approximation: "))
            gaußverteilung(funktion,grenzen,stichproben,approximationen)
    input("\nEnter drücken um das Programm zu verlassen...")
    cls()

