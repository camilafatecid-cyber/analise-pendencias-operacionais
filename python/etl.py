import pandas as pd

# Caminho do arquivo
caminho = '../data/raw/pendencias.csv'

# Ler dados
df = pd.read_csv(caminho)

# Converter datas
df['data_criacao'] = pd.to_datetime(df['data_criacao'])
df['data_prazo'] = pd.to_datetime(df['data_prazo'])
df['data_conclusao'] = pd.to_datetime(df['data_conclusao'])

# Criar flag de atraso
df['atraso'] = (df['data_conclusao'] > df['data_prazo']) | (df['status'] == 'Atrasado')

# Criar tempo de resolução
df['tempo_resolucao'] = (df['data_conclusao'] - df['data_criacao']).dt.days

# Tratar valores nulos
df['tempo_resolucao'] = df['tempo_resolucao'].fillna(-1)
df['atraso'] = df['atraso'].fillna(True)

# Salvar base tratada
df.to_csv('../data/processed/pendencias_tratadas.csv', index=False)

# Mostrar resultado
print(df)

import sqlite3

# Criar conexão com banco
conn = sqlite3.connect('../data/processed/operacoes.db')

# Salvar tabela única (base inicial)
df.to_sql('pendencias', conn, if_exists='replace', index=False)

conn.close()

import sqlite3

conn = sqlite3.connect('../data/processed/operacoes.db')

# -------------------------
# DIMENSÃO COLABORADOR
# -------------------------
dim_colaborador = df[['colaborador']].drop_duplicates().reset_index(drop=True)
dim_colaborador['colaborador_id'] = dim_colaborador.index + 1

# -------------------------
# DIMENSÃO DEPARTAMENTO
# -------------------------
dim_departamento = df[['departamento']].drop_duplicates().reset_index(drop=True)
dim_departamento['departamento_id'] = dim_departamento.index + 1

# -------------------------
# FATO
# -------------------------
fato = df.merge(dim_colaborador, on='colaborador')
fato = fato.merge(dim_departamento, on='departamento')

fato_final = fato[[
    'id',
    'colaborador_id',
    'departamento_id',
    'status',
    'tempo_resolucao',
    'atraso'
]]

# -------------------------
# SALVAR NO BANCO
# -------------------------
dim_colaborador.to_sql('dim_colaborador', conn, if_exists='replace', index=False)
dim_departamento.to_sql('dim_departamento', conn, if_exists='replace', index=False)
fato_final.to_sql('fato_pendencias', conn, if_exists='replace', index=False)

conn.close()