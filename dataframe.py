import pandas as pd
import logica as lg

print(lg)

#creazione data frame per il piano di ammortamento
def impacchetta_piani_ammortamento(prezzo_auto, anticipo, dati_classic, dati_maxi, dati_rifin):
    """
    Prende i dati di input e restituisce i DataFrame dei piani di ammortamento.
    """
    
    # --- 1. PIANO CLASSICO ---
    res_c = lg.finanziamento_classic(prezzo_auto, anticipo, dati_classic["taeg"], dati_classic["mesi"])
    lista_c = lg.piano_ammortamento(res_c["capitale_fin"], dati_classic["taeg"], dati_classic["mesi"], res_c["rata"])
    df_classico = pd.DataFrame(lista_c).set_index("Mese")
    
    # --- 2. PIANO MAXI RATA ---
    capitale_m = prezzo_auto - anticipo
    res_m = lg.finanziamento_maxirata(prezzo_auto, anticipo, dati_maxi["taeg"], dati_maxi["mesi"], dati_maxi["maxi_rata"])
    lista_m = lg.piano_ammortamento(capitale_m, dati_maxi["taeg"], dati_maxi["mesi"], res_m["rata"])
    df_maxi = pd.DataFrame(lista_m).set_index("Mese")
    
    # --- 3. PIANO RIFINANZIAMENTO ---
    res_ri = lg.ri_finanziamento(dati_maxi["maxi_rata"], dati_rifin["taeg"], dati_rifin["mesi"])
    lista_ri = lg.piano_ammortamento(dati_maxi["maxi_rata"], dati_rifin["taeg"], dati_rifin["mesi"], res_ri["rata"])
    df_rifin = pd.DataFrame(lista_ri).set_index("Mese")
    
    return df_classico, df_maxi, df_rifin

# 2. LA FUNZIONE DI IMPACCHETTAMENTO PANDAS
def impacchetta_ranking_verticale(risultato_analisi):
    """
    Trasforma il dizionario in una tabella dove i parametri sono sulle righe
    e le modalità di acquisto sono sulle colonne.
    """
    # 1. Creiamo il DataFrame
    df = pd.DataFrame(risultato_analisi)
    
    # 2. Selezioniamo le righe nell'ordine desiderato
    indici_ordinati = [
        "costo_auto", "anticipo", "rata", "rate_n", 
        "maxi", "interessi", "co", "costo_reale", "rank"
    ]
    df = df.reindex(indici_ordinati)
    
    # 3. Rinominiamo le righe (l'indice) per l'interfaccia finale
    df.index = [
        "Prezzo Auto", 
        "Anticipo", 
        "Rata Mensile", 
        "N° Rate", 
        "Maxi Rata", 
        "Interessi Totali.", 
        "Costo Opportunità", 
        "COSTO REALE", 
        "RANKING"
    ]
    
    return df
#### dataframe per il valore auto
def impacchetta_svalutazione(prezzo_auto, deprezzamento, anni):
    """
    Trasforma la lista generata da valore_auto in un DataFrame 
    che mostra la svalutazione anno per anno.
    """
    # 1. Chiamiamo la tua funzione originale
    dati_svalutazione = lg.valore_auto(prezzo_auto, deprezzamento, anni)
    
    # 2. Creiamo il DataFrame
    df = pd.DataFrame(dati_svalutazione)
    
    # 3. Rendiamo la tabella più pulita
    df.columns = ["Anno", "Valore Stimato (€)"]
    df.set_index("Anno", inplace=True)
    
    return df
##data frame per tabella confronto riscatto
def impacchetta_confronto(risultato_confronto):
    """
    Trasforma il dizionario di convenienza riscatto in un 
    DataFrame verticale pronto per la visualizzazione.
    """
    # 1. Creiamo il DataFrame dal dizionario
    # Usiamo orient='index' per avere le chiavi del dizionario come righe
    df = pd.DataFrame.from_dict(risultato_confronto, orient='index', columns=['Valore'])
    
    # 2. Rinominiamo l'indice per togliere i nomi tecnici (opzionale ma consigliato)
    # L'indice avrà già i nomi "Valore di Mercato", "Valore Netto", ecc. 
    # definiti nel tuo return.
    
    return df
##tabella riassuntiva totale
def impacchetta_riepilogo_finale(risultato_riepilogo):
    """
    Trasforma il dizionario dei costi finali in un DataFrame Pandas
    ordinato per mostrare l'esborso totale e la variazione percentuale.
    """
    # 1. Creiamo il DataFrame e lo ruotiamo per avere le modalità sulle righe
    df = pd.DataFrame(risultato_riepilogo).T
    
    # 2. Rinominiamo le colonne per una lettura chiara
    df.columns = ["ESBORSO TOTALE (€)", "VARIAZIONE % (vs Listino)"]
    
    # 3. Rinominiamo gli indici per renderli più "parlanti"
    df.index = [
        "Acquisto in Contanti", 
        "Finanziamento Classico", 
        "Maxi Rata (Riscatto Cash)", 
        "Rifinanziamento Maxi Rata"
    ]
    
    return df