import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd
import os
from datetime import datetime

# Alphabet Mooré complet avec les lettres spéciales
ALPHABET_MOORE = {
    'basiques': ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 
                 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z'],
    'voyelles_avec_accents': ['ɛ', 'ɔ', 'ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ɛ̃', 'ɔ̃'],
    'voyelles_longues': ['ā', 'ē', 'ī', 'ō', 'ū', 'ɛ̄', 'ɔ̄'],
    'nasales': ['ŋ', 'ɲ', 'ɱ'],
    'speciaux': ['ʼ', 'ʋ', 'ɣ', 'ɓ', 'ɗ', 'ƴ', 'ʔ']
}

# Toutes les lettres Mooré dans une seule liste
ALL_MOORE_LETTERS = (
    ALPHABET_MOORE['basiques'] + 
    ALPHABET_MOORE['voyelles_avec_accents'] + 
    ALPHABET_MOORE['voyelles_longues'] + 
    ALPHABET_MOORE['nasales'] + 
    ALPHABET_MOORE['speciaux']
)

# Charger le fichier Excel contenant les traductions Moore - Français

# Chemins corrigés
file_path = r"C:/Users/HP/Documents/ArticleRBaZIE/Data1.xlsx"
backup_path = r"C:/Users/HP/Documents/ArticleRBaZIE/Data1_backup.xlsx"
new_words_path = r"C:/Users/HP/Documents/ArticleRBaZIE/nouveaux_mots.xlsx"

# Charger les données initiales
try:
    df = pd.read_excel(file_path)
    # Créer une sauvegarde
    df.to_excel(backup_path, index=False)
except Exception as e:
    messagebox.showerror("Erreur", f"Impossible de charger le fichier: {e}")
    exit()

# Supprimer la colonne 'Unnamed: 0' si elle existe
df = df.drop(columns=['Unnamed: 0'], errors='ignore')

# Renommer les colonnes pour éviter les problèmes de casse
df.columns = ['Moore', 'Français']

# Vérifier si le fichier pour nouveaux mots existe, sinon le créer
if not os.path.exists(new_words_path):
    new_words_df = pd.DataFrame(columns=['Moore', 'Français', 'Date_Ajout', 'Source'])
    new_words_df.to_excel(new_words_path, index=False)
else:
    new_words_df = pd.read_excel(new_words_path)

# Fonction pour sauvegarder les nouvelles entrées
def sauvegarder_nouveau_mot(moore, francais, source="Utilisateur"):
    global new_words_df
    
    # Ajouter à DataFrame temporaire
    nouvelle_ligne = {
        'Moore': moore,
        'Français': francais,
        'Date_Ajout': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Source': source
    }
    
    new_words_df = pd.concat([new_words_df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    
    # Sauvegarder dans le fichier
    new_words_df.to_excel(new_words_path, index=False)
    
    # Mettre à jour le DataFrame principal pour la session en cours
    global df
    df = pd.concat([df, pd.DataFrame([{'Moore': moore, 'Français': francais}])], ignore_index=True)
    
    # Optionnel: sauvegarder aussi dans le fichier principal
    # df.to_excel(file_path, index=False)

# Fonction pour proposer d'ajouter un mot manquant
def proposer_ajout_mot(mot_original, direction):
    reponse = messagebox.askyesno(
        "Mot non trouvé", 
        f"Le mot '{mot_original}' n'a pas été trouvé dans la base de données.\n"
        f"Souhaitez-vous l'ajouter ?"
    )
    
    if reponse:
        if direction == "Moore vers Français":
            # Demander la traduction en Français
            traduction = simpledialog.askstring(
                "Ajouter une traduction",
                f"Veuillez entrer la traduction en Français pour '{mot_original}':"
            )
            if traduction and traduction.strip():
                sauvegarder_nouveau_mot(mot_original, traduction.strip())
                return f"Le mot '{mot_original}' a été ajouté avec la traduction: {traduction}"
            else:
                return "Ajout annulé."
                
        elif direction == "Français vers Moore":
            # Demander la traduction en Moore
            traduction = simpledialog.askstring(
                "Ajouter une traduction",
                f"Veuillez entrer la traduction en Moore pour '{mot_original}':"
            )
            if traduction and traduction.strip():
                sauvegarder_nouveau_mot(traduction.strip(), mot_original)
                return f"Le mot '{mot_original}' a été ajouté avec la traduction: {traduction}"
            else:
                return "Ajout annulé."
    
    return None

# Fonction de traduction Moore -> Français
def traduire_moore_vers_francais(mot_ou_phrase):
    mot_ou_phrase_lower = mot_ou_phrase.lower()
    
    # Recherche exacte d'abord
    resultats_exacts = df[df['Moore'].str.lower() == mot_ou_phrase_lower]
    if not resultats_exacts.empty:
        traduction = resultats_exacts.iloc[0]['Français']
        return f"Traduction (Français): {traduction}"
    
    # Recherche partielle
    resultats_partiels = df[df['Moore'].str.contains(mot_ou_phrase, case=False, na=False)]
    if not resultats_partiels.empty:
        traduction = resultats_partiels.iloc[0]['Français']
        return f"Traduction (Français): {traduction}"
    
    # Mot non trouvé, proposer d'ajouter
    ajout_resultat = proposer_ajout_mot(mot_ou_phrase, "Moore vers Français")
    if ajout_resultat:
        return ajout_resultat
    
    return "Désolé, aucune traduction trouvée pour ce mot/phrase."

# Fonction de traduction Français -> Moore
def traduire_francais_vers_moore(mot_ou_phrase):
    mot_ou_phrase_lower = mot_ou_phrase.lower()
    
    # Recherche exacte d'abord
    resultats_exacts = df[df['Français'].str.lower() == mot_ou_phrase_lower]
    if not resultats_exacts.empty:
        traduction = resultats_exacts.iloc[0]['Moore']
        return f"Traduction (Moore): {traduction}"
    
    # Recherche partielle
    resultats_partiels = df[df['Français'].str.contains(mot_ou_phrase, case=False, na=False)]
    if not resultats_partiels.empty:
        traduction = resultats_partiels.iloc[0]['Moore']
        return f"Traduction (Moore): {traduction}"
    
    # Mot non trouvé, proposer d'ajouter
    ajout_resultat = proposer_ajout_mot(mot_ou_phrase, "Français vers Moore")
    if ajout_resultat:
        return ajout_resultat
    
    return "Désolé, aucune traduction trouvée pour ce mot/phrase."

# Fonction pour afficher les mots ajoutés récemment
def afficher_nouveaux_mots():
    try:
        mots_recent_df = pd.read_excel(new_words_path)
        if mots_recent_df.empty:
            messagebox.showinfo("Mots ajoutés", "Aucun nouveau mot n'a été ajouté.")
            return
        
        # Créer une nouvelle fenêtre pour afficher les mots
        fenetre_mots = tk.Toplevel(fenetre)
        fenetre_mots.title("Mots ajoutés récemment")
        fenetre_mots.geometry("600x400")
        
        # Créer un cadre avec scrollbar
        cadre = tk.Frame(fenetre_mots)
        cadre.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(cadre)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Liste des mots
        liste_mots = tk.Listbox(cadre, yscrollcommand=scrollbar.set, font=("Arial", 11))
        
        # Ajouter les mots à la liste
        for index, row in mots_recent_df.iterrows():
            liste_mots.insert(tk.END, f"{row['Moore']} = {row['Français']} (Ajouté le: {row['Date_Ajout']})")
        
        liste_mots.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=liste_mots.yview)
        
        # Bouton pour fermer
        btn_fermer = tk.Button(fenetre_mots, text="Fermer", command=fenetre_mots.destroy)
        btn_fermer.pack(pady=5)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire les mots ajoutés: {e}")

# Fonction pour insérer un caractère Mooré dans le champ de saisie
def inserer_caractere_moore(caractere):
    entry.insert(tk.INSERT, caractere)
    entry.focus_set()

# Fonction pour afficher le clavier Mooré
def afficher_clavier_moore():
    # Créer une nouvelle fenêtre pour le clavier
    fenetre_clavier = tk.Toplevel(fenetre)
    fenetre_clavier.title("Clavier Mooré - Insérez des caractères spéciaux")
    fenetre_clavier.geometry("650x400")
    
    # Onglets pour différentes catégories de caractères
    notebook = ttk.Notebook(fenetre_clavier)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Fonction pour créer un cadre avec des boutons
    def creer_cadre_caracteres(parent, caracteres, titre, colonnes=8):
        frame = ttk.Frame(parent)
        
        # Titre
        ttk.Label(frame, text=titre, font=("Arial", 10, "bold")).pack(pady=(5, 10))
        
        # Cadre pour les boutons
        boutons_frame = ttk.Frame(frame)
        boutons_frame.pack()
        
        row, col = 0, 0
        for i, caractere in enumerate(caracteres):
            if col >= colonnes:
                col = 0
                row += 1
            
            btn = tk.Button(boutons_frame, text=caractere, font=("Arial", 14, "bold"),
                           width=4, height=2, bg="#e0e0e0",
                           command=lambda c=caractere: inserer_caractere_moore(c))
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
        
        return frame
    
    # Onglet 1: Lettres basiques
    tab1 = creer_cadre_caracteres(notebook, ALPHABET_MOORE['basiques'], 
                                   "Lettres Basiques (communes avec le Français)", 10)
    notebook.add(tab1, text="Lettres Basiques")
    
    # Onglet 2: Voyelles avec accents
    tab2 = creer_cadre_caracteres(notebook, ALPHABET_MOORE['voyelles_avec_accents'], 
                                   "Voyelles avec Accents", 5)
    notebook.add(tab2, text="Voyelles Accentuées")
    
    # Onglet 3: Voyelles longues
    tab3 = creer_cadre_caracteres(notebook, ALPHABET_MOORE['voyelles_longues'], 
                                   "Voyelles Longues", 5)
    notebook.add(tab3, text="Voyelles Longues")
    
    # Onglet 4: Nasales et spéciales
    tab4 = creer_cadre_caracteres(notebook, ALPHABET_MOORE['nasales'] + ALPHABET_MOORE['speciaux'], 
                                   "Consonnes Nasales et Caractères Spéciaux", 5)
    notebook.add(tab4, text="Nasales & Spéciaux")
    
    # Onglet 5: Tous les caractères
    tab5 = creer_cadre_caracteres(notebook, ALL_MOORE_LETTERS, 
                                   "Tous les Caractères Mooré", 8)
    notebook.add(tab5, text="Tous les Caractères")
    
    # Bouton de fermeture
    btn_fermer = tk.Button(fenetre_clavier, text="Fermer le Clavier", 
                          command=fenetre_clavier.destroy, font=("Arial", 10))
    btn_fermer.pack(pady=5)

# Fonction pour afficher un aide-mémoire des caractères Mooré
def afficher_aide_memoire():
    fenetre_aide = tk.Toplevel(fenetre)
    fenetre_aide.title("Aide-mémoire - Alphabet Mooré")
    fenetre_aide.geometry("500x400")
    
    text_widget = tk.Text(fenetre_aide, wrap=tk.WORD, font=("Arial", 10), padx=10, pady=10)
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    aide_text = """ALPHABET MOORÉ - AIDE-MÉMOIRE

Lettres Basiques (communes avec le Français):
a b d e f g h i k l m n o p r s t u v w y z

Voyelles avec Accents:
ɛ - epsilon (e ouvert)
ɔ - o ouvert
ã - a nasal
ẽ - e nasal
ĩ - i nasal
õ - o nasal
ũ - u nasal
ɛ̃ - epsilon nasal
ɔ̃ - o ouvert nasal

Voyelles Longues (avec macron):
ā - a long
ē - e long
ī - i long
ō - o long
ū - u long
ɛ̄ - epsilon long
ɔ̄ - o ouvert long

Consonnes Nasales:
ŋ - eng (n vélaire)
ɲ - n palatal
ɱ - m labio-dental

Caractères Spéciaux:
ʼ - coup de glotte
ʋ - v labio-dental
ɣ - gamma (g spirant)
ɓ - b implosif
ɗ - d implosif
ƴ - y implosif
ʔ - coup de glotte (autre forme)

CONSEILS D'UTILISATION:
1. Utilisez le clavier virtuel pour insérer les caractères spéciaux
2. Pour les mots français, utilisez les lettres basiques
3. Les voyelles nasales sont fréquentes en Mooré
4. Les caractères spéciaux modifient souvent la prononciation"""
    
    text_widget.insert(tk.END, aide_text)
    text_widget.config(state=tk.DISABLED)
    
    btn_fermer = tk.Button(fenetre_aide, text="Fermer", command=fenetre_aide.destroy)
    btn_fermer.pack(pady=5)

# Fonction pour effacer le champ de saisie
def effacer_saisie():
    entry.delete(0, tk.END)
    entry.focus_set()

# Fonction appelée lorsque l'utilisateur clique sur le bouton "Traduire"
def traduire():
    mot_ou_phrase = entry.get().strip()
    
    if not mot_ou_phrase:
        messagebox.showerror("Erreur", "Veuillez entrer un mot ou une phrase.")
        return
    
    if choix_var.get() == "Moore vers Français":
        resultat = traduire_moore_vers_francais(mot_ou_phrase)
    elif choix_var.get() == "Français vers Moore":
        resultat = traduire_francais_vers_moore(mot_ou_phrase)
    else:
        messagebox.showerror("Erreur", "Veuillez choisir un type de traduction.")
        return

    label_resultat.config(text=resultat)
    # Effacer le champ de saisie après traduction
    entry.delete(0, tk.END)

# Création de la fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Application de Traduction Moore <-> Français")
fenetre.geometry("700x600")

# Titre
label_titre = tk.Label(fenetre, text="Traduction Moore <-> Français", 
                       font=("Arial", 16, "bold"))
label_titre.pack(pady=10)

# Choisir le type de traduction
choix_var = tk.StringVar(value="Moore vers Français")  # Valeur par défaut

label_type_traduction = tk.Label(fenetre, text="Choisissez le type de traduction:", 
                                 font=("Arial", 12))
label_type_traduction.pack(pady=5)

# Cadre pour les boutons radio
cadre_radio = tk.Frame(fenetre)
cadre_radio.pack(pady=5)

# Boutons radio pour choisir la direction de traduction
radio_moore_francais = tk.Radiobutton(cadre_radio, text="Moore → Français", 
                                       variable=choix_var, 
                                       value="Moore vers Français", font=("Arial", 12))
radio_francais_moore = tk.Radiobutton(cadre_radio, text="Français → Moore", 
                                       variable=choix_var, 
                                       value="Français vers Moore", font=("Arial", 12))
radio_moore_francais.pack(side=tk.LEFT, padx=20)
radio_francais_moore.pack(side=tk.LEFT, padx=20)

# Cadre pour la saisie avec boutons d'accès rapide
cadre_saisie = tk.Frame(fenetre)
cadre_saisie.pack(pady=15)

# Étiquette et champ de saisie
entry_label = tk.Label(cadre_saisie, text="Entrez un mot ou une phrase :", 
                       font=("Arial", 12))
entry_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))

# Champ de saisie principal
entry = tk.Entry(cadre_saisie, font=("Arial", 14), width=40)
entry.grid(row=1, column=0, columnspan=3, pady=5)

# Boutons d'accès rapide pour caractères Mooré fréquents
cadre_rapide = tk.Frame(cadre_saisie)
cadre_rapide.grid(row=2, column=0, columnspan=3, pady=5)

# Caractères Mooré fréquents pour accès rapide
caracteres_frequents = ['ɛ', 'ɔ', 'ŋ', 'ã', 'ẽ', 'ĩ', 'ō', 'ū', 'ʼ']

for i, caractere in enumerate(caracteres_frequents):
    btn = tk.Button(cadre_rapide, text=caractere, font=("Arial", 10, "bold"),
                   width=3, height=1, bg="#d0e0ff",
                   command=lambda c=caractere: inserer_caractere_moore(c))
    btn.grid(row=0, column=i, padx=2)

# Boutons d'action
cadre_actions = tk.Frame(fenetre)
cadre_actions.pack(pady=10)

# Bouton pour le clavier Mooré
btn_clavier = tk.Button(cadre_actions, text="⌨️ Clavier Mooré", 
                       font=("Arial", 11), bg="#4CAF50", fg="white",
                       padx=15, command=afficher_clavier_moore)
btn_clavier.pack(side=tk.LEFT, padx=5)

# Bouton pour effacer
btn_effacer = tk.Button(cadre_actions, text="✖️ Effacer", 
                       font=("Arial", 11), bg="#f44336", fg="white",
                       padx=15, command=effacer_saisie)
btn_effacer.pack(side=tk.LEFT, padx=5)

# Bouton pour l'aide-mémoire
btn_aide = tk.Button(cadre_actions, text="❓ Aide Alphabet", 
                    font=("Arial", 11), bg="#2196F3", fg="white",
                    padx=15, command=afficher_aide_memoire)
btn_aide.pack(side=tk.LEFT, padx=5)

# Bouton principal de traduction
btn_traduire = tk.Button(fenetre, text="🔍 Traduire", font=("Arial", 14, "bold"), 
                         bg="#FF9800", fg="white", padx=25, pady=5, command=traduire)
btn_traduire.pack(pady=15)

# Label pour afficher le résultat de la traduction
label_resultat = tk.Label(fenetre, text="", font=("Arial", 14), 
                          wraplength=650, justify="left", bg="#f9f9f9",
                          relief=tk.SUNKEN, padx=10, pady=10, width=50, height=4)
label_resultat.pack(pady=10)

# Cadre pour les boutons supplémentaires
cadre_bas = tk.Frame(fenetre)
cadre_bas.pack(pady=10)

# Bouton pour voir les mots ajoutés
btn_voir_mots = tk.Button(cadre_bas, text="📚 Voir les mots ajoutés", 
                         font=("Arial", 11), bg="#9C27B0", fg="white",
                         padx=15, command=afficher_nouveaux_mots)
btn_voir_mots.pack(side=tk.LEFT, padx=5)

# Informations sur les fonctionnalités
label_info = tk.Label(fenetre, 
                      text="Fonctionnalités:\n"
                      "• Traduction dans les deux sens\n"
                      "• Clavier Mooré intégré avec caractères spéciaux\n"
                      "• Ajout automatique des mots manquants\n"
                      "• Stockage des nouveaux mots",
                      font=("Arial", 10), justify="left", bg="#e8f4f8",
                      relief=tk.RIDGE, padx=10, pady=5)
label_info.pack(pady=10, padx=20, fill=tk.X)

# Statistiques
label_stats = tk.Label(fenetre, 
                       text=f"Base de données: {len(df)} mots | Nouveaux mots: {len(new_words_df)} | Caractères Mooré: {len(ALL_MOORE_LETTERS)}",
                       font=("Arial", 9), bg="#f0f0f0")
label_stats.pack(pady=5)

# Lancer l'application Tkinter
fenetre.mainloop()