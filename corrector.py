import os
import sys
import importlib

files = os.listdir('.')
module_file = [f.split('.')[0] for f in files if 'grupo' in f][0]

grupo = importlib.import_module(module_file)

grammars = [
    ['S:X Y\nX:e\nX:b\nX:lambda\nY:a\nY:d', True, ('b d $', 'S=>X Y=>b Y=>b d')],
    ['S:A\nA:B A\nA:lambda\nB:a B\nB:b', True, ('a a a b $', 'S=>A=>B A=>a B A=>a a B A=>a a a B A=>a a a b A=>a a a b')],
    ['S:A B\nA:a A\nA:c\nA:lambda\nB:b B\nB:d', True, ('a a c d $', 'S=>A B=>a A B=>a a A B=>a a c B=>a a c d')],
    ['S:S C w c\nS:S D\nS:S E\nS:F\nS:F\nS:H', False, None],
    ['E:T A\nA:+ T A\nA:- T A\nA:lambda\nT:F B\nB:* F B\nB:/ F B\nB:lambda\nF:id\nF:( E )', True,('id / id $','E=>T A=>F B A=>id B A=>id / F B A=>id / id B A=>id / id A=>id / id')],
    ['DL:Dec DL´\nDL´:Dec DL´\nDL´:lambda\nDec:IdList ; Type\nIdList:id IdList´\nIdList´:, id IdList´\nIdList´:lambda\nType:ScalarType\nType:array ( STL ) of Type\nScalarType:id ST´\nScalarType:Sign intlist ... Bound\nST´:... Bound\nST´:lambda\nBound:Sign intlist\nBound:id\nSign:+\nSign:-\nSign:lambda\nSTL:ScalarType . STL´\nSTL´:, ScalarType STL´\nSTL´:lambda', True, ('id ; id $', 'DL=>Dec DL´=>IdList ; Type DL´=>id IdList´ ; Type DL´=>id ; Type DL´=>id ; ScalarType DL´=>id ; id ST´ DL´=>id ; id DL´=>id ; id')]
]

for ix, grammar in enumerate(grammars):
    print('***** Resultados test gramática {} *****'.format(ix+1))
    print(grammar[0])
    print('-' * 3, ' Fin gramática ', '-' * 3)

    try:
        g = grupo.Gramatica(grammar[0])

        isLL1 = g.isLL1()

        resultStr = ''
        if isLL1 != grammar[1]:
            resultStr = 'incorrecto'
        else:
            resultStr = 'correcto'

        print('El resultado del método isLL1 es {} !'.format(resultStr))
        print('Resultado entregado: ', isLL1)
        print('Resultado esperado: ', grammar[1])

        if(grammar[2]):
            parseResult = g.parse(grammar[2][0])
            if parseResult != grammar[2][1]:
                resultStr = 'incorrecto'
            else:
                resultStr = 'correcto'

            print('El resultado del método Parse es {} !'.format(resultStr))
            print('Resultado entregado: ', parseResult)
            print('Resultado esperado: ', grammar[2][1])

    except Exception as e:
        print('''Se produjo una excepción al intentar leer el string
                 con la gramática !''')
        print(e)
    print('')