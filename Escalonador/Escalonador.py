import os
import math

class Processo:
    def __init__(self, id, nome, comandos):
        self.id = id
        self.nome = nome
        self.comandos = comandos
        self.pc = 0  # Contador de programa
        self.registradores = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        self.estado = "Pronto"
        self.tempo_espera = 0

    def executar_comando(self):
        comando = self.comandos[self.pc]
        self.pc += 1
        if "=" in comando:
            reg, valor = comando.split("=")
            self.registradores[reg] = int(valor)
        elif comando == "E/S":
            self.estado = "Bloqueado"
        elif comando == "COM":
            pass  # Simulação do comando executado
        elif comando == "SAIDA":
            self.estado = "Finalizado"

    def __str__(self):
        regs = ", ".join([f"{k}={v}" for k, v in self.registradores.items()])
        return f"{self.nome}. {regs}"

class Escalonador:
    def __init__(self, quantum):
        self.quantum = quantum
        self.fila_prontos = []
        self.fila_bloqueados = []
        self.log = []
        self.trocas = 0
        self.instrucoes_totais = 0
        self.processos_finalizados = []

    def carregar_processos(self, pasta):
        arquivos = sorted(os.listdir(pasta))
        for id, arquivo in enumerate(arquivos):
            with open(os.path.join(pasta, arquivo), 'r') as f:
                linhas = f.read().splitlines()
                
                # Verificar se o arquivo excede o limite de 22 linhas
                if len(linhas) > 22:
                    self.log.append(f"Erro: O arquivo {arquivo} excede o limite de 22 linhas e será ignorado.")
                    continue
                
                nome = linhas[0]
                comandos = linhas[1:]
                
                # Verificar se há mais de 21 comandos (excluindo o nome)
                if len(comandos) > 21:
                    self.log.append(f"Erro: O programa {nome} possui mais de 21 comandos e será ignorado.")
                    continue
                
                self.fila_prontos.append(Processo(id, nome, comandos))
                self.log.append(f"Carregando {nome}")


    def executar(self):
        while self.fila_prontos or self.fila_bloqueados:
            if self.fila_prontos:
                processo = self.fila_prontos.pop(0)
                self.log.append(f"Executando {processo.nome}")
                instrucoes_executadas = 0

                while (instrucoes_executadas < self.quantum and
                       processo.pc < len(processo.comandos) and
                       processo.estado != "Bloqueado"):
                    processo.executar_comando()
                    instrucoes_executadas += 1

                self.instrucoes_totais += instrucoes_executadas
                self.trocas += 1

                if processo.estado == "Bloqueado":
                    processo.tempo_espera = math.ceil(self.quantum / 2)
                    self.fila_bloqueados.append(processo)
                    self.log.append(f"E/S iniciada em {processo.nome}")
                elif processo.estado == "Finalizado":
                    self.processos_finalizados.append(processo)
                    self.log.append(f"{processo} terminado.")
                else:
                    self.fila_prontos.append(processo)
                    self.log.append(f"Interrompendo {processo.nome} após {instrucoes_executadas} instruções")
            
            for processo in self.fila_bloqueados[:]:
                processo.tempo_espera -= 1
                if processo.tempo_espera <= 0:
                    processo.estado = "Pronto"
                    self.fila_bloqueados.remove(processo)
                    self.fila_prontos.append(processo)

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
        quantum = int(f.read().strip())

    escalonador = Escalonador(quantum)
    escalonador.carregar_processos("processos")
    escalonador.executar()
    escalonador.salvar_log()
