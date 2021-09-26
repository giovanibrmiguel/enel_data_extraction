import json 
import pandas as pd
import re

def read_json(file_name):
    data = json.load(open(file_name))
    texto = data[0]['description'].replace('\n', ' ')
    return texto

def extract_data(texto):
    #Assumindo que a primeira palavra após N DA INSTALAÇÃO vai ser o número da instalação
    n_instalacao = re.search('N° DA INSTALAÇÃO (\w+)', texto).group(1) 

    #Assumindo que a palavra entre CPF?CNPJ e INC. EST vai ser o CPF/CNPJ
    CPF_CNPJ = re.search('CPF/CNPJ: (.*) INSC. EST', texto).group(1) 

    #Assumindo que a frase entre 'leitura anterior' e 'leitura atual' excluindo as duas primeiras palavras (mes e dia) são o local
    local = re.search('Leitura anterior (.*) Leitura atual', texto).group(1)
    local = local.split(' ', 2)[2]

    #Assumindo que a primeira palavra após GRUPO vai ser o grupo
    grupo = re.search('Grupo (\w+)', texto).group(1)

    #Assumindo que a primeira palavra após GRUPO vai ser o grupo
    subgrupo = re.search('Subgrupo (\w+)', texto).group(1)

    #Assumindo que a primeira palavra após Modalidade Tarifária vai ser a modalidade tarifária
    modalidade_tarifaria = re.search('Modalidade Tarifária (\w+)', texto).group(1)

    #Assumindo que a energia_contratada vai ser um número aparecendo logo após o texto Energia Contratada
    energia_contratada = re.search('Demanda / Energia Contratada ([\d,\.]+)', texto).group(1)

    #Assumindo que o sétimo string após 'Série Base de cálculo Alíquota ICMS' vai ser a série
    serie = re.search('Série Base de cálculo Alíquota ICMS (.*)', texto).group(1)
    serie = serie.split(' ', 8)[8]
    serie = serie.split()[0]

    #Assumindo que após a palavra Hora Ponta virá a tabela que terá 13 linhas
    tabela = re.search('Hora Ponta (.*)', texto).group(1)
    tabela = tabela.split()
    table_months = tabela[:13]
    table_demanda = tabela[13:26]
    table_consumo_hora_ponta = tabela[26:39]
    table_consumo_hora_fora_ponta = tabela[39:52]
    table_dicio = {'month':table_months,
            'demanda':table_demanda,
            'consumo_hora_ponta':table_consumo_hora_ponta,
            'consumo_hora_fora_ponta':table_consumo_hora_fora_ponta
            }

    #Assumindo que o PIS/PASEP vai estar entre parenteses após a frase PIS/PASEP
    PIS_PASEP = re.search('PIS/PASEP \((.*?)\)', texto).group(1)
    PIS_PASEP

    #Assumindo que o COFINS vai estar entre parenteses após a frase COFINS
    COFINS = re.search('COFINS \((.*?)\)', texto).group(1)
    COFINS

    keys = ['n_instalacao',
            'CPF_CNPJ',
            'local',
            'grupo',
            'subgrupo',
            'modalidade_tarifaria',
            'energia_contratada',
            'serie',
            'tabela',
            'PIS_PASEP',
            'COFINS'
            ]

    values = [n_instalacao,
            CPF_CNPJ,
            local,
            grupo,
            subgrupo,
            modalidade_tarifaria,
            energia_contratada,
            serie,
            table_dicio,
            PIS_PASEP,
            COFINS
            ]
    dictionary = dict(zip(keys, values))
    return dictionary

def create_json(dictionary, output_name):
    out_file = open(output_name, "w")
    json.dump(dictionary, out_file, indent = 4)

if __name__ == "__main__":
    input_name = input('Please, type the JSON file name to be extracted: ')+'.json'
    texto = read_json(input_name)
    dictionary = extract_data(texto)
    output_name = input("Please, type the desired name for the JSON output file: ")+'.json'
    create_json(dictionary, output_name)
    print('DONE!')
    
