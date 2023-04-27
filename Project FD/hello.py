# Import des bibliothèques nécessaires
import pandas as pd
from itertools import combinations
from functions import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.pdfgen import canvas
import io
from flask import send_file
from functions import Apriori_classique
from functions import apriori_Close
from functions import apriori_reduce_transactions
import os
import pickle



#from sklearn.preprocessing import StandardScaler
#from mlxtend.preprocessing import TransactionEncoder
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('index.html')

# @app.route('/hello')
# def hello():
#    return render_template('hello.html')

@app.route('/upload', methods = ['GET', 'POST'])

def uploader_file():
   
      if request.method == 'POST':
        f = request.files['file']
        min_sup =float( request.form['min_supp'])
        min_conf = float(request.form['min_confidence'] )
        type_algorithme= request.form['type_algorithme']

        
       #  min_lift=request.form['min_lift']
        filename = f.filename    
        f.save(f.filename)

      # Chargement des données
      df = pd.read_csv(filename,header=None)   
      # Nettoyage des données
      #df.dropna(inplace=True) # suppression des valeurs manquantes
      #df.fillna("0",inplace=True)
      #df.drop_duplicates(inplace=True) # suppression des doublons
      #df=df.astype(str)
      df.dropna(inplace=True) # suppression des valeurs manquantes
      df.drop_duplicates(inplace=True) # suppression des doublons Lignes 
      df = df.astype(str)


      
      
      array=df.values
      transactions=[]
     
      for i in range(0,len(df)):
           transactions.append([str(df.values[i,j]) for j in range(0,len(df.columns)) if str(df.values[i,j])!="0"])
      
      if(type_algorithme == '1'):
            #rules ,frequent_itemsets= apriori_Classique_frozenset(transactions, 0.04, 0.04,1)
            freq_itemsets, association_rules = Apriori_classique(transactions, min_sup, min_conf)
      elif (type_algorithme =="2"): 
            freq_itemsets, association_rules = apriori_reduce_transactions(transactions, min_sup,min_conf)      
      elif (type_algorithme=="3"):
            freq_itemsets, association_rules = apriori_Close(transactions, min_sup, min_conf)   
            
           
      
      # Affichage des règles d'association générées
      #freq_items_dict = {tuple(sorted(list(k))): v for k, v in frequent_itemsets.items()}
      # Convert float keys to string keys
      #itemsets_frequens = {str(k): v for k, v in freq_items_dict.items()}

      # Convert float keys to string keys
   

      



# Écrire les frozensets dans le fichier avec un saut de ligne
     
      with open("frozensets.txt", "w") as f:
        f.write('Les itemset frequent  :' + '\n')
        for freq in freq_itemsets :
             f.write(str(freq) + '\n')
        for rule in association_rules:
             f.write(str(rule) + '\n')
      PAGE_HEIGHT = 792  # 11 inch x 72 pt / inch
      PAGE_WIDTH = 612  # 8.5 inch x 72 pt / inch
# Générer le PDF
      c = canvas.Canvas("static/frozensets.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
      y = 750  # Position verticale de départ

# Lire les frozensets à partir du fichier et les ajouter au PDF
      with open("frozensets.txt", "r") as f:
       for line in f:
              c.drawString(50, y, line.strip())
              y -= 20  # Saut de ligne
              if y<50 : 
                  c.showPage()
                  y = PAGE_HEIGHT - 50
      c.save()

            # Return the HTML template with links to the plot.png and frozensets.pdf files
      return render_template('result.html',  pdf_path='/frozensets.pdf')


@app.route('/frozensets.pdf')
def frozensets_pdf():
    return send_file('frozensets.pdf', mimetype='application/pdf')

if __name__ == '__main__':
   app.run(debug = True)