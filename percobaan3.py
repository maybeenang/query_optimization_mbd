import matplotlib.pyplot as plt
import pandas as pd
import time

from sqlalchemy import create_engine
from collections import defaultdict

time_data = defaultdict(list)

engine = create_engine('mysql://root:@localhost:3306/tubes_mbd', echo=False)

query1 = '''
SELECT * FROM mahasiswa INNER JOIN prodi ON prodi.id = mahasiswa.id_prodi
'''

query2 = '''
SELECT nim, nama_mhs, nama_prodi FROM mahasiswa INNER JOIN prodi ON prodi.id = mahasiswa.id_prodi
'''

# percobaan tanpa index
time_now = time.time()

data = pd.read_sql_query(query1, engine)

time_after = time.time()

time_data['time'].append(time_after - time_now)

# percobaan dengan index
time_now = time.time()

data = pd.read_sql_query(query2, engine)

time_after = time.time()

time_data['time'].append(time_after - time_now)

df = pd.DataFrame(time_data)

# memasukan hasil percobaan ke csv
df.to_csv('percobaan3.csv', mode='a', header=False, index=False)

# menampilkan hasil percobaan
data = pd.read_csv('percobaan3.csv', names=['time'])

# bar
plt.bar(data.index, data['time'])
# create name on x axis
plt.xticks(data.index, ['Query 1', 'Query 2'])
plt.ylabel('Time (ms)')
plt.title('Materialized View')
plt.show()
