"""
Author: Oguz Erdogan, Miuul
https://www.linkedin.com/in/oguzerdo/

https://github.com/oguzerdo/rule_based_segmentation/blob/main/01_rule_based_segmentation.py

"""

# Portekizde bulunan bir otele ait bu veri setinde 2015-2018 boyunca konukların
# bazı demografik bilgileri ve rezervasyon ile ilgili bilgileri yer almakta.
# Otel, konuklarının bazı özelliklerini kullanarak seviye tabanlı (level based )
# yeni müşteri tanımları (persona) oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup
# bu segmentlere göre yeni gelebilecek müşterilerin otele
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.


# Örneğin: Fransadan Ajans aracılığıyla rezervasyon yapmış 30 yaşındaki birisinin
# ortalama ne kadar kazandırabileceği ya da ne kadar zaman önce rezervasyon yapabileceği belirlenmek isteniyor.


################# Uygulama Öncesi #####################

#	ID	Nationality	Age	LeadTime	LodgingRevenue	OtherRevenue	Channel
# 	 4	FRA 	    60.0	93	    240.0	        60.0        	Agent
# 	 8	FRA 	    32.0	38	    535.0	        94.0        	Agent
# 	12	FRA	        58.0	60	    292.0	        81.0        	Agent
# 	14	ESP	        42.0	87	    327.7	        48.0        	Direct
# 	16	FRA	        68.0	11	    437.0	        36.0        	Agent


################# Uygulama Sonrası #####################

#   customers_level_based	Revenue	            LeadTime	    SEGMENT
#	DEU_AGENT_18_25	        560.716760	        103.129221	        A
#	DEU_AGENT_26_40	        449.799012	        78.828552	        B
#	DEU_AGENT_41_50	        492.285417	        104.734114	        B
#	DEU_AGENT_51_60	        500.283815	        127.269332	        B
#	DEU_AGENT_60+	        360.369899	        243.133928	        C


# Değişken tanımları
# Nationality: Konuğun milliyeti
# Age: Konuğun yaşı
# LeadTime: Rezervasyon yapılan gün ile checkin arasındaki gün sayısı
# LodgingRevenue: Müşteri tarafından konaklama giderleri için harcanan toplam tutar (Euro). Bu değere oda, beşik ve diğer ilgili konaklama giderleri dahildir.
# OtherRevenue: Müşteri tarafından diğer harcamalar için harcanan toplam tutar (Euro). Bu değere yiyecek, içecek, spa ve diğer harcamalar dahildir.
# Channel: Müşteri tarafından otelde rezervasyon yapmak için kullanılan kanal.
# Agent Turizm ajansi ile rezervasyon,
# Direct: Direct booking.
# Corporate: Partnerler aracılığıyla yapılan rezervasyon.
# Electronic: Elektronik kanallar aracılığıyla yapılan rezervasyon.


# https://www.sciencedirect.com/science/article/pii/S2352340920314645?via%3Dihub
import pandas as pd
from matplotlib import pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option("display.width", 500)

# data.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd

data = pd.read_csv('datasets/data.csv', sep="|")

# Bu şekilde bir işlem yapmamalıyız.
yedek = data

yedek.head()
data.head()

yedek["Age"] = yedek["Age"].apply(lambda x: x * x)

yedek.head()
data.head()

data = pd.read_csv('datasets/data.csv', sep="|")

# Bu şekilde kullanmalıyız.
df = data.copy()
df["Age"] = df["Age"].apply(lambda x: x * x)

df.head()
data.head()

### Veriyi anlama


data = pd.read_csv('datasets/data.csv', sep="|")
df = data.copy()
df.head()

#    ID Nationality   Age  LeadTime  LodgingRevenue  OtherRevenue Channel
# 0   4         FRA  60.0        93           240.0          60.0   Agent
# 1   8         FRA  32.0        38           535.0          94.0   Agent
# 2  12         FRA  58.0        60           292.0          81.0   Agent
# 3  14         ESP  42.0        87           327.7          48.0  Direct
# 4  16         FRA  68.0        11           437.0          36.0   Agent

df.shape

df.info()

# Age ve Leadtime degiskeninde - degerler var
df.describe([0.1, 0.5, 0.75, 0.9, 0.95, 0.99]).T

#                   count          mean           std   min     10%      50%      75%      90%      95%        99%      max
# ID              35725.0  34973.034206  22583.237559   4.0  7132.8  31726.0  50506.0  71004.2  77593.8  82185.280  83585.0
# Age             35725.0     48.112414     14.474405 -11.0    29.0     48.0     58.0     68.0     73.0     81.000    114.0
# LeadTime        35725.0     90.635969     97.235745  -1.0     3.0     58.0    135.0    220.0    288.0    451.000    588.0
# LodgingRevenue  35725.0    357.515912    265.671866   0.0   117.0    292.0    444.0    670.0    881.8   1413.000   2055.0
# OtherRevenue    35725.0     85.870103     96.379774   0.0    12.0     56.0    110.0    187.5    260.5    461.904   1465.0

# Age ve Leadtime degiskeninde - degerler var bunları çıkaralım
df = df.loc[~((df["Age"] <= 0) | (df["LeadTime"] < 0))]

# Veri setindeki IDnin unique olma durumunu kontrol edelim
df.shape

# Toplam gözlem sayısı ID değişkeninideki toplam unique sayısına eşit. Çoklanmış bir veri yok.
df.ID.nunique()

# Bir başka yöntem
df[df.ID.duplicated()]

# Toplam kazancı ifade eden bir değişken yok bunu oluşturalım.

df["Revenue"] = df['LodgingRevenue'] + df["OtherRevenue"]

# Revenue'de farklı bir durum var mı kontrol edelim.
df[df["Revenue"] <= 0]

# Revenue dagilimina bakalim
df["Revenue"].hist();
plt.show()

# Daha yakından incelemek istersek, genellikle harcamalar 200-400 Euro aralığında görülüyor.
df[df["Revenue"] < 750]["Revenue"].hist();
plt.show()

# Ilerleyen projelerde her bir değişkene tek tek grafik olarak bakmak bizi yoracak,
# Sayısal değişkenlerde describe ile veriyi grafiğe bakar gibi yorumlamak mümküm.
df.describe([0, 0.01, 0.1, 0.5, 0.75, 0.9, 0.95, 0.99]).T

#                   count          mean           std   min    0%      1%     10%      50%      75%       90%       95%        99%       max
# ID              35725.0  34973.034206  22583.237559   4.0   4.0  888.48  7132.8  31726.0  50506.0  71004.20  77593.80  82185.280  83585.00
# Age             35725.0     48.112414     14.474405 -11.0 -11.0   20.00    29.0     48.0     58.0     68.00     73.00     81.000    114.00
# LeadTime        35725.0     90.635969     97.235745  -1.0  -1.0    0.00     3.0     58.0    135.0    220.00    288.00    451.000    588.00
# LodgingRevenue  35725.0    357.515912    265.671866   0.0   0.0   66.60   117.0    292.0    444.0    670.00    881.80   1413.000   2055.00
# OtherRevenue    35725.0     85.870103     96.379774   0.0   0.0    2.00    12.0     56.0    110.0    187.50    260.50    461.904   1465.00
# Revenue         35725.0    443.386015    318.581430  65.0  65.0   78.50   141.0    364.5    552.3    827.62   1080.36   1707.000   2197.75

# Kaç unique Channel vardır?
df['Channel'].nunique()
df['Channel'].value_counts()

# Agent         29657
# Direct         4496
# Corporate      1245
# Electronic      327

# Hangi Milliyetten kaçar tane rezervasyon olmuş?
df["Nationality"].value_counts()
df.groupby("Nationality")["Revenue"].count()

# Nationality
# DEU    7702
# ESP    3814
# FRA    9103
# GBR    6409
# ITA    2503
# PRT    6194


# Milliyetlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("Nationality").agg({"Revenue": "sum"})

#                 Revenue
# Nationality
# DEU          3541379.31
# ESP          1635497.67
# FRA          4406410.68
# GBR          3039657.47
# ITA          1192924.21
# PRT          2024096.05

# Channel türlerine göre göre toplam, ortalama geliri ve rezervasyon sayılarını inceleyelim
df.groupby("Channel").agg({"Revenue": ["sum", 'mean', 'count']})

#                 Revenue
#                     sum        mean  count
# Channel
# Agent       13218264.05  445.704692  29657
# Corporate     390745.36  313.851695   1245
# Direct       2131530.41  474.094842   4496
# Electronic     99425.57  304.053731    327


# Ülkelere göre Rezervasyon geliri ortalamaları nedir?
df.groupby("Nationality").agg({"Revenue": "mean"})

#                 Revenue
# Nationality
# DEU          459.799962
# ESP          428.814282
# FRA          484.061373
# GBR          474.279524
# ITA          476.597767
# PRT          326.783347


# Ülke-Channel kırılımında Revenue ortalamaları nedir?

df.groupby(["Nationality", "Channel"]).agg({"Revenue": "mean"})[0:7]

#                            Revenue
# Nationality Channel
# DEU         Agent       453.932861
#             Corporate   405.155306
#             Direct      547.891510
#             Electronic  346.241071
# ESP         Agent       432.095200
#             Corporate   273.374132
#             Direct      497.338772

# Segmentlere başlangıç
# Nationality, DistributionChannel, Age kırılımında ortalama lead time nedir ve ortalama kazançlar nedir?


df.groupby(["Nationality", "Channel", "Age"]).agg({"LeadTime": "mean",
                                                   "Revenue": "mean"})[0:20]

# Çıktıyı Revenue'a göre sıralayalım

agg_df = df.groupby(["Nationality", "Channel", "Age"]).agg({"LeadTime": "mean",
                                                            "Revenue": "mean"})
agg_df = agg_df.sort_values(by="Revenue", ascending=False)

agg_df.head()

#                              LeadTime  Revenue
# Nationality Channel    Age
# ESP         Direct     20.0      31.0   2196.0
# DEU         Corporate  41.0       5.0   1924.5
# ITA         Corporate  62.0      24.0   1748.5
# DEU         Corporate  60.0      68.0   1596.5
# GBR         Electronic 27.0       9.0   1566.4

# Indekste yer alan isimleri değişken ismine çevirelim

agg_df.index
agg_df = agg_df.reset_index()
agg_df.head()

#   Nationality     Channel   Age  LeadTime  Revenue
# 0         ESP      Direct  20.0      31.0   2196.0
# 1         DEU   Corporate  41.0       5.0   1924.5
# 2         ITA   Corporate  62.0      24.0   1748.5
# 3         DEU   Corporate  60.0      68.0   1596.5
# 4         GBR  Electronic  27.0       9.0   1566.4

# İlk veri setindeki gözlem boyutuna bakalım (35709, 8)
df.shape

# Gruplamadan sonraki gözlem boyutu (1209, 5)
agg_df.shape

# Age değişkeninin dagilimlarini inceleyelim ve bunlari kategorik degiskene cevirelim
df['Age'].hist()
plt.show()

# AGE değişkeninin nerelerden bölüneceğini belirtelim:
# 18i dahil edebilmek icin 17 ile baslattik, verisetinde 17 yasinda konuk yok.
bins = [17, 25, 40, 50, 60, agg_df["Age"].max()]
labels = ['18_25', '26_40', '41_50', '51_60', '60+']
agg_df["age_cat"] = pd.cut(agg_df["Age"], bins, labels=labels)

agg_df.head()

#   Nationality     Channel   Age  LeadTime  Revenue age_cat
# 0         ESP      Direct  20.0      31.0   2196.0   18_25
# 1         DEU   Corporate  41.0       5.0   1924.5   41_50
# 2         ITA   Corporate  62.0      24.0   1748.5     60+
# 3         DEU   Corporate  60.0      68.0   1596.5   51_60
# 4         GBR  Electronic  27.0       9.0   1566.4   26_40

# 18-25 yas aralığındaki kişileirin harcamaları daha fazla görünüyor.
agg_df.groupby('age_cat')["Revenue"].mean()
agg_df.groupby('age_cat').agg({"Revenue": "mean"})

#             Revenue
# age_cat
# 18_25    512.206998
# 26_40    407.179816
# 41_50    406.624691
# 51_60    430.374044
# 60+      422.929742

agg_df.head()

# Yöntem 1
agg_df['customers_level_based'] = [row[0].upper() + "_" + row[1].upper() + "_" + row[5].upper() for row in
                                   agg_df.values]

# Yöntem 2
cols = [col for col in agg_df.columns if col not in ["Age", "LeadTime", 'Revenue']]
agg_df['customers_level_based'] = agg_df.apply(lambda x: "_".join(x[col] for col in cols).upper(), axis=1)

# Yöntem 3
agg_df['customers_level_based'] = (agg_df[['Nationality', 'Channel', "age_cat"]].agg('_'.join, axis=1)).str.upper()

# Amacımıza bir adım daha yaklaştık.
# Burada ufak bir problem var. Birçok aynı segment olacak.
# örneğin DEU_AGENT_60+ segmentinden birçok sayıda olabilir.
# kontrol edelim:
agg_df["customers_level_based"].value_counts()

# DEU_AGENT_60+           31
# PRT_AGENT_60+           30

# Bu sebeple segmentlere göre groupby yaptıktan sonra revenue ortalamalarını almalı ve segmentleri tekilleştirmeliyiz.
# Burada leadtimelari da bir hedef degisken gibi incelemek iyi olabilir

agg_df_final = agg_df.groupby("customers_level_based").agg({"Revenue": "mean",
                                                            'LeadTime': "mean"})

# customers_level_based index'te yer almaktadır. Bunu değişkene çevirelim.
agg_df_final = agg_df_final.reset_index()
agg_df_final.head()

#   customers_level_based     Revenue    LeadTime
# 0       DEU_AGENT_18_25  560.716760  103.129221
# 1       DEU_AGENT_26_40  449.799012   78.828552
# 2       DEU_AGENT_41_50  492.285417  104.734114
# 3       DEU_AGENT_51_60  500.283815  127.269332
# 4         DEU_AGENT_60+  360.369899  243.133928

#############################################
# GÖREV 7: Yeni müşterileri (DEU_AGENT_18_25) segmentlere ayırınız.
#############################################
# Revenu'a göre segmentlere ayıralım ve segmentleri betimleyelim

agg_df_final["SEGMENT"] = pd.qcut(agg_df_final["Revenue"], 4, labels=["D", "C", "B", "A"])

agg_df_final.groupby("SEGMENT").agg({"Revenue": ["count", "mean", "sum", "max", "min"]}).reset_index()

#   SEGMENT Revenue
#             count        mean           sum         max         min
# 0       D      29  216.516813   6278.987575  290.916667  116.000000
# 1       C      29  341.635048   9907.416379  413.803123  295.126296
# 2       B      29  470.204172  13635.920997  503.966599  419.286899
# 3       A      29  596.331327  17293.608481  818.187500  504.546095

agg_df_final.groupby("SEGMENT").agg({"Revenue": ["count", "mean"],
                                     "LeadTime": ["count", "mean"]}).reset_index()

#   SEGMENT Revenue             LeadTime
#             count        mean    count       mean
# 0       D      29  216.516813       29  22.210802
# 1       C      29  341.635048       29  56.291879
# 2       B      29  470.204172       29  80.206429
# 3       A      29  596.331327       29  68.800687


#############################################
# Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################

# Nationality   # Channel        # Age
# ---           ---              ---
# PRT           # _AGENT         # _18_25
# GBR           # _DIRECT        # _26_40
# DEU           # _CORPORATE     # _41_50
# FRA           # _ELECTRONIC    # _51_60
# ESP                            # _60+
# ITA

new_guest = "PRT_AGENT_18_25"

agg_df_final[agg_df_final["customers_level_based"] == new_guest]

#    customers_level_based     Revenue   LeadTime SEGMENT
# 98       PRT_AGENT_18_25  402.508236  62.404329       C


new_guest = "ITA_ELECTRONIC_51_60"
agg_df_final[agg_df_final["customers_level_based"] == new_guest]

#    customers_level_based     Revenue  LeadTime SEGMENT
# 96  ITA_ELECTRONIC_51_60  172.666667      12.0       D
