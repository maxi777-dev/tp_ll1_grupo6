from collections import defaultdict

class Gramatica():
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.producciones = gramatica.split("\n") 

        self.antecedentes = [i.split(':', 1)[0] for i in self.producciones] #Obtenemos una lista con los antecedentes de la gramatica
        self.concecuentes = [i.split(':', 1)[1] for i in self.producciones] #Obtenemos una lista con los consecuentes de la gramatica
        self.producciones = [i.split(':', 1) for i in self.producciones] #Obtenemos una lista con todas las producciones de la gramatica
        print("producciones: ", self.producciones)

        self.diccionario = dict.fromkeys(self.antecedentes) #Creamos un diccionario con los antecedentes

        '''Con el siguiente FOR completamos el diccionario, es decir, cada no terminal será una key o indice del diccionario, y seguido
        de cada no terminal tendremos una lista de todas las derivaciones de dicho no terminal''' 

        for i in self.producciones: 
            if (self.diccionario[i[0]] == None): #Si el diccionario cuya key es i[0] está vacio:                 
                self.diccionario[i[0]] = [i[1]] #agregamos el consecuente de la "key" directamente                 
            else:
                self.diccionario[i[0]].append(i[1]) #sino, incertamos el concecuente a la lista con un append. Esto se debe a que no podemos hacer
                                                    #un append a algo None
        print('Diccionario: ', self.diccionario) 

        #A continuacion vamos a confeccionar una lista con todos los terminales de la gramatica        
        self.terminales = [x for i in self.concecuentes for x in i.split(' ')] #Por cada consecuente, si esta separado por un espacio, lo dividimos con el .split(' ')
        self.terminales = [ elem for elem in self.terminales if elem[0].islower()] #Además, colocamos en la lista de terminales solo aquellos que comiencen con letra minuscula
        self.terminales.append('$') #Agregamos el no terminal $
        print('Terminales: ', self.terminales)


        self.no_terminales = list(dict.fromkeys(self.antecedentes)) #Para finalizar hacemos una lista de No Terminales, los cuales serán las keys del diccionario
        print('No Terminales: ', self.no_terminales)
        
        esLL1 = self.isLL1()
        if (esLL1):
            mensaje = " La gramatica no es LL(1)"
        else:
            mensaje = " La gramatica es LL(1)"
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
            Fo=self.follow(i)
            firstset[i]=Fi
            followset[i]=Fo
        
        print(firstset)
        print(followset)

        return True

    def first(self, no_ter):
        Conjunto_First=[]
        x=0
        length=0
        if(no_ter in self.terminales):
            Conjunto_First.extend(no_ter)
        else:
            for i in self.diccionario[no_ter]:
                if(i[0] in self.terminales):
                        Conjunto_First.extend(i[0])
                else:
                        length=len(i)
                        while(x<length):
                            if('lambda' in self.diccionario[i[x]]):
                                Conjunto_First.extend(self.first(i[x]))
                                x+=1
                            else:                              
                                Conjunto_First.extend(self.first(i[x]))
                                break
        firstset[no_ter]=Conjunto_First
        return Conjunto_First


    def follow(self, no_ter):
        foll=[]
        if(no_ter=='E'): #si es el AXIOMA
            foll.extend('$')
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
                                    if((x not in foll)and(x!='lambda')):
                                        foll.extend(x)
                                for x in self.follow(key):
                                    if((x not in foll)and(x!='lmbd')):
                                        foll.extend(x)
                            else:
                                for x in self.first(each[ctr+1]):
                                    if((x not in foll)and(x!='lambda')):
                                        foll.extend(x)
                        if((no_ter != key)and(ctr==length-1)):
                            for x in self.follow(key):
                                if((x not in foll)and(x!='lambda')):
                                    foll.extend(x)
                    ctr+=1
                ctr=0
        followset[no_ter]=foll
        return foll


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

firstset = []
followset = []

if __name__ == "__main__":
    gramatica = Gramatica("X:X Y\nX:A\nX:b\nX:lambda\nY:a\nY:d")