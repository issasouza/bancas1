import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
import zipfile
from extrafuns import fun_result


#partipação em bancas de trabalhos conclusão

def getBancas (zipname):
    zipfilepath = './xml_zip' + '/' + str (zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup= BeautifulSoup(lattesxmldata, 'lxml',
                        from_encoding='ISO-8859-1')


# extrair PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO
    part_traba_c = soup.find_all('participacao-em-trabalhos-conclusão')
# VERIFICANDO se ha participacao
    if len(part_traba_c) == 0:
        print('participacao em bancas de trabalhos de conclusão não encontrada para:', zipname)
    else:
        ls_dados_part = []
        ls_natu_banca = []
        ls_tipo_banca = []
        ls_title_banca = []
        ls_year_banca = []
        ls_pais_banca = []
        ls_idioma_banca = []
        ls_part_banca = []
        ls_ordem =[]
        ls_nome_banca= []
        

        for i in range(len(part_traba_c)):
            #PARTICIPACAO-EM-BANCA-DE-MESTRADO
            part_bancas = part_traba_c[i].find_all('participacao-em-banca-de-mestrado')
            if len(part_bancas) == 0:
                print('participante em banca de mestrado nao encontrado',zipname)
            else: #DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                for j in range(len(part_bancas)):
                    ptb = part_bancas[j].find_all('dados-basicos-da-participacao-em-bancas-de-graduacao-de-mestrado')
                    #definindo ano inicial???
                    for k in range(len(ptb)):
                        dadosbanca = str(ptb[k])
                        result = re.search('natureza=\"(.*)\"tipo',dadosbanca)
                        cc = fun_result(result)
                        ls_natu_banca.append(cc)
                        #print (ls_natu_banca)

                        result = re.search('titulo=\"(.*)\"ano',dadosbanca)
                        cc = fun_result(result)
                        ls_title_banca.append(cc)

                        result = re.search('pais=\"(.*)\"idioma',dadosbanca)
                        cc = fun_result(result)
                        ls_pais_banca.append(cc)
                        
                        

                        #detalhe participantes da banca
                        #DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO
                        detalhe_banca = part_bancas[i].find_all(
                            'detalhamento-da-participacao-em-banca-de-mestrado')
                        detalhe_banca = str(detalhe_banca)

#<DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO 
# NOME-DO-CANDIDATO="Marielle Albuquerque Azoubel" 
#CODIGO-INSTITUICAO="002100000009" NOME-INSTITUICAO="Universidade Federal de Pernambuco"
# CODIGO-ORGAO="" NOME-ORGAO="" CODIGO-CURSO="60054131" 
# NOME-CURSO="Educação Matemática e Tecnológica" NOME-CURSO-INGLES=""/>

                        #nome-do-candidato
                        result = re.search('nome-do-candidato=\"(.*)\"nome-instituicao',
                        detalhe_banca)
                        cc = fun_result(result)
                        ls_nome_banca(cc)

                        result = re.search('')





        #dataFrame para dados
        df_ptb = pd.DataFrame({
            'N'
        })


'''NATUREZA="Graduação" TITULO="Estudo comparativo de carbonatação utilizando pó de vidro e areia como agregado miúdo" ANO="2018" PAIS="Brasil" IDIOMA="Esperanto" HOME-PAGE="" DOI="" TITULO-INGLES=""/>

<PARTICIPANTE-BANCA NOME-COMPLETO-DO-PARTICIPANTE-DA-BANCA="Ennes do Rio Abreu" NOME-PARA-CITACAO-DO-PARTICIPANTE-DA-BANCA="ABREU, E. R." ORDEM-PARTICIPANTE="3" NRO-ID-CNPQ=""/>

<PALAVRAS-CHAVE PALAVRA-CHAVE-1="pó de vidro" PALAVRA-CHAVE-2="carbonatação" PALAVRA-CHAVE-3="gás carbônico" PALAVRA-CHAVE-4="" PALAVRA-CHAVE-5="" PALAVRA-CHAVE-6=""/>'''
