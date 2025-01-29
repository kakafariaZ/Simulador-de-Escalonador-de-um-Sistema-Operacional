# Relatório de Teste e Avaliação do Sistema de Escalonamento de Processos

## Introdução
Este projeto tem como objetivo analisar o desempenho de um sistema de escalonamento de processos com base em diferentes valores de quantum. O sistema foi avaliado utilizando pelo menos 10 valores distintos de quantum, variando de 3 a 12. A análise buscou identificar a relação entre o valor de quantum e o comportamento do sistema em termos de trocas de processo e número de instruções executadas.

---

## Metodologia
- **Conjunto de processos**: Cada processo possui um número específico de comandos, incluindo operações simples, entradas/saídas e comandos de finalização.
- **Valores de quantum analisados**: De 3 a 12.
- **Dados coletados**: 
  - Número de trocas de processo (por término de quantum, finalização de processo ou operação de entrada/saída).
  - Número de instruções executadas até a troca de processo.
- **Logs gerados**: Arquivos de log contendo métricas sobre o comportamento do sistema para cada valor de quantum.

---

## Resultados
A tabela abaixo apresenta a média de trocas de processo e de instruções executadas para cada valor de quantum:

| **Quantum** | **Média de Trocas** | **Média de Instruções** |
|-------------|---------------------|-------------------------|
| 3           | 6.67               | 2.27                   |
| 4           | 5.44               | 2.78                   |
| 5           | 5.00               | 3.02                   |
| 6           | 4.78               | 3.16                   |
| 7           | 4.33               | 3.49                   |
| 8           | 4.33               | 3.49                   |
| 9           | 4.22               | 3.58                   |
| 10          | 4.11               | 3.68                   |
| 11          | 3.89               | 3.89                   |
| 12          | 3.89               | 3.89                   |

---

## Análise dos Resultados
### 1. **Número Médio de Trocas de Processo**
Com o aumento do valor de quantum, o número médio de trocas de processo diminui. Este comportamento é esperado, já que valores maiores de quantum permitem que os processos tenham mais tempo de execução antes de serem interrompidos.  

- **Exemplo**: Para quantum 3, a média de trocas é de 6.67, enquanto para quantum 11 e 12, estabiliza-se em 3.89.

De acordo com *Tanenbaum*, cada troca de processo envolve uma sobrecarga. Assim, valores maiores de quantum reduzem a frequência dessas trocas, melhorando a eficiência do sistema.

### 2. **Número Médio de Instruções Executadas por Quantum**
À medida que o quantum aumenta, a quantidade de instruções executadas antes da interrupção também cresce.  
- **Exemplo**: A média de instruções sobe de 2.27 (quantum 3) para 3.89 (quantum 11 e 12).

### 3. **Estabilização das Métricas**
A partir de quantum 11, tanto as trocas de processo quanto as instruções executadas se estabilizam. Isso sugere um ponto de saturação no sistema, onde valores maiores de quantum não trazem benefícios adicionais.

---

## Conclusões
### Valor Ideal de Quantum
- A análise indica que **quantuns entre 9 e 10** apresentam o melhor equilíbrio entre o número de trocas de processo e as instruções executadas.
- Quantuns muito baixos (como 3 e 4) resultam em muitas trocas, gerando overhead e reduzindo a eficiência.
- Quantuns muito altos (como 11 e 12) mostram estabilização nas métricas, indicando que o sistema não se beneficia significativamente de valores maiores.

Segundo *Tanenbaum* em *Sistemas Operacionais Modernos*, quantuns maiores permitem maior execução contínua dos processos, o que melhora o desempenho geral do sistema, especialmente para processos que requerem mais tempo de CPU.

---

## Como Executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
