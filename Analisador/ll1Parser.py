import csv

class LL1Parser:
    def __init__(self, tableFile):
        self.parseTable = self.loadParseTable(tableFile)
    
    def loadParseTable(self, filePath):
        table = {}
        with open(filePath, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Ler e ignorar a linha de cabeçalho, se presente
            for row in reader:
                if len(row) < 3:
                    continue  # Pular linhas que não têm colunas suficientes
                nonTerminal, terminal, production = row
                if nonTerminal not in table:
                    table[nonTerminal] = {}
                table[nonTerminal][terminal] = production
        return table
    
    def parse(self, inputString):
        stack = ['$', 'S']  # Supondo que 'S' é o símbolo inicial e '$' é o marcador de fim de entrada
        inputString = inputString + '$'
        index = 0

        print(f"Pilha inicial: {stack}")
        print(f"Entrada inicial: {inputString}")

        while stack:
            top = stack.pop()
            if index >= len(inputString):
                return "Erro: Entrada não reconhecida"

            currentChar = inputString[index]
            
            print(f"Topo da pilha: {top}")
            print(f"Caractere atual: {currentChar}")

            if top == currentChar:
                print(f"Correspondência encontrada. Consumindo '{currentChar}'")
                index += 1
            elif top in self.parseTable:
                if currentChar in self.parseTable[top]:
                    production = self.parseTable[top][currentChar]
                    print(f"Aplicando produção: {top} -> {production}")
                    if production != 'ε':  # 'ε' representa epsilon (string vazia)
                        stack.extend(reversed(production))
                else:
                    return "Erro: Entrada não reconhecida"
            elif top == '$' and currentChar == '$':
                # Ambos a pilha e a entrada terminam com '$'
                print("Fim da entrada alcançado com sucesso")
                return "Sucesso: Entrada aceita"
            else:
                return "Erro: Entrada não reconhecida"

            print(f"Pilha atualizada: {stack}")
            print(f"Entrada restante: {inputString[index:]}")

        if index == len(inputString) and not stack:
            return "Sucesso: Entrada aceita"
        else:
            return "Erro: Entrada não aceita"

def mainFunction():
    tableFile = 'parseTable.csv'
    parser = LL1Parser(tableFile)

    inputFile = 'input.txt'
    with open(inputFile, 'r') as file:
        inputString = file.read().strip()

    result = parser.parse(inputString)
    print(result)

mainFunction()
