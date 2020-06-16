from collections import defaultdict
                                                        #ANDA SI NO TIENE ESPACIOS EN S->' 'algo
class Gramatica():
    def __init__(self, gramatica):

        
        self.gramatica = gramatica
        producciones = gramatica.split("\n") 

        antecedentes = [i.split(':', 1)[0] for i in producciones] #Obtenemos una lista con los antecedentes de la gramatica
        consecuentes = [i.split(':', 1)[1] for i in producciones] #Obtenemos una lista con los consecuentes de la gramatica
        producciones = [i.split(':', 1) for i in producciones] #Obtenemos una lista con todas las producciones de la gramatica
        

        self.diccionario = dict.fromkeys(antecedentes) #Creamos un diccionario con los antecedentes



        #-------------------------------------Lista de terminales de la gramatica------------------------------------- 
        
          
        self.terminales = [x for i in consecuentes for x in i.split(' ')] #Por cada consecuente, si esta separado por un espacio, lo dividimos con el .split(' ')
        self.terminales = [ elem for elem in self.terminales if elem[0].islower()] #Además, colocamos en la lista de terminales solo aquellos que comiencen con letra minuscula
        self.terminales = list(set(self.terminales))
        self.terminales.append('$') #Agregamos el no terminal $
        print('Terminales: ', self.terminales)

        #-------------------------------------Lista de no terminales de la gramatica-------------------------------------

        self.no_terminales = list(dict.fromkeys(antecedentes)) 
        print('No Terminales: ', self.no_terminales)

        for regla in producciones:
            regla[1] = regla[1].replace(" ","")        #saco los espacios de la gramatica                     
        print("producciones: ", producciones)

        #-------------------------------------Realizamos un diccionario con las producciones (keys: no terminales, values: derivacion del NT)-------------------------------------

        for i in producciones: 
            if (self.diccionario[i[0]] == None): #Si el diccionario cuya key es i[0] está vacio:                 
                self.diccionario[i[0]] = [i[1]]  #agregamos el consecuente de la "key" directamente                 
            else:
                self.diccionario[i[0]].append(i[1]) #sino, insertamos el consecuente a la lista con un append. Esto se debe a que no podemos hacer
                                                    #un append a algo None
        
        print('Diccionario: ', self.diccionario) 

        #-------------------------------------Llamar al metodo isLL1-------------------------------------


        esLL1 = self.isLL1()
        if (esLL1): 
            mensaje = " La gramatica es LL(1)"
        else:
            mensaje = " La gramatica no es LL(1)"
        print(esLL1, mensaje)

        pass

    def isLL1(self):
        """Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.

        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        """
        for i in self.no_terminales:
            Fi=self.first(i)            
            firstset[i]=Fi
            Fo=self.follow(i)
            followset[i]=Fo

        print('FIRSTS :', firstset)
        print('FOLLOWS :' , followset)

        return True

    def first(self, no_ter): #no_ter es un string

        Conjunto_First=[] 
        length=0
        x=0 
        
        if(no_ter in self.terminales):   
            Conjunto_First.extend(no_ter)
        else:
            for i in self.diccionario[no_ter]:  #Recorremos las reglas del no terminal
                x = 0
                if((i[0] in self.terminales) or (i == 'lambda')):     #si el primer simbolo es un terminal, lo añadimos al conj first
                    if (i != 'lambda'):
                        Conjunto_First.extend(i[0])
                    else:                                             
                        if('lambda' not in Conjunto_First):
                            Conjunto_First.append('lambda')
                else:
                        length=len(i)
                        while(x<length):
                            if('lambda' in self.diccionario[i[x]]):
                                if (i[x] != no_ter):
                                    Conjunto_First.extend(self.first(i[x]))
                                    x+=1
                            else:                              
                                Conjunto_First.extend(self.first(i[x]))
                                break
                                

        Conjunto_First = list(set(Conjunto_First))
        if (no_ter.isupper()):
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
        devivacion : string
            Representación de las reglas a aplicar para derivar la cadenas
            utilizando la gramática.
        """
        pass

firstset = {}
followset = {}

if __name__ == "__main__":
    gramatica = Gramatica("S:b B X\nX:aAX\nX:lambda\nA:a B\nA:c\nB:d C\nC:bC\nC:lambda")