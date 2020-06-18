from collections import defaultdict
                                        
class Gramatica():
    def __init__(self, gramatica):

        
        self.gramatica = gramatica
        self.producciones = gramatica.split("\n") 

        antecedentes = [i.split(':', 1)[0] for i in self.producciones] #Obtenemos una lista con los antecedentes de la gramatica
        consecuentes = [i.split(':', 1)[1] for i in self.producciones] #Obtenemos una lista con los consecuentes de la gramatica
        self.producciones = [i.split(':', 1) for i in self.producciones] #Obtenemos una lista con todas las producciones de la gramatica
        
        self.diccionario = dict.fromkeys(antecedentes) #Creamos un diccionario con los antecedentes

        #-------------------------------------Lista de terminales de la gramatica-------------------------------------         
          
        self.terminales = [x for i in consecuentes for x in i.split(' ')] #Por cada consecuente, si esta separado por un espacio, lo dividimos con el .split(' ')
        #self.terminales = [ elem for elem in self.terminales if elem[0].islower()] #Además, colocamos en la lista de terminales solo aquellos que comiencen con letra minuscula
        vector = []
        for i in self.terminales:
            if ((i == '') or (i[0].isupper())):
                continue
            else:
                vector.append(i)
        self.terminales = vector
        self.terminales = list(set(self.terminales))
        self.terminales.append('$') #Agregamos el no terminal $
        print('-------------------------------------------------------------------------------------------------------------------------')
        print('Terminales: ', self.terminales)

        #-------------------------------------Lista de no terminales de la gramatica-------------------------------------

        self.no_terminales = list(dict.fromkeys(antecedentes)) 
        print('No Terminales: ', self.no_terminales)

        for regla in self.producciones:
            regla[1] = regla[1].replace(" ","")        #saco los espacios de la gramatica                     
        print("producciones: ", self.producciones)

        #-------------------------------------Realizamos un diccionario con las producciones (keys: no terminales, values: derivacion del NT)-------------------------------------

        for i in self.producciones: 
            if (self.diccionario[i[0]] == None): #Si el diccionario cuya key es i[0] está vacio:                 
                self.diccionario[i[0]] = [i[1]]  #agregamos el consecuente de la "key" directamente                 
            else:
                self.diccionario[i[0]].append(i[1]) #sino, insertamos el consecuente a la lista con un append. Esto se debe a que no podemos hacer
                                                    #un append a algo None
        
        print('Diccionario: ', self.diccionario) 
        print('-------------------------------------------------------------------------------------------------------------------------')

        #-------------------------------------Llamar al metodo isLL1-------------------------------------

        esLL1 = self.isLL1()
        if (esLL1): 
            print(esLL1, " La gramatica es LL(1)")
            print('La tabla generada para la gramatica es la siguiente:')
            print(' ')
            self.parse("b")
        else:
            print(esLL1, " La gramatica NO es LL(1)")

        pass

    def isLL1(self):
        """Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.

        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        """
        for keys in self.diccionario:
            for reglas in self.diccionario.get(keys):
                if (reglas[0] == keys):
                    print("La gramática no es LL(1), debido a que presenta Recursión a Izquierda.")
                    return False
        
        for i in self.no_terminales:
            Fi=self.first(i)            
            firstset[i]=Fi
            Fo=self.follow(i)
            followset[i]=Fo

        selectlist = []
        x = 0
        for key in firstset.keys():
            selectlist = list(firstset[key])
            if ('lambda' in firstset[key]):
                selectlist.remove('lambda')
                listafollows = list(followset[key])
                for i in listafollows:
                    selectlist.append(i)    
            selecttset[key] = selectlist
            x += 1

        print('FIRSTS: ', firstset)
        print('FOLLOWS: ' , followset)        
        print('SELECTS: ', selecttset)
        print('-------------------------------------------------------------------------------------------------------------------------')

        EsLL1 = True
        for key in selecttset.keys():
            if (len(selecttset[key]) != len(set(selecttset[key]))):
                EsLL1 = False
                break

        return EsLL1

    def first(self, no_ter): #no_ter es un string
        Conjunto_First=[] 
        length=0
        x=0 
        if(no_ter in self.terminales):   
            Conjunto_First.extend(no_ter) #si nos llega un terminal como paramentro, lo agregamos directamente al Conjunto_First
        else:
            for i in self.diccionario[no_ter]:  #Recorremos las reglas del no terminal
                x = 0
                if((i[0] in self.terminales) or (i == 'lambda')): 
                    if (i != 'lambda'):
                        Conjunto_First.extend(i[0]) #si el primer simbolo es un terminal lo añadimos directamente al First
                    else:                                             
                        if(('lambda' not in Conjunto_First)):
                            Conjunto_First.append('lambda') #Agregamos lambda al Conjunto_First
                else:
                        length=len(i)
                        while(x<length): #Recorremos el consecuente completo
                            if (i[x] in self.terminales):
                                Conjunto_First.extend(i[x]) #Si es terminal, lo agregamos al conjunto first
                                x += 1
                            else:
                                if('lambda' in self.diccionario[i[x]]):#Si lambda se encuentra entre los consecuentes del No_Terminal evaluado 
                                    if (i[x] != no_ter): #Para evitar la recursion izq. preguntamos si el No Terminal es distinto al que estamos evaluando
                                        Conjunto_First.extend(self.first(i[x]))
                                        #x+=1
                                    x += 1
                                else:
                                    if (no_ter != i[x]):      #Para evitar la recursion izq                   
                                        Conjunto_First.extend(self.first(i[x])) #Llamamos al metodo First, pero con otro No Terminal
                                    else:
                                        for j in self.diccionario[no_ter]: #Por cada consecuente del no terminal
                                            if (j[0] != no_ter): #Para evitar la recursion izq
                                                Conjunto_First.extend(self.first(j[0]))
                                    break
        if (no_ter.isupper()): #Puede suceder (debido a como planteamos los follows) que llegue como parametro un terminal
            firstset[no_ter]=Conjunto_First 
        return Conjunto_First


    def follow(self, no_ter):
        fo = []
        axioma = list(self.diccionario.keys())[0]
        if(no_ter==axioma): 
            fo.extend('$')
        for key in self.diccionario.keys():
            vals=self.diccionario[key]
            for each in vals:
                ctr=0
                length=len(each)
                for j in each:
                    if(j==no_ter):
                        if(ctr<length-1):
                            if((no_ter != key)and('lambda'in self.first(each[ctr+1]))):
                                for x in self.first(each[ctr+1]):
                                    if((x not in fo)and(x!='lambda')):
                                        fo.extend(x)
                                for x in self.follow(key):
                                    if((x not in fo)and(x!='lambda')):
                                        fo.extend(x)
                            else:
                                for x in self.first(each[ctr+1]):
                                    if((x not in fo)and(x!='lambda')):
                                        fo.extend(x)
                        if((no_ter != key)and(ctr==length-1)):
                            for x in self.follow(key):
                                if((x not in fo)and(x!='lambda')):
                                    fo.extend(x)
                    ctr+=1
                ctr=0
        followset[no_ter]=fo
        return fo


    def parse(self, cadena):
        """Retorna la derivación para una cadena dada utilizando las
           producciones de la gramática y los conjuntos de Fi, Fo y Se
           obtenidos previamente.
        Parameters
        ----------
        cadena : string
            Cadena de entrada.

            Ejemplo:
            babc

        Returns
        -------
        derivacion : string
            Representación de las reglas a aplicar para derivar la cadenas
            utilizando la gramática.
        """
        for i in self.no_terminales:
            self.armarTabla(i)
        self.printTabla()

        EsValidaLaCadena = self.ParsearCadena(cadena)
        if (EsValidaLaCadena):
            print ("La cadena es aceptada :)")
        else:
            print ("La cadena NO es aceptada :(")
        pass

    def armarTabla(self, ip):
        for i in self.diccionario[ip]: 
            if ip not in tabla: 
                tabla[ip]={}
            if i[0] in self.terminales and i !='lambda':
                if i[0] not in tabla[ip]:
                    tabla[ip][i[0]]=[]
                tabla[ip][i[0]].append(str(ip +" -> "+ i))
            elif i == 'lambda':
                for k in followset[ip]:
                    if k not in tabla[ip]: 
                        tabla[ip][k]=[]
                    tabla[ip][k].append(str(ip +" -> "+ i))
            else:
                for k in firstset[ip]:
                    if k not in tabla[ip]: 
                        tabla[ip][k]=[]
                    tabla[ip][k].append(str(ip + " -> "+i))
        

    def printTabla(self):
        for i in tabla:
            for j in tabla[i]:
                for k in tabla[i][j]:
                    print(i,":",j,":",k)


    def ParsearCadena(self, cadena):
        bandera = True
        cadena = cadena + "$"
        axioma = self.no_terminales[0]

        pila = []
        
        pila.append("$")
        pila.append(axioma)

        indice = 0
        
        while len(pila) > 0:
            tope = pila[len(pila)-1] #sacamos la variable de encima de la pila
            print ("Tope =>",tope)
            lookahead = cadena[indice]
            print ("Lookahead => ",lookahead)
            if tope == lookahead: #si la variable de encima de la pila coincide con lo que nos llega en la cadena,
                pila.pop()              #se elimina de la pila
                indice = indice + 1	    #incrementamos el indice para leer el siguiente look-a-head
            else:	
                key = tope             
                if ((key in self.terminales) or (lookahead not in tabla[key])): #si lo que esta en el tope de la pila es terminal o lo que leemos
                    bandera = False		                                        #de la cadena no se encuentra en la tabla, la cadena no pertenece
                    break                                                       #a la gramatica
                value = tabla[key][lookahead]
                elemento = value[0].split("-> ") #nos quedamos con el consecuente de la regla
                if elemento[1] != 'lambda':
                    pila.pop()                                            
                    i = len(elemento[1]) -1 
                    while (i >= 0): #agregamos el consecuente de a un simbolo en la pila (de atras hacia adelante) 
                        pila.append(elemento[1][i])
                        i -= 1          
                else:
                    pila.pop()	
        return bandera
        

firstset = {}
followset = {}
selecttset = {}
tabla = {}

if __name__ == "__main__":
    gramatica = Gramatica("E:E + T\nE:E - T\nE:T\nT:T * F\nT:T / F\nT:F\nF:n\nF:( E )")
    #1) E:T A\nA:+ T A\nA:- T A\nA:lambda\nT:F B\nB:* F B\nB:/ F B\nB:lambda\nF:n\nF:( E ) ---> ES LL(1)
    #2) E:E + T\nE:E - T\nE:T\nT:T * F\nT:T / F\nT:F\nF:n\nF:( E ) ---> NO ES LL(1)
    #3) X:X Y\nX:e\nX:b\nX:lambda\nY:a\nY:d ---> NO ES LL(1)
    #4) X:X Y\nX:A\nX:b\nX:lambda\nY:a\nY:d\nA:r ---> NO ES LL(1)
    #5) S:A b\nS:B a\nA:a A\nA:a\nB:a ---> NO ES LL(1)
    #6) X:a S\nS:a Z\nS:b\nZ:b\nZ:a A b\nZ:lambda\nA:a A\nA:lambda ---> ES LL(1)
    #7) E:E + E\nE:E - E\nE:( E )\nE:n ---> NO ES LL(1)
    #8) S:A B c\nA:a\nA:lambda\nB:b\nB:lambda ---> ES LL(1)
    #9) S:a S e\nA:B\nA:b B e\nA:C\nB:c e\nB:f\nC:b ---> NO ES LL(1)
    #10) F:X Y\nX:a B R\nX:a C Q\nB:b\nB:d\nC:e\nC:b\nR:r\nQ:q\nY:b ---> NO ES LL(1)

    """ PROBLEMAS QUE FALTAN SOLUCIONAR EN LOS FIRST:
            1) En la G de ejemplo del TP, hay un X -> A y A no aparece del lado de los antecedentes. AHI ROMPE
            2) En la gramatica 10, en los Fi de F, aparecen 2 'a' y tiene que aparecer una.
                Igualmente, resuelve bien que no es LL(1)
            3) No anda con por ejemplo: Ab -> c [S:c X\nX:Ab X\nX:lambda\nAb:a b]
    """