import pandas as pd
import numpy as np
from openpyxl import load_workbook


# xlsx = pd.ExcelFile('Finder.xlsx')
# print(xlsx.sheet_names)
#
# sheet1_df = xlsx.parse('Лист1')

x2 = np.random.randn(100, 2)
df2 = pd.DataFrame(x2)
writer = pd.ExcelWriter('Finder.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace')
df2.to_excel(writer, sheet_name='x2')
writer.close()
