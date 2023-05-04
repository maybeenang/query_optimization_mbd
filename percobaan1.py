import matplotlib.pyplot as plt
import pandas as pd
import time

from sqlalchemy import create_engine
from collections import defaultdict

time_data = defaultdict(list)

engine = create_engine('mysql://root:@localhost:3306/tubes_mbd', echo=False)
engine_index = create_engine(
    'mysql://root:@localhost:3306/tubes_mbd_indexing', echo=False)

query = "SELECT * FROM mahasiswa WHERE nama_mhs = 'Vera'"

# percobaan tanpa index
time_now = time.time()

data = pd.read_sql_query(query, engine)

time_after = time.time()

time_data['time'].append(time_after - time_now)

# percobaan dengan index
time_now = time.time()

data = pd.read_sql_query(query, engine_index)

time_after = time.time()

time_data['time'].append(time_after - time_now)

df = pd.DataFrame(time_data)

# memasukan hasil percobaan ke csv
df.to_csv('percobaan1.csv', mode='a', header=False, index=False)

# menampilkan hasil percobaan
data = pd.read_csv('percobaan1.csv', names=['time'])

# bar
plt.bar(data.index, data['time'])
# create name on x axis
plt.xticks(data.index, ['Tanpa Index', 'Dengan Index'])
plt.ylabel('Time (ms)')
plt.title('Indexing')
plt.show()
