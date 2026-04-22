import sqlite3
import pandas as pd

conn = sqlite3.connect('../data/processed/operacoes.db')

query = """
SELECT 
    d.departamento,
    COUNT(*) as total_tarefas,
    AVG(f.tempo_resolucao) as tempo_medio
FROM fato_pendencias f
JOIN dim_departamento d
    ON f.departamento_id = d.departamento_id
GROUP BY d.departamento
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()