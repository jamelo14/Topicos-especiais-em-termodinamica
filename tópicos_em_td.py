import matplotlib.pyplot as plt
import numpy as np
import random as rd
from statistics import mean

# 1 p direita
# -1 q esquerda

####################################### Condições Iniciais #######################################

N = 1000
QTD_PART = 10000
p = 0.5
q = 1 - p

############################################# Outros #############################################

labelx_barras = "Posição"
labely_barras = "Probabilidade [%]"

labelx_traj = "valor de N"
labely_traj = "posição média das partículas"

titulo = "Posição média e probabilidade"

cor_teoria = "red"
cor_experimento = "blue"
cor_traj = "purple"

legenda_teoria = "resultados teóricos"
legenda_experimental = "resultados experimentais"

legenda_posicao = "posição"

##################################################################################################

# Função fatorial
def fatorial(N):
    if N <= 1:
        return 1
    fat = 1
    for i in range(1,N + 1):
        fat *= i
        
    return fat

# Combinação de N elementos, N1 em N1
def combinacao(N1, N2):
    global N
    return fatorial(N)/( fatorial(N1) * fatorial(N2) )

# Probabilidade de N1 passos à direita e N2 passos à esquerda
def P(N1, N2):
    global p, q, N
    return ( combinacao(N1, N2) * p**N1 * q**N2 )

def proxima_posicao():
	global p, q
	
	var = rd.random()
	
	return 1 if var < p else -1

def simular_particula(resu):
	x = np.zeros(N)
	
	for i in range(N - 1):
		x[i + 1] = x[i] + proxima_posicao()
		
	if resu == "posicao final":
		return x[N-1]  
		
	elif resu == "trajetoria":
		return x
		
	elif resu == "ambos":
		return x[N-1], x
		
	print("simular_particula(): Retornando None pois o argumento posicional \"resu\" não coincide com as opções possíveis (\"posicao final\", ou \"trajetoria\", ou \"ambos\") ")
	return None

def soma_trajetorias(traj, media):
	return list(map(lambda x, y: x + y, traj, media))

# Função principal
def main():
    global N, p, q, titulo, labelx_barras, labely_barras, cor_teoria, cor_experimento, legenda_teoria, legenda_experimental, labelx_traj, labely_traj, legenda_posicao, cor_traj
		
	########## Calculando a distribuição esperada ##########
    # O deslocamento médio representa o centro da distribuição
    DM = (p - q) * N

    # O deslocamento quadrado médio indica o tamanho da gaussiana
    D2M = p**2 * N + p*q*N

    # Vetores dos eixos
    x = np.zeros(N)
    y = np.zeros(N)

    # Loop de cálculos
    for N1 in range(N+1):
        x[N1-1] = 2*N1 - N
        y[N1-1] = P(N1, N-N1) * 100
    
    plt.subplot(2, 1, 1)
    # Plota as barras
    plt.bar(x, y, color=cor_teoria)
    
    # Limita o range dos eixos
    plt.axis([DM - D2M/2, DM + D2M/2, None, None])
    
    # Título
    plt.title(titulo)
    
    # Labels
    plt.xlabel(labelx_barras)
    plt.ylabel(labely_barras)
    
    # Legendas
    legendas = [legenda_teoria, legenda_experimental]
    
    # Ticks (medidas nos eixos)
    plt.xticks([DM - D2M/2, DM,  DM + D2M/2])
    
    ########## Fazendo a simulação da partícula ##########
    posicoes_simulacao = {}
    
    # Lista que carregará a trajetória média
    trajetoria_media = [0 for _ in range(QTD_PART)]
    
    # As posições são salvas em um dicionário
    # As chaves do dicionário são as posições
    # Os valores dos dicionários são a quantidade de vezes que uma partícula caiu nessa posição.
    for i in range(QTD_PART):
    	var, trajetoria = simular_particula("ambos")
    	
    	trajetoria_media = soma_trajetorias(trajetoria, trajetoria_media)
    	
    	if var in posicoes_simulacao.keys(): 
    		posicoes_simulacao[var] += 1
    		
    	else:
    		posicoes_simulacao[var] = 0
    
   	# Transformando a quandidade das posições de X em probabilidades
    probabilidades = list(map(lambda x: x/QTD_PART*100, posicoes_simulacao.values()))
   	
    # Plota as barras
    plt.bar(posicoes_simulacao.keys(), probabilidades, color=cor_experimento)
    
    # Aplicando legendas
    plt.legend(legendas)
    
    # Plotando a trajetória média
    plt.subplot(2, 1, 2)
    
    # Calclando a média das trajetórias
    trajetoria_media = list(map(lambda x: x/QTD_PART, trajetoria_media))
    
    # Plotando a trajetória média por "altura"
    plt.plot(list(range(N)), trajetoria_media, color=cor_traj)
    
    # Limita o range dos eixos
    plt.axis([0, N, min(trajetoria_media) - abs(mean(trajetoria_media)), max(trajetoria_media) + abs(mean(trajetoria_media))])
   
    # Labels
    plt.xlabel(labelx_traj)
    plt.ylabel(labely_traj)
    
    # Legendas
    legendas = [legenda_posicao]
    
    # Aplicando a legenda
    plt.legend(legendas)
    
    # Ticks (medidas nos eixos)
    plt.xticks([0, N] + list(range(N)[::100]))
    plt.yticks([min(trajetoria_media) - abs(mean(trajetoria_media)), mean(trajetoria_media), max(trajetoria_media)+ abs(mean(trajetoria_media)), 0])
    
    # Mostra o Gráfico
    plt.show()

	

# Inicio do programa
main()
