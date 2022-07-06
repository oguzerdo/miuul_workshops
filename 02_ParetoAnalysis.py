'''

Dünya nüfusunun 20%si toplam zenginliğin 80%'ini oluşturuyor.
Satılan ürünlerin 20%si toplam kârlılığın 80%'ini oluşturuyor.

Sizin bir şirketiniz yok mu?

Muhtelemen siz de
Kıyafetlerinizin 20 %’sini giyiyor,
Arkadaşlarınızın sadece %20'si ile buluşuyorsunuz.

Ama özetle
sonuçların %80'i, nedenlerin %20'sinden kaynaklanıyor.

sayılara takılmayalım;

etkinin büyük bir kısmını, özel bir azınlık oluşturur.


'''

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width', 500)

# 2010-2011 yılı içerisindeki veriler
df_ = pd.read_excel("datasets/online_retail_II.xlsx",  sheet_name="Year 2010-2011")

df = df_.copy()
df.head()
df.dropna(inplace=True)
df.shape


df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[df["Price"] > 0]
df = df[df["Quantity"] > 0]
df["TotalPrice"] = df["Quantity"] * df["Price"]
df.describe().T


dataframe = df.copy()
# Müşteri özelinde toplam harcamaları bulalım.
dataframe = dataframe.groupby("Customer ID").agg({'TotalPrice': "sum"})

# TotalPrice'a göre azalan bir şekilde sıralayalım.
dataframe = dataframe.sort_values('TotalPrice', ascending=False)
dataframe.head()
# index sorununu düzeltelim.
dataframe.reset_index(inplace=True)

# Kümülatif toplamları alalım.
dataframe['CumSum'] = dataframe['TotalPrice'].cumsum()

dataframe[0:15]

# Eşik değeri belirleme, toplam gelirin % kaçını merak ediyoruz?
threshold = dataframe['TotalPrice'].sum() * 0.8
threshold
target_df = dataframe[dataframe['CumSum'] <= threshold]

# %80'e hitap eden kişiler ne kadar
target_df.shape

# %80'e hitap eden kişiler % ne kadarlık bir kesim
round(target_df.shape[0] / dataframe.shape[0],2)


def pareto_analysis(dataframe, id_, price_col, percentile=0.8):
    dataframe = dataframe.groupby(id_).agg({price_col: "sum"})
    dataframe = dataframe.sort_values(price_col, ascending=False)
    dataframe.reset_index(inplace=True)
    dataframe['CumSum'] = dataframe[price_col].cumsum()
    threshold = dataframe[price_col].sum() * percentile
    target_df = dataframe[dataframe['CumSum'] <= threshold]
    print("Toplam Kazanç:", dataframe[price_col].sum())
    print(f"Toplam kazancın %{100 * percentile} kısmı", target_df.shape[0], "kullanıcıdan gelmekte.")
    print(f"Toplam kazancın %{100 * percentile} 'ini getiren kullanıcılar, tüm kitlenin % {round((target_df.shape[0] * 100 / dataframe.shape[0]),2)} kesimini oluşturmakta.")


pareto_analysis(df, "Customer ID", 'TotalPrice', percentile=0.75)
