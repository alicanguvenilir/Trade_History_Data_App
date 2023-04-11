import pandas as pd
import requests
import json

#GET
response_API = requests.get('https://seffaflik.epias.com.tr/transparency/service/market/intra-day-trade-history?endDate=2023-04-10&startDate=2023-04-10')

#veri json dosyasına dönüştürülür
data = json.loads(response_API.text)

#veri pandas ile dataframe'e dönüştürülür
df = pd.DataFrame(data["body"]["intraDayTradeHistoryList"])


#PH ile başlayan conractların filtreleyen fonksiyon
def PH_find(conract_value):
    if "PH" in conract_value:
        return True
    return False


#PH ile başlayan conract değerleri fonksiyon yardımı ile filtrelenir
df = df[df["conract"].apply(PH_find)]


#Toplam İşlem Tutarı bulunur
df["Toplam İşlem Tutarı"] = df["price"]*df["quantity"]/10


#Toplam İşlem Miktarı bulunur
df["Toplam İşlem Miktarı"] = df["quantity"]/10


#conract değerine göre sıralanır
df.set_index("conract", inplace=True)


#conract değerleri gruplanır
ConGroup = df.groupby("conract")


#Değerler bir sonuç tablosuna dönüştürülür
result_data = pd.DataFrame(ConGroup["Toplam İşlem Tutarı"].sum())
result_data["Toplam İşlem Miktarı"] = ConGroup["Toplam İşlem Miktarı"].sum()
result_data["Ağırlıklı Ortalama Fiyat"] = result_data["Toplam İşlem Tutarı"] / result_data["Toplam İşlem Miktarı"]
final_data = result_data.reset_index()

#tarihler conract değerlerinden dönüştürülür
def dateParser(yyaaggss):
    yy = str(yyaaggss)[2] + str(yyaaggss)[3]
    aa = str(yyaaggss)[4] + str(yyaaggss)[5]
    gg = str(yyaaggss)[6] + str(yyaaggss)[7]
    ss = str(yyaaggss)[8] + str(yyaaggss)[9]
    return gg + "." + aa + ".20" + yy + " " + ss + ":00"

final_data.insert(0, "Tarih", final_data["conract"].apply(dateParser))

del final_data["conract"]

print(final_data)

final_data.to_csv(r'C:\Users\User\Desktop\my_data.csv', index=False)

