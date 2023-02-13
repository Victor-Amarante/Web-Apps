import pandas as pd
import numpy as np
from datetime import date, time, datetime, timedelta

# -- BASE PRAZOS DIARIOS AGENDADOS
def tratamento_prazos_diarios_agendados(base_agendados, base_centro_custo):
    '''
    Essa função vai auxiliar no tratamento automático da base de dados referentes aos prazos agendados.
    '''
    hoje = date.today()
    df = pd.read_excel(base_agendados, engine='openpyxl')
    # dropando colunas que nao serao usadas
    df = df.drop(['NPC', 'Número do Órgão', 'Sistema Acompanhamento', 'Responsável Cancelamento',
                    'ID Obrigação', 'Observação ', 'Observação da conclusão', 'Projeto',
                    'Link de Acesso à Audiência'], axis=1)
    # criando duas novas colunas vazias
    df[' '] = ' '
    df[' '] = ' '
    # selecionar o tipo de atividade = diligencia e nao selecionar os protocolos e apagar todas as linhas
    df_remove = df[(df['Tipo de Atividade'] == 'Diligência') &
                        (df['Sub Tipo Compromisso'].str.contains('Protocolo') == False)]
    df = df.drop(df_remove.index)
    centro_custo = pd.read_excel(base_centro_custo, engine='openpyxl')
    df_ajustado = pd.merge(df, centro_custo, on='Célula', how='left')
    df_ajustado.drop(['Centro de Custo_x', 'Gestor', 'Diretoria', 'Escritorio'], axis=1, inplace=True)

    df_ajustado = df_ajustado[['ID Processo', 'ID Prazo', 'Data Cadastro Prazo', 'Data do Prazo','Hora do Prazo', 'Tipo de Atividade', 'Sub Tipo Compromisso','Parte Cliente', 'Parte Adversa', 'Número do Processo', 'Órgão',
                                    'Comarca', 'UF', 'Tipo de Processo', 'Sistema Eletrônico','Status do Prazo', 'Data Inicio Compromisso', 'Data Conclusão','Data Protocolo', 'Data Auditoria Protocolo', 'Prazo para Protocolo',
                                    'Data Prazo Automático', 'Data Revisão', 'Prazo Revisão','Data de Reprovação', 'Data Cancelamento','Motivo do cancelamento do Agendamento', 'Observação de Cancelamento',
                                    'Fase', 'Estratégia', 'Objeto', 'Sub-Objeto', 'Produto','Adv. Responsável Processo', 'Responsável Cadastro','Responsavel Prazo', 'Responsável Revisão', 'Responsável Conclusão',
                                    'Responsável Protocolo', 'Responsável Auditoria Protocolo', 'Célula','Centro de Custo_y','Cliente', 'Segmento', 'Forma Abertura', 'ID PA', 'ID Prazo Origem',
                                    ' ', ' ', 'Tem serviço contratado?', 'Id serviço', 'Tipo','Subtipo do serviço', 'Data da contratação', 'Hora da contratação','Status do serviço', 'Status Sugestão alteração/cancelamento',
                                    'Vinculado ao Recurso?', 'ID Recurso']]
    
    df_ajustado.rename(columns = {'Centro de Custo_y': 'Centro de Custo'}, inplace=True)

    df_final = df_ajustado[(df_ajustado['Centro de Custo'] != 'AMBEV') &
                                (df_ajustado['Centro de Custo'] != 'CCB MASSIFICADO') &
                                (df_ajustado['Centro de Custo'] != 'Apresentação QCA') &
                                (df_ajustado['Centro de Custo'] != 'EQUIPE PARAÍBA') &
                                (df_ajustado['Centro de Custo'] != 'MONGERAL') &
                                (df_ajustado['Centro de Custo'] != 'MARITIMO E PORTUARIO') &
                                (df_ajustado['Centro de Custo'] != ' ')]

    # colunas_datas = list(df_final.select_dtypes('datetime').columns)
    # colunas_datas.append('Data de Reprovação')
    # for i in colunas_datas:
    #     df_final[i] = pd.to_datetime(df[i], format='%Y-%m-%d')
    #     df_final[i] = df[i].dt.strftime('%d/%m/%Y')

    # df_final.to_excel(f'BASE_TRATADA_AGENDADOS_{hoje}.xlsx', index=False, engine='openpyxl')
    return df_final

# -- BASE PRAZOS DIARIOS PENDENTES
def tratamento_prazos_diarios_pendentes(base_pendentes, base_centro_custo):
    '''
    Essa função vai auxiliar no tratamento automático da base de dados referentes aos prazos pendentes.
    '''
    hoje = date.today()
    df2 = pd.read_excel(base_pendentes, engine='openpyxl')

    df2 = df2.drop(['NPC', 'Número do Órgão', 'Sistema Acompanhamento', 'Responsável Cancelamento',
                            'ID Obrigação', 'Observação ', 'Observação da conclusão', 'Projeto', 'Link de Acesso à Audiência'], axis=1)   # dropando as colunas desnecessarias
    # criacao de novas colunas vazias para colocar entre as colunas id prazo origem e tem servico contratado
    df2[' '] = ' '
    df2[' '] = ' '
    # selecionar o tipo de atividade = diligencia e nao selecionar os protocolos e apagar todas as linhas
    df2_remove = df2[(df2['Tipo de Atividade'] == 'Diligência') &
        (df2['Sub Tipo Compromisso'].str.contains('Protocolo') == False)]

    df2 = df2.drop(df2_remove.index)
    centro_custo = pd.read_excel(base_centro_custo, engine='openpyxl')
    df2_ajustado = pd.merge(df2, centro_custo, on='Célula', how='left')
    df2_ajustado.drop(['Centro de Custo_x', 'Gestor', 'Diretoria', 'Escritorio'], axis=1, inplace=True)

    df2_ajustado = df2_ajustado[['ID Processo', 'ID Prazo', 'Data Cadastro Prazo', 'Data do Prazo','Hora do Prazo', 'Tipo de Atividade', 'Sub Tipo Compromisso','Parte Cliente', 'Parte Adversa', 'Número do Processo', 'Órgão',
        'Comarca', 'UF', 'Tipo de Processo', 'Sistema Eletrônico','Status do Prazo', 'Data Inicio Compromisso', 'Data Conclusão','Data Protocolo', 'Data Auditoria Protocolo', 'Prazo para Protocolo',
        'Data Prazo Automático', 'Data Revisão', 'Prazo Revisão','Data de Reprovação', 'Data Cancelamento','Motivo do cancelamento do Agendamento', 'Observação de Cancelamento',
        'Fase', 'Estratégia', 'Objeto', 'Sub-Objeto', 'Produto','Adv. Responsável Processo', 'Responsável Cadastro','Responsavel Prazo', 'Responsável Revisão', 'Responsável Conclusão',
        'Responsável Protocolo', 'Responsável Auditoria Protocolo', 'Célula','Centro de Custo_y','Cliente', 'Segmento', 'Forma Abertura', 'ID PA', 'ID Prazo Origem',
        ' ', ' ', 'Tem serviço contratado?', 'Id serviço', 'Tipo','Subtipo do serviço', 'Data da contratação', 'Hora da contratação','Status do serviço', 'Status Sugestão alteração/cancelamento',
        'Vinculado ao Recurso?', 'ID Recurso']]

    df2_ajustado.rename(columns = {'Centro de Custo_y': 'Centro de Custo'}, inplace=True)

    # Acrescentar "Administração Judicial" que não estará mais presente no escritório
    df2_final = df2_ajustado[(df2_ajustado['Centro de Custo'] != 'AMBEV') &
                (df2_ajustado['Centro de Custo'] != 'CCB MASSIFICADO') &
                (df2_ajustado['Centro de Custo'] != 'Apresentação QCA') &
                (df2_ajustado['Centro de Custo'] != 'EQUIPE PARAÍBA') &
                (df2_ajustado['Centro de Custo'] != 'MONGERAL') &
                (df2_ajustado['Centro de Custo'] != 'MARITIMO E PORTUARIO') &
                (df2_ajustado['Centro de Custo'] != ' ')]

    # Filtragens das datas
    filtro1 = (((df2_final['Status do Prazo'] == 'Pendente') | (df2_final['Status do Prazo'] == 'Nao Protocolada')) & (df2_final['Data Prazo Automático'].isnull()))
    df2_final.loc[filtro1, "Data Prazo Automático"] = df2_final["Data do Prazo"]

    filtro2 = df2_final['Status do Prazo'] == 'Pendente'
    df2_final.loc[filtro2, "Data Prazo Automático"] = df2_final["Data do Prazo"]

    filtro3 = df2_final['Status do Prazo'] == 'Aguardando Auditoria'
    df2_final.loc[filtro3, "Data Prazo Automático"] = df2_final['Prazo para Protocolo'] + timedelta(days = 2)

    filtro4 = ((df2_final['Status do Prazo'] == 'Aguardando Revisão') & (df2_final['Prazo Revisão'] < pd.to_datetime(hoje)))
    df2_final.loc[filtro4, "Data Prazo Automático"] = df2_final['Prazo para Protocolo']

    filtro5 = ((df2_final['Status do Prazo'] == 'Aguardando Revisão') & (df2_final['Prazo Revisão'] >= pd.to_datetime(hoje)))
    df2_final.loc[filtro5, "Data Prazo Automático"] = df2_final['Prazo Revisão']

    # Fazer a filtragem das datas anteriores a 2020 e remover as linhas
    df_remove_data_under_2020 = df2_final['Data Prazo Automático'] < pd.to_datetime(datetime.date(2021,1,1))

    df2_final = df2_final.drop(df_remove_data_under_2020.index)

    # df2_final.to_excel(f'BASE_TRATADA_PENDENTES_{hoje}.xlsx', index=False, engine='openpyxl')
    return df2_final


