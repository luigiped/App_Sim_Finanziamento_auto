#improto librerie
import numpy_financial as npf

## Finanziamento classico

def finanziamento_classic (prezzo_auto, anticipo, taeg, mesi):
    capitale_fin = prezzo_auto - anticipo
    tasso_mensile = (taeg/100)/12

    #ammortamento alla francese
    rata = abs(npf.pmt(tasso_mensile, mesi, capitale_fin))
    interessi_tot = (rata*mesi)-capitale_fin

    return {
        "rata": round(rata,2),
        "interessi_tot": round(interessi_tot,2),
        "capitale_fin": capitale_fin,
    }

## Finanziamento con maxirata

def finanziamento_maxirata (prezzo_auto, anticipo, taeg, mesi, maxi_rata):
    capitale_fin = prezzo_auto - anticipo
    tasso_mensile = (taeg/100)/12

    #ammoratamento alla francesce

    rata = abs(npf.pmt(tasso_mensile, mesi,capitale_fin, fv = -maxi_rata))
    interessi_tot = (rata*mesi) + maxi_rata - capitale_fin

    return {
        "rata":round(rata,2),
        "interessi_tot":round(interessi_tot,2),
        "maxi_rata":maxi_rata,
    }
#funzione per il calcolo del ri-finanziamento
def ri_finanziamento (maxi_rata, taeg, mesi):  
    tasso_mensile = (taeg/100)/12
    rata = abs(npf.pmt(tasso_mensile,mesi,maxi_rata))
    interessi_tot = (rata*mesi)-maxi_rata
    return {
        "rata":round(rata,2),
        "interessi_tot":round(interessi_tot,2),
    }

# generazione piano di ammortamento

def piano_ammortamento (capitale_fin, taeg, mesi, rata, fv_finale=0):
    tasso_mese = (taeg/100)/12
    piano_ammortamento = []
    residuo = capitale_fin

    for piano in range(1,mesi+1):
        interessi_mese = residuo * tasso_mese
        quota_capitale = rata - interessi_mese
        residuo -= quota_capitale

        piano_ammortamento.append({
            "Mese": piano,
            "Rata": rata,
            "Interessi": round(interessi_mese,2),
            "Quota capitale": round(quota_capitale,2),
            "Capitale residuo": max(0, round(residuo,2)),
    
        })
    return piano_ammortamento

# calcolo costo opportunità

def costo_opp_cash (prezzo_auto, rendimento_annuo):
    r_decimale = rendimento_annuo / 100  # 0.05
    i_mensile = r_decimale / 12          # 0.004166..
    mesi =12
    montante_totale = prezzo_auto * (1 + i_mensile)**mesi
    guadagno_perso = montante_totale - prezzo_auto
    return round(guadagno_perso,2)

def costo_opp(anticipo, rendimento_annuo, mesi):
    # Esempio: capitale=7500, rendimento_annuo=5, mesi=35
    
    r_decimale = rendimento_annuo / 100  # 0.05
    i_mensile = r_decimale / 12          # 0.004166...
    
    # Formula interesse composto: C * (1 + i)^n
    montante_totale = anticipo * (1 + i_mensile)**mesi
    guadagno_perso = montante_totale - anticipo
    
    return round(guadagno_perso,2)

# analisi comparativa
def analisi_comp (prezzo, anticipo, rendimento_annuo, dati_classic, dati_maxi):
    # --- 1. CONTANTI ---
    co_cash = costo_opp_cash(prezzo, rendimento_annuo)
    
    costo_reale_cash = prezzo 

    # --- 2. FINANZIAMENTO CLASSICO ---
    res_c = finanziamento_classic(prezzo, anticipo, dati_classic["taeg"], dati_classic["mesi"])
    # CO calcolato sulla liquidità risparmiata (Prezzo - Anticipo)
    co_classic = costo_opp( anticipo, rendimento_annuo, dati_classic["mesi"])
    costo_reale_classic = anticipo + (res_c["rata"] * dati_classic["mesi"])

    # --- 3. FINANZIAMENTO MAXIRATA ---
    res_m = finanziamento_maxirata(prezzo, anticipo, dati_maxi["taeg"], dati_maxi["mesi"], dati_maxi["maxi_rata"])
    # CO calcolato sulla liquidità risparmiata inizialmente
    co_maxi = costo_opp(anticipo, rendimento_annuo, dati_maxi["mesi"])
    costo_reale_maxi = anticipo + (res_m["rata"] * dati_maxi["mesi"]) + dati_maxi["maxi_rata"]

    # --- RANKING DINAMICO ---
    costi = {"CONTANTI": costo_reale_cash, "CLASSICO": costo_reale_classic, "MAXI_RATA": costo_reale_maxi}
    sorted_keys = sorted(costi, key=costi.get)
    rank_risultati = {sorted_keys[0]: "OTTIMALE", sorted_keys[1]: "INTERMEDIA", sorted_keys[2]: "PEGGIORE"}

    return {
        "CONTANTI": {
            "costo_auto": prezzo, "anticipo": 0, "rata": 0, "rate_n": 0, 
            "maxi": 0, "interessi": 0, "co": co_cash, 
            "costo_reale": costo_reale_cash, "rank": rank_risultati["CONTANTI"]
        },
        "CLASSICO": {
            "costo_auto": prezzo, "anticipo": anticipo, "rata": res_c['rata'], 
            "rate_n": dati_classic['mesi'], "maxi": 0, "interessi": res_c['interessi_tot'], 
            "co": co_classic, "costo_reale": costo_reale_classic, "rank": rank_risultati["CLASSICO"]
        },
        "MAXI_RATA": {
            "costo_auto": prezzo, "anticipo": anticipo, "rata": res_m['rata'], 
            "rate_n": dati_maxi['mesi'], "maxi": dati_maxi['maxi_rata'], 
            "interessi": res_m['interessi_tot'], "co": co_maxi, 
            "costo_reale": costo_reale_maxi, "rank": rank_risultati["MAXI_RATA"]
        }
    }
# tabella valore auto
def valore_auto(valore_iniziale, deprezzamento_annuo, anni):
    valori = []
    for anno in range(0, anni + 1):
        valore_residuo = valore_iniziale * ((1 - deprezzamento_annuo / 100) ** anno)
        valori.append({
            "Anno": anno,
            "Valore residuo": round(valore_residuo, 2)
        })
    return valori

#tabella comparativa riscatto vs rifinanziamento
def confronto_riscatto_rifinanziamento(prezzo_auto, deprezzamento_annuo, anni, maxi_rata, interessi_tot, km_extra=0, danni=0):
    # 1. Recupero valore di mercato dalla funzione valore auto
    svalutazione = valore_auto(prezzo_auto, deprezzamento_annuo, anni)
    valore_mercato = svalutazione[-1]["Valore residuo"]
    
    # 2. Valore Netto (al netto di km e danni)
    valore_netto = valore_mercato - km_extra - danni
    
    # 3. Surplus (Differenza tra valore mercato e maxi rata)
    surplus = valore_netto - maxi_rata
    
    # 4. LOGICA DI SOSTENIBILITÀ
    # Se interessi_tot > surplus allora NON è sostenibile
    sostenibile = interessi_tot <= surplus
    
    # 5. Calcolo Totale dei due finanziamenti (Costo Totale Storico)
    # sommare il costo del primo finanziamento
    # qui calcoliamo l'incremento di costo del secondo
    esito_sostenibilita = "SOSTENIBILE" if sostenibile else "NON SOSTENIBILE (Interessi > Surplus)"

    return {
        "Valore di Mercato": round(valore_mercato, 2),
        "Valore Netto": round(valore_netto, 2),
        "Surplus Attuale": round(surplus, 2),
        "Interessi Rifinanziamento": round(interessi_tot, 2),
        "Sostenibilità": esito_sostenibilita,
        "Convenienza Riscatto": "SI" if surplus > 0 else "NO"
    }

def tabella_totale_riassuntiva(prezzo_auto, risultato_analisi, interessi_tot):
    # 1. Estraggo i costi reali calcolati nella funzione 'analisi_comp'
    totale_cash = risultato_analisi["CONTANTI"]["costo_reale"]
    totale_classico = risultato_analisi["CLASSICO"]["costo_reale"]
    
    # 2. Il costo della Maxi Rata semplice (senza rifinanziamento)
    totale_maxi_semplice = risultato_analisi["MAXI_RATA"]["costo_reale"]
    
    # 3. Il costo della Maxi Rata SE RIFINANZIATA (Costo originale + nuovi interessi)
    totale_rifinanziato = totale_maxi_semplice + interessi_tot

    # Funzione interna per calcolare la variazione % rispetto al prezzo auto
    def calc_var(totale):
        return round(((totale / prezzo_auto) - 1) * 100, 2)

    return {
        "CONTANTI": {
            "Costo Finale": round(totale_cash, 2),
            "Variazione %": f"{calc_var(totale_cash)}%"
        },
        "FIN_CLASSICO": {
            "Costo Finale": round(totale_classico, 2),
            "Variazione %": f"{calc_var(totale_classico)}%"
        },
        "MAXI_RATA_CASH": {
            "Costo Finale": round(totale_maxi_semplice, 2),
            "Variazione %": f"{calc_var(totale_maxi_semplice)}%"
        },
        "RIFINANZIAMENTO": {
            "Costo Finale": round(totale_rifinanziato, 2),
            "Variazione %": f"{calc_var(totale_rifinanziato)}%"
        }
    }