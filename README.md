## App_Sim_Finanziamento_Auto

Simulatore finanziario per la scelta del tipo di finanziamento relativo all'acquisto di un'automobile.
Il progetto è a scopo didattico e nasce come esercizio per sviluppare una piccola web app.

# Logica del progetto
  logica.py
  Il file contiene tutte le funzioni necessarie al funzionamento logico della web app.


# Calcolo rata finanziamento
  Creazione delle funzioni per il calcolo della rata nel caso di finanziamento classico e maxi-rata.


# Generazione piani di ammortamento alla francese
  Funzione per generare i piani di ammortamento secondo il metodo alla francese.


# Calcolo del costo opportunità
  Funzione che calcola quanto si sarebbe potuto guadagnare investendo l'anticipo dell'auto per la stessa durata del finanziamento.


# Analisi comparativa

  Funzione che confronta tre modalità di acquisto: cash, finanziamento classico e finanziamento maxi-rata.
  Da qui si ricavano:
  
  il costo finale dell’auto in base ai dati inseriti dall’utente;

  il costo opportunità calcolato precedentemente;

  un ranking della soluzione migliore, con valori: ottimo, intermedio e peggiore.

# Calcolo valore auto
  Funzione che stima il valore di mercato dell’auto in base agli anni di utilizzo e a un tasso di deprezzamento definito tramite uno slider.

# Tabella comparativa finale e calcolo valore residuo
  Funzione per valutare la convenienza del riscatto dell’auto alla fine dell’ultimo mese della maxi-rata o in caso di rifinanziamento.
  Include il calcolo di un nuovo piano di ammortamento e la determinazione del valore finale pagato tra finanziamento iniziale e rifinanziamento.

# dataframe.py
  Questo file aggrega i dati provenienti da logica.py in dataframe tramite la libreria pandas, organizzando i dati in tabelle per una manutenzione più semplice e veloce del codice.

# app.py
 Interfaccia grafica del simulatore realizzata con la libreria Streamlit.
