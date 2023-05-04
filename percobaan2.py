import matplotlib.pyplot as plt
import pandas as pd
import time

from sqlalchemy import create_engine
from collections import defaultdict

time_data = defaultdict(list)

engine = create_engine('mysql://root:@localhost:3306/tubes_mbd', echo=False)

query1 = '''
SELECT mahasiswa.nim, mahasiswa.nama_mhs, prodi.nama_prodi, mata_kuliah.nama_matkul FROM mahasiswa ,perkuliahan, mata_kuliah, prodi
WHERE 
perkuliahan.nim = mahasiswa.nim AND
perkuliahan.id_matkul = mata_kuliah.id AND
mahasiswa.id_prodi = prodi.id
'''

query2 = '''
SELECT mahasiswa.nim, mahasiswa.nama_mhs, prodi.nama_prodi, mata_kuliah.nama_matkul FROM mahasiswa INNER JOIN perkuliahan ON perkuliahan.nim = mahasiswa.nim
INNER JOIN mata_kuliah ON perkuliahan.id_matkul = mata_kuliah.id
INNER JOIN prodi ON mahasiswa.id_prodi = prodi.id
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
df.to_csv('percobaan2.csv', mode='a', header=False, index=False)

# menampilkan hasil percobaan
data = pd.read_csv('percobaan2.csv', names=['time'])

# bar
plt.bar(data.index, data['time'])
# create name on x axis
plt.xticks(data.index, ['Query 1', 'Query 2'])
plt.ylabel('Time (ms)')
plt.title('JOIN Optimization')
plt.show()
