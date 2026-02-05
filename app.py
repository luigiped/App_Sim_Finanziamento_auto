import streamlit as st
import pandas as pd
import dataframe as df_manager
import logica as lg

#per installare tutte le dipendenze del progetto, eseguire il comando:
#pip install -r requirements.txt

# Configurazione pagina
st.set_page_config(page_title="Analisi Finanziamento Auto", layout="wide")

#avvio streamlit app.py --> streamlit run app.py


# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    /* 1. Metriche */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 5px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        color: #4da3ff !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }

    /* 2. Tab */
    [data-baseweb="tab-list"] p {
        font-size: 20px !important;
        font-weight: bold !important;
    }
            
    /* 3. Tabelle Ammortamento (Target specifico per Streamlit Canvas) */
    [data-testid="stDataFrame"] div[role="gridcell"] div {
        font-size: 22px !important; /* Testo celle */
    }
    [data-testid="stDataFrame"] div[role="columnheader"] span {
        font-size: 22px !important; /* Testo intestazioni */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Dashboard Analisi Finanziamento Auto")

# --- SIDEBAR: INPUT UTENTE ---
st.sidebar.header("1. Dati Veicolo e Mercato")
prezzo = st.sidebar.number_input("Prezzo Auto (€)", value=41000, step=500)
anticipo = st.sidebar.number_input("Anticipo (€)", value=5000, step=500)
resa_investimento = st.sidebar.slider("Rendimento Annuo Investimenti (%)", 0.0, 10.0, 5.0)

st.sidebar.divider()
st.sidebar.header("2. Parametri Svalutazione")
deprezzamento_annuo = st.sidebar.slider("Svalutazione Annua (%)", 5, 30, 15)
anni_analisi = st.sidebar.slider("Anni di possesso", 1, 10, 3)

st.sidebar.divider()
st.sidebar.header("3. Finanziamenti")
col_c1, col_c2 = st.sidebar.columns(2)
with col_c1:
    taeg_c = st.sidebar.number_input("TAEG Classico (%)", value=7.0)
with col_c2:
    mesi_c = st.sidebar.number_input("Mesi Classico", value=60)

st.sidebar.divider()
taeg_m = st.sidebar.number_input("TAEG Maxi Rata (%)", value=4.74)
mesi_m = st.sidebar.number_input("Mesi Maxi Rata", value=35)
maxi_r = st.sidebar.number_input("Valore Maxi Rata (€)", value=21762)
taeg_rifin = st.sidebar.number_input("TAEG Rifin. Maxi (%)", value=7.0)
mesi_rifin = st.sidebar.number_input("Mesi Rifin. Maxi", value=36)

# --- LOGICA DI CALCOLO ---
dati_c = {"taeg": taeg_c, "mesi": mesi_c}
dati_m = {"taeg": taeg_m, "mesi": mesi_m, "maxi_rata": maxi_r}
dati_r = {"taeg": taeg_rifin, "mesi": mesi_rifin}

risultato_analisi = lg.analisi_comp(prezzo, anticipo, resa_investimento, dati_c, dati_m)
res_rifin = lg.ri_finanziamento(maxi_r, dati_r["taeg"], dati_r["mesi"])
res_confronto = lg.confronto_riscatto_rifinanziamento(prezzo, deprezzamento_annuo, anni_analisi, maxi_r, res_rifin["interessi_tot"])
res_riepilogo = lg.tabella_totale_riassuntiva(prezzo, risultato_analisi, res_rifin["interessi_tot"])

# --- FUNZIONI DI FORMATTAZIONE ---
def format_euro(val):
    if isinstance(val, (int, float)): return f"€{val:,.2f}".replace(",", " ").replace(".", ",").replace(" ",".")
    return val

def color_rank(val):
    color = ''
    if val == 'OTTIMALE': color = 'background-color: #45bf48; color: #030303; font-weight: bold'
    elif val == 'PEGGIORE': color = 'background-color: #d63a29; color: #030303'
    elif val == 'INTERMEDIA': color = 'background-color: #f5902c; color: #030303'
    return color

# --- VISUALIZZAZIONE METRICHE FORMATTATE ---
m1, m2, m3, m4 = st.columns(4)

# Usiamo la tua funzione format_euro per trasformare i numeri in stringhe belle da vedere
m1.metric("Rata Classico", format_euro(risultato_analisi['CLASSICO']['rata']))
m2.metric("Rata Maxi", format_euro(risultato_analisi['MAXI_RATA']['rata']))
m3.metric("Valore Residuo", format_euro(res_confronto['Valore di Mercato']))
m4.metric("Surplus/Gap",format_euro(res_confronto['Surplus Attuale']), delta_color="normal")

# --- VISUALIZZAZIONE ---
st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Analisi Costi", "📅 Piani Ammortamento", "📉 Valore & Riscatto"])

with tab1:
    st.subheader("Confronto Strategie e Impatto Finanziario")
    
    # Rapporto 1:1 per dare lo stesso spazio a entrambe
    col_ranking, col_riepilogo = st.columns([1, 1])
    
    with col_ranking:
        st.markdown("##### 🏆 Dettaglio Parametri")
        df_ranking = df_manager.impacchetta_ranking_verticale(risultato_analisi)
        
        # Creiamo una funzione di formattazione che controlla il nome della riga
        def smart_format(val, row_name):
            # Se la riga è "N° Rate", formattiamo come intero semplice
            if "N° Rate" in str(row_name):
                return f"{int(val)}" if isinstance(val, (int, float)) else val
            # Altrimenti usiamo la tua funzione format_euro
            return format_euro(val)

        # Applichiamo la formattazione riga per riga usando uno Styler personalizzato
        st.table(df_ranking.style.applymap(
            color_rank, 
            subset=pd.IndexSlice[['RANKING'], :]
        ).format(lambda v: smart_format(v, df_ranking.index[df_ranking.values.tolist().index(next(x for x in df_ranking.values.tolist() if v in x))] if v in df_ranking.values else "")))
    
    with col_riepilogo:
        st.markdown("##### 💰 Costo Totale Reale")
        df_riepilogo = df_manager.impacchetta_riepilogo_finale(res_riepilogo)
        
        # FIX ERRORE: Usiamo una funzione lambda per gestire la percentuale
        # Questo evita l'errore se il dato è già una stringa
        st.table(df_riepilogo.style.format({
            "ESBORSO TOTALE (€)": format_euro,
            "VARIAZIONE % (vs Listino)": lambda x: f"{x}%" if isinstance(x, (int, float)) else x
        }))

with tab2:
    st.subheader("Dettaglio Rate e Ammortamento")
    df_c, df_m, df_ri = df_manager.impacchetta_piani_ammortamento(prezzo, anticipo, dati_c, dati_m, dati_r)
    sel = st.segmented_control("Seleziona Piano", ["Classico", "Maxi Rata", "Rifinanziamento"], default="Classico")
    
    mapping = {"Classico": df_c, "Maxi Rata": df_m, "Rifinanziamento": df_ri}
    st.dataframe(mapping[sel].style.format(format_euro), use_container_width=True, height=400)

with tab3:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Andamento Svalutazione")
        df_sval = df_manager.impacchetta_svalutazione(prezzo, deprezzamento_annuo, anni_analisi)
        st.area_chart(df_sval)
    with c2:
        st.subheader("Verifica Riscatto")
        df_risc = df_manager.impacchetta_confronto(res_confronto)
        st.table(df_risc.style.format(format_euro))
        
        if "NON SOSTENIBILE" in res_confronto["Sostenibilità"]:
            st.error("⚠️ Attenzione: Il rifinanziamento costa più del valore dell'auto!")
        else:
            st.success("✅ Operazione sostenibile finanziariamente")