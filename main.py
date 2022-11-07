import os
import time
from datetime import datetime
import requests
from dotenv import load_dotenv
import json

load_dotenv()
# Dotenv è una libreria che permette di salvare la propria api key all'interno di una ".env" esterna al progetto.
# Funziona insieme alla libreria "os".
api_key = os.getenv("api_key")  # chiave api personale per scaricare i dati salvata all'esterno del progetto.


class Dati:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  # link da cui prendere i dati.
        self.headers = {
            'Accepts': 'application/json',  # formato risposta: json.
            'X-CMC_PRO_API_KEY': api_key  # chiave api.
        }

    def richiesta_dati(self, inizio, fine, fiat, classifica, direzione):
        params = dict(start=inizio, limit=fine, convert=fiat, sort=classifica, sort_dir=direzione)
        # Parametri per predisporre la classifica a nostro piacimento.
        # Inizio e fine per impostare il numero di criptovalute da analizzare partendo da x e finendo in y;
        # fiat, indica il tipo di valuta che sarà USD in questo caso;
        # classifica, per scegliere che tipo di dati si ha bisogno;
        # direzione, per scegliere se interessa avere un ordine crescente o decrescente.
        r = requests.get(url=self.url, headers=self.headers, params=params).json()  # richiesta dati.
        return r['data']  # riceve dati in formato json.


dati = Dati()

while 1:

    # dizionario contenente tutti i dati in json.
    dati_stampa = {}

    # Punto numero 1

    volume_dati = dati.richiesta_dati('1', '1', 'USD', 'volume_24h', 'desc')
    volume_simbolo = volume_dati[0]['symbol']
    volume = str(round(volume_dati[0]['quote']['USD']['volume_24h'], 2)) + " USD"
    dati_stampa["La criptovaluta con il volume maggiore (in $) delle ultime 24 ore"] = []
    dati_stampa["La criptovaluta con il volume maggiore (in $) delle ultime 24 ore"].append({
        "Simbolo": volume_simbolo,
        "Volume_24h": volume
    })

    # Punto numero 2

    incrementi_dati = dati.richiesta_dati('1', '10', 'USD', 'percent_change_24h', 'desc')
    lista_incrementi = []
    for incremento in incrementi_dati:
        lista_incrementi.append(incremento['name'])
        lista_incrementi.append(f"con simbolo: {incremento['symbol']}")
        lista_incrementi.append(f"con una percentuale pari a: "
                                f"{round(incremento['quote']['USD']['percent_change_24h'], 2)} %")
    diminuzioni_dati = dati.richiesta_dati('1', '10', 'USD', 'percent_change_24h', 'asc')
    lista_diminuzioni = []
    for diminuzione in diminuzioni_dati:
        lista_diminuzioni.append(diminuzione['name'])
        lista_diminuzioni.append(f"con simbolo: {diminuzione['symbol']}")
        lista_diminuzioni.append(f"con una percentuale pari a: "
                                 f"{round(diminuzione['quote']['USD']['percent_change_24h'], 2)} %")
    dati_stampa["Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)"] = []
    dati_stampa["Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)"].append({
        "Criptovalute_migliori": lista_incrementi,
        "Criptovalute_peggiori": lista_diminuzioni
    })

    # Punto numero 3

    capitalizzazione_dati = dati.richiesta_dati('1', '20', 'USD', 'market_cap', 'desc')
    criptovalute = []
    prezzo_totale = 0.0
    for criptovaluta in capitalizzazione_dati:
        prezzo_totale += criptovaluta['quote']['USD']['price']
        criptovalute.append(criptovaluta['name'])
        criptovalute.append(f"con simbolo: {criptovaluta['symbol']}")
    prezzo_totale_USD = str(round(prezzo_totale, 2)) + " USD"
    dati_stampa["Quantita di denaro necessaria per acquistare una unita di ciascuna delle prime 20 criptovalute"] = []
    dati_stampa["Quantita di denaro necessaria per acquistare una unita di ciascuna delle prime 20 "
                "criptovalute"].append({"Criptovalute": criptovalute,
                                        "Denaro_necessario": prezzo_totale_USD
                                        })

    # Punto numero 4

    volumi_dati = dati.richiesta_dati('1', '1000', 'USD', 'volume_24h', 'desc')
    volume_minimo = 76000000
    criptovalute_accettabili = []
    lista_prezzi = []
    for volume in volumi_dati:
        if volume['quote']['USD']['volume_24h'] > volume_minimo:
            criptovalute_accettabili.append(volume['name'])
            criptovalute_accettabili.append(f"con simbolo: {volume['symbol']}")
            lista_prezzi.append(volume['quote']['USD']['price'])

    prezzo_totale_2 = 0.0
    for prezzo in lista_prezzi:
        prezzo_totale_2 += prezzo
    prezzo_totale_2_USD = str(round(prezzo_totale_2, 2)) + " USD"
    dati_stampa["La quantita di denaro necessaria per acquistare una unita di tutte le criptovalute il cui volume "
                "delle ultime 24 ore sia superiore a 76.000.000$"] = []
    dati_stampa["La quantita di denaro necessaria per acquistare una unita di tutte le criptovalute il cui"
                " volume delle ultime 24 ore sia superiore a 76.000.000$"].append(
        {"Criptovalute": criptovalute_accettabili, "Denaro_necessario": prezzo_totale_2_USD
         })

    # Punto numero 5

    capitalizzazione_dati = dati.richiesta_dati('1', '20', 'USD', 'market_cap', 'desc')
    prezzo_tot_oggi = 0
    prezzo_tot_ieri = 0
    for criptovaluta in capitalizzazione_dati:  # da punto 3
        prezzo_tot_ieri += criptovaluta['quote']['USD']['price'] / \
                           (1 + (criptovaluta['quote']['USD']['percent_change_24h'] / 100))
        prezzo_tot_oggi += criptovaluta['quote']['USD']['price']
    guadagno_perdita_percentuale = ((prezzo_tot_oggi - prezzo_tot_ieri) / prezzo_tot_oggi) * 100
    dati_stampa["La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unita di "
                "ciascuna delle prime 20 criptovalute il giorno prima"] = []
    dati_stampa["La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unita "
                "di ciascuna delle prime 20 criptovalute il giorno prima"].append(
        {"Prezzo_totale_ieri": str(round(prezzo_tot_ieri, 2)) + " USD",
         "Prezzo_totale_oggi": str(round(prezzo_tot_oggi, 2)) + " USD",
         "Percentuale_perdita_guadagno": str(round(guadagno_perdita_percentuale, 2)) + " %"
         })

    # data e ora su file json.
    now = datetime.now()
    data_ora = now.strftime("%d_%m_%Y_%H_%M_%S")

    # info progetto su file json.
    dati_stampa['Info_Progetto'] = []
    dati_stampa['Info_Progetto'].append({
        "Progetto": "Sistema di reportistica sul mondo delle Criptovalute",
        "Nome": "Alberto Toscano",
        "Ambiente di sviluppo": "Pycharm Community",
        "Linguaggio": "Python 3",
        "Destinatario": "start2impact"
    })
    # scrivere in file json.
    with open(data_ora + ".json", "w") as outfile:
        json.dump(dati_stampa, outfile, indent=4)

    # routine: stampa ogni 24 ore.
    minutes = 1440
    seconds = minutes * 60
    time.sleep(seconds)
