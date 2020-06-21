from collections import defaultdict
                                        
class Gramatica():
    def __init__(self, gramatica):

        firstset.clear()
        followset.clear()
        selecttset.clear()
        tabla.clear()

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

        #for regla in self.producciones:
         #   regla[1] = regla[1].replace(" ","")        #saco los espacios de la gramatica                     
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

        """"esLL1 = self.isLL1()
        #if (esLL1): 
            print("La gramatica ES LL(1)")
            print('La tabla generada para la gramatica es la siguiente:')
            print(' ')
            cadena = "(n,n)"
            derivacion = self.parse(cadena)
            print(' ')
            if (derivacion.split("=> ")[-1] == cadena):
                print("La cadena '" + cadena +"' PUEDE ser representada mediante la gramatica propuesta  ̿(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. * ・ ｡ﾟ")
            else:
                print("La cadena '" + cadena +"' NO PUEDE ser representada mediante la gramatica propuesta  ̿(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. * ・ ｡ﾟ")
            print(' ')
            print('La cadena de derivacion de la cadena es la siguiente: ')
            print(derivacion)
            print(' ')
        else:
            print("La gramatica NO ES LL(1)")
            print(' ')"""

        pass

    def isLL1(self):
        """Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.

        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        """

        vector_reglas = []
        for keys in self.diccionario:
            for reglas in self.diccionario.get(keys):
                if (reglas[0] == keys):
                    var = str(keys) + ' -> ' + str(reglas)
                    vector_reglas.append(var)
        if (len(vector_reglas) > 0):
            print("La gramática presenta Recursión a Izquierda en las siguientes reglas: ")
            for reglas in vector_reglas: 
                print(reglas)
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
            Conjunto_First.append(no_ter) #si nos llega un terminal como paramentro, lo agregamos directamente al Conjunto_First
        else:
            for i in self.diccionario[no_ter]:  #Recorremos las reglas del no terminal
                lista = i.split(" ")
                if (len(lista)>1):
                    i = lista[0]
                x = 0
                if((i[0] in self.terminales) or (i in self.terminales)): 
                    if (len(i) == 1):
                        Conjunto_First.extend(i[0]) #si el primer simbolo es un terminal lo añadimos directamente al First
                    else:
                        if (i == 'lambda'):                                             
                            if(('lambda' not in Conjunto_First)):
                                Conjunto_First.append(i) #Agregamos lambda al Conjunto_First
                        else:
                            Conjunto_First.append(i)
                else:
                    length=len(lista)                   
                    while(x<length): #Recorremos el consecuente completo  
                        i = lista[x]                       
                        if (i in self.terminales):
                            Conjunto_First.append(i) #Si es terminal, lo agregamos al conjunto first
                            x += 1
                            break
                        else:
                            if('lambda' in self.diccionario[i]):#Si lambda se encuentra entre los consecuentes del No_Terminal evaluado 
                                if (i != no_ter): #Para evitar la recursion izq. preguntamos si el No Terminal es distinto al que estamos evaluando
                                    Conjunto_First.extend(self.first(i))
                                    if ('lambda' in Conjunto_First):
                                        if (('lambda' in firstset[i]) and (i != lista[-1])):
                                            Conjunto_First.remove('lambda')
                                x += 1
                            else:
                                if (no_ter != i):      #Para evitar la recursion izq                   
                                    Conjunto_First.extend(self.first(i)) #Llamamos al metodo First, pero con otro No Terminal
                                    if ('lambda' in Conjunto_First):
                                        if (('lambda' in firstset[i]) and (i != lista[-1])):
                                            Conjunto_First.remove('lambda')
                                            x += 1
                                            Conjunto_First.extend(self.first(i))
                                else:
                                    for j in self.diccionario[no_ter]: #Por cada consecuente del no terminal
                                        if (j[0] != no_ter): #Para evitar la recursion izq
                                            Conjunto_First.extend(self.first(j[0]))
                                break
        if (no_ter[0].isupper()): #Puede suceder (debido a como planteamos los follows) que llegue como parametro un terminal
            firstset[no_ter]=Conjunto_First 
        return Conjunto_First


    def follow(self, no_ter):
        Confjunto_Follow = []               
        axioma = list(self.diccionario.keys())[0]
        if(no_ter==axioma): 
            Confjunto_Follow.extend('$')
        for key in self.diccionario.keys():
            elemento = self.diccionario[key]
            for each in elemento:
                lista = each.split(" ")
                if (len(lista)>1):
                    each = lista[0]
                ctr=0
                length=len(lista)
                for j in lista:
                    if(j==no_ter):
                        if(ctr<length-1):
                            if((no_ter != key)and('lambda'in self.first(lista[ctr+1]))):
                                for x in self.first(lista[ctr+1]):
                                    if((x not in Confjunto_Follow)and(x!='lambda')):
                                        Confjunto_Follow.append(x)
                                for x in self.follow(key):
                                    if((x not in Confjunto_Follow)and(x!='lambda')):
                                        Confjunto_Follow.append(x)
                            else:
                                for x in self.first(lista[ctr+1]):
                                    if((x not in Confjunto_Follow)and(x!='lambda')):
                                        Confjunto_Follow.append(x)
                        if((no_ter != key)and(ctr==length-1)):
                            for x in self.follow(key):
                                if((x not in Confjunto_Follow)and(x!='lambda')):
                                    Confjunto_Follow.append(x)
                    ctr+=1
                ctr=0
        followset[no_ter]=Confjunto_Follow
        return Confjunto_Follow


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
        if (self.isLL1() == False):
            return None


        for i in self.no_terminales:
            self.armarTabla(i)
        self.printTabla()

        axioma = self.no_terminales[0]
        derivacion = ""
        pila = []
        
        pila.append("$")
        pila.append(axioma)

        indice = 0
        lista = cadena.split(" ")
        
        while len(pila) > 0:
            tope = pila[len(pila)-1] #sacamos la variable de encima de la pila
            lookahead = lista[indice]
            if tope == lookahead: #si la variable de encima de la pila coincide con lo que nos llega en la cadena,
                pila.pop()              #se elimina de la pila
                indice = indice + 1	    #incrementamos el indice para leer el siguiente look-a-head
            else:	
                key = tope             
                if ((key in self.terminales) or (lookahead not in tabla[key])): #si lo que esta en el tope de la pila es terminal o lo que leemos
                    #bandera = False		                                        #de la cadena no se encuentra en la tabla, la cadena no pertenece
                    break                                                       #a la gramatica
                value = tabla[key][lookahead]
                
                elemento = value[0].split(" -> ") #nos quedamos con el consecuente de la regla

                if(derivacion == ""):
                    derivacion = elemento[0]+ "=>" +elemento[1]
                else:                   
                    derivacion2 = derivacion.split("=>")[-1]
                    derivacion += "=>"         
                    reemplazo = elemento[0].replace(" ","")
                    if (elemento[1] != 'lambda'):
                        a = elemento[1]
                    else:
                        a = ""                      
                    derivacion2 = derivacion2.replace(reemplazo,a, 1)
                    derivacion += str(derivacion2)                

                if elemento[1] != 'lambda':
                    pila.pop() 
                    if (len(lista[indice]) > 1) and (elemento[1] == lookahead): #ASI ESTABA ANTES Y PASABAN COSAS (lookahead in elemento[1]):
                        pila.append(lookahead)  
                    else:
                        lista2 = elemento[1].split(" ")
                        i = len(lista2) - 1 
                        while (i >= 0): #agregamos el consecuente de a un simbolo en la pila (de atras hacia adelante) 
                            pila.append(lista2[i])
                            i -= 1          
                else:
                    pila.pop()
        b = True
        longitud = len(derivacion)
        while b == True:           
            if (derivacion[longitud-1] == ' '): #Muchas derivaciones en lambda pueden dejar espacios al final de la cadena de derivacion
                derivacion = derivacion[:-1]
                longitud -= 1
            else:
                b = False

        derivacion = derivacion.replace("  "," ")
        return derivacion

    def armarTabla(self, ip): #id X
        for i in self.diccionario[ip]: 
            lista = i.split(" ")
            aux = i
            if (len(lista)>1):
                i = lista[0]
            if (ip not in tabla): 
                tabla[ip] = {}
            if i in self.terminales and i !='lambda':
                if i not in tabla[ip]:      
                    tabla[ip][i]=[]
                tabla[ip][i].append(str(ip +" -> "+ aux))
            elif i == 'lambda':
                for k in followset[ip]:
                    if k not in tabla[ip]: 
                        tabla[ip][k]=[]
                    tabla[ip][k].append(str(ip +" -> "+ aux))
            else: # es un no terminal
                for k in firstset[ip]:
                    if (k != 'lambda'):
                        if k not in tabla[ip]: 
                            tabla[ip][k]=[]
                        tabla[ip][k].append(str(ip + " -> "+ aux))
                    else: #si es lambda, nos tenemos que fijar cual regla es.
                        for k in followset[ip]:
                            if (k not in tabla[ip]): 
                                tabla[ip][k]=[]
                            if (lista[-1] == i):   
                                tabla[ip][k].append(str(ip +" -> "+ aux))
              
       
    def printTabla(self):
        for i in tabla:
            for j in tabla[i]:
                for k in tabla[i][j]:
                    print(i,":",j,":",k)
        

firstset = {}
followset = {}
selecttset = {}
tabla = {}


if __name__ == "__main__":
    gramatica = Gramatica("S:A b B a\nS:d\nA:C A b\nA:B\nB:g S d\nB:lambda\nC:a\nC:e d")
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
    #11) S:A b B a\nS:d\nA:C A b\nA:B\nB:g S d\nB:lambda\nC:a\nC:e d ---> ES LL(1)
    #12) S:A B\nA: a A\nA:c\nA:lambda\nB:b B\nB:d
    #13) S:( L )\nS:n\nL:S X\nX:, S X\nX:lambda

    """ PROBLEMAS QUE FALTAN SOLUCIONAR EN LOS FIRST:
            1) En la G de ejemplo del TP, hay un X -> A y A no aparece del lado de los antecedentes. AHI ROMPE
            2) En la gramatica 10, en los Fi de F, aparecen 2 'a' y tiene que aparecer una.
                Igualmente, resuelve bien que no es LL(1)
            3) No anda con por ejemplo: Ab -> c [S:c X\nX:Ab X\nX:lambda\nAb:a b] SI TENEMOS NO TERMINALES CON MAS DE UNA LETRA NO ANDA

        COMENTARIOS:
            4) Comentar follow y armartabla
    """