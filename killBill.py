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
    ap = soup.find_all('participacao-em-trabalhos-conclusão')
# VERIFICANDO se ha participacao
    if len(ap) == 0:
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
        ls_nome_cita = []
        ls_nro =[]

        for i in range(len(ap)):
            #PARTICIPANTE-BANCA
            app = ap[i].find_all('participante-banca')
            if len(app) == 0:
                print('participante em banca nao encontrado',zipname)
            else: #DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                for j in range(len(app)):
                    ptb = app[j].find_all('dados-basicos-da-participacao-em-bancas-de-graduacao')
                    #definindo ano inicial???
                    for k in range(len(ptb)):
                        banca = str(ptb[k])
                        result = re.search('ano=\"(.*)\"pais',banca)
                        cc = fun_result(result)
                        ls_year_banca.append(cc)

                        

                        #participantes da banca
                        ep = ptb[k].find_all('participante-banca')
                        for m in range(len(ep)):
                            ip = ep[m].find_all('participante-banca')
                            ls_part_banca = []
                            ls_nome_cita = []
                            for m in range(len(ip)):
                                partic = str(ip[m])
                                result = re.search('nome-completo-partcipante-da-banca=\"(.*)\" nome-para-citacao-do-participante-da-banca',partic)
                                cc = fun_result(result)
                                ls_part_banca.append(cc)
                                ls_nome_cita.append(cc)

        #dataFrame para dados
        df_ptb = pd.DataFrame({
            'N'
        })


'''NATUREZA="Graduação" TITULO="Estudo comparativo de carbonatação utilizando pó de vidro e areia como agregado miúdo" ANO="2018" PAIS="Brasil" IDIOMA="Esperanto" HOME-PAGE="" DOI="" TITULO-INGLES=""/>

<PARTICIPANTE-BANCA NOME-COMPLETO-DO-PARTICIPANTE-DA-BANCA="Ennes do Rio Abreu" NOME-PARA-CITACAO-DO-PARTICIPANTE-DA-BANCA="ABREU, E. R." ORDEM-PARTICIPANTE="3" NRO-ID-CNPQ=""/>

<PALAVRAS-CHAVE PALAVRA-CHAVE-1="pó de vidro" PALAVRA-CHAVE-2="carbonatação" PALAVRA-CHAVE-3="gás carbônico" PALAVRA-CHAVE-4="" PALAVRA-CHAVE-5="" PALAVRA-CHAVE-6=""/>'''