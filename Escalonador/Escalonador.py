import os # Usado para manipulação de arquivos e diretórios
import math # Utilizado para operações matemáticas, como arredondamento

class Processo: # Representa um processo no sistema, com atributos como ID, nome, comandos, registradores, estado, etc.
    def __init__(self, id, nome, comandos):
        self.id = id
        self.nome = nome
        self.comandos = comandos
        self.pc = 0  # Contador de programa
        self.registradores = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        self.estado = "Pronto"
        self.tempo_espera = 0

    def executar_comando(self): # Executa o próximo comando do processo.
        comando = self.comandos[self.pc]
        self.pc += 1
        if "=" in comando:
            reg, valor = comando.split("=") # Divide o comando em registrador e valor
            self.registradores[reg] = int(valor) # Atribui o valor ao registrador
        elif comando == "E/S":
            self.estado = "Bloqueado"
        elif comando == "COM":
            pass  # Simula a execução de um comando
        elif comando == "SAIDA": 
            self.estado = "Finalizado"

    def __str__(self): # Retorna uma representação legível do processo, mostrando o nome e os valores dos registradores.
        regs = ", ".join([f"{k}={v}" for k, v in self.registradores.items()])
        return f"{self.nome}. {regs}"

class Escalonador: # Responsável por gerenciar a execução dos processos usando o algoritmo Round-Robin.
    def __init__(self, quantum):
        self.quantum = quantum
        self.fila_prontos = []
        self.fila_bloqueados = []
        self.log = []
        self.trocas = 0
        self.instrucoes_totais = 0
        self.processos_finalizados = []

    def carregar_processos(self, pasta): 
        arquivos = sorted(os.listdir(pasta)) # Lista os arquivos na pasta
        for id, arquivo in enumerate(arquivos):
            with open(os.path.join(pasta, arquivo), 'r') as f:
                linhas = f.read().splitlines() # Lê todas as linhas do arquiv
                
                # Verificar se o arquivo excede o limite de 22 linhas
                if len(linhas) > 22:
                    self.log.append(f"Erro: O arquivo {arquivo} excede o limite de 22 linhas e será ignorado.")
                    continue
                
                nome = linhas[0]  # A primeira linha é o nome do processo
                comandos = linhas[1:] # As demais linhas são os comandos
                
                # Verifica se há mais de 21 comandos (fora o nome)
                if len(comandos) > 21:
                    self.log.append(f"Erro: O programa {nome} possui mais de 21 comandos e será ignorado.")
                    continue
                
                # Adiciona o processo à fila de prontos
                self.fila_prontos.append(Processo(id, nome, comandos)) #Adiciona os processos válidos à fila de prontos.
                self.log.append(f"Carregando {nome}")


    def executar(self): # Executa os processos usando o algoritmo Round-Robin.
        while self.fila_prontos or self.fila_bloqueados:
            if self.fila_prontos:
                processo = self.fila_prontos.pop(0) # Remove o primeiro processo da fila de prontos
                self.log.append(f"Executando {processo.nome}")
                instrucoes_executadas = 0

                # Executa comandos enquanto o quantum não é atingido e o processo não está bloqueado

                while (instrucoes_executadas < self.quantum and
                       processo.pc < len(processo.comandos) and 
                       processo.estado != "Bloqueado"):
                    processo.executar_comando()
                    instrucoes_executadas += 1

                self.instrucoes_totais += instrucoes_executadas # Atualiza o total de instruções executadas
                self.trocas += 1 # Incrementa o contador de trocas de contexto

                if processo.estado == "Bloqueado": # Processo bloqueado (E/S)
                    processo.tempo_espera = math.ceil(self.quantum / 2) # Define o tempo de espera
                    self.fila_bloqueados.append(processo)  # Adiciona à fila de bloqueados
                    self.log.append(f"E/S iniciada em {processo.nome}")
                elif processo.estado == "Finalizado": # Processo finalizado
                    self.processos_finalizados.append(processo) # Adiciona à lista de finalizados
                    self.log.append(f"{processo} terminado.")
                else: # Processo ainda não terminou
                    self.fila_prontos.append(processo) # Retorna à fila de prontos
                    self.log.append(f"Interrompendo {processo.nome} após {instrucoes_executadas} instruções")
            
            # Atualiza o tempo de espera dos processos bloqueados
            for processo in self.fila_bloqueados[:]:
                processo.tempo_espera -= 1
                if processo.tempo_espera <= 0: # Processo terminou a espera
                    processo.estado = "Pronto" # Muda o estado para Pronto
                    self.fila_bloqueados.remove(processo) # Remove da fila de bloqueados
                    self.fila_prontos.append(processo) # Adiciona à fila de prontos

    def salvar_log(self):
        # Cálculo das médias de trocas e instruções
        media_trocas = self.trocas / len(self.processos_finalizados) if self.processos_finalizados else 0
        media_instrucoes = self.instrucoes_totais / self.trocas if self.trocas else 0
        
        # Aguardar a geração do arquivo de log para cada quantum
        log_file = f"log{str(self.quantum).zfill(2)}.txt"
        
        with open(log_file, 'w') as f:
            # Escreve as mensagens do log
            for linha in self.log:
                f.write(linha + '\n')
            # Escreve as médias
            f.write(f"MEDIA DE TROCAS: {media_trocas:.2f}\n")
            f.write(f"MEDIA DE INSTRUCOES: {media_instrucoes:.2f}\n")
            f.write(f"QUANTUM: {self.quantum}\n")


if __name__ == "__main__":
    with open("quantum.txt", 'r') as f: 
        quantum = int(f.read().strip()) # Lê o valor do quantum do arquivo quantum.txt

    escalonador = Escalonador(quantum) # Cria o escalonador com o quantum lido
    escalonador.carregar_processos("processos")  # Carrega os processos da pasta "processos"
    escalonador.executar()  # Executa os processos
    escalonador.salvar_log() # Salva o log em um arquivo
-
