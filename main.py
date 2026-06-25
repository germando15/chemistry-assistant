#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 Chimie Pro - PoC Console
Recherche d'éléments · Masse molaire · Moles · Export rapport format txt
"""

import json
import re
from datetime import datetime
from typing import Optional, List, Dict, Tuple

# ============================================================
# BASE DE DONNÉES DES ÉLÉMENTS
# ============================================================
ELEMENTS = [
    {"numero": 1, "nom": "Hydrogène", "symbole": "H", "masse": 1.008},
    {"numero": 2, "nom": "Hélium", "symbole": "He", "masse": 4.0026},
    {"numero": 3, "nom": "Lithium", "symbole": "Li", "masse": 6.94},
    {"numero": 4, "nom": "Béryllium", "symbole": "Be", "masse": 9.0122},
    {"numero": 5, "nom": "Bore", "symbole": "B", "masse": 10.81},
    {"numero": 6, "nom": "Carbone", "symbole": "C", "masse": 12.011},
    {"numero": 7, "nom": "Azote", "symbole": "N", "masse": 14.007},
    {"numero": 8, "nom": "Oxygène", "symbole": "O", "masse": 15.999},
    {"numero": 9, "nom": "Fluor", "symbole": "F", "masse": 18.998},
    {"numero": 10, "nom": "Néon", "symbole": "Ne", "masse": 20.180},
    {"numero": 11, "nom": "Sodium", "symbole": "Na", "masse": 22.990},
    {"numero": 12, "nom": "Magnésium", "symbole": "Mg", "masse": 24.305},
    {"numero": 13, "nom": "Aluminium", "symbole": "Al", "masse": 26.982},
    {"numero": 14, "nom": "Silicium", "symbole": "Si", "masse": 28.085},
    {"numero": 15, "nom": "Phosphore", "symbole": "P", "masse": 30.974},
    {"numero": 16, "nom": "Soufre", "symbole": "S", "masse": 32.065},
    {"numero": 17, "nom": "Chlore", "symbole": "Cl", "masse": 35.45},
    {"numero": 18, "nom": "Argon", "symbole": "Ar", "masse": 39.948},
    {"numero": 19, "nom": "Potassium", "symbole": "K", "masse": 39.098},
    {"numero": 20, "nom": "Calcium", "symbole": "Ca", "masse": 40.078},
    {"numero": 26, "nom": "Fer", "symbole": "Fe", "masse": 55.845},
    {"numero": 29, "nom": "Cuivre", "symbole": "Cu", "masse": 63.546},
    {"numero": 30, "nom": "Zinc", "symbole": "Zn", "masse": 65.38},
    {"numero": 47, "nom": "Argent", "symbole": "Ag", "masse": 107.87},
    {"numero": 79, "nom": "Or", "symbole": "Au", "masse": 196.97},
    {"numero": 82, "nom": "Plomb", "symbole": "Pb", "masse": 207.2}
]

# Index pour recherche rapide
ELEMENTS_INDEX = {}
for el in ELEMENTS:
    ELEMENTS_INDEX[el["symbole"]] = el
    ELEMENTS_INDEX[el["nom"].lower()] = el
    ELEMENTS_INDEX[str(el["numero"])] = el


# ============================================================
# 1. RECHERCHE D'ÉLÉMENT
# ============================================================
def rechercher_element(query: str) -> Optional[Dict]:
    """
    Recherche un élément par nom, symbole ou numéro atomique.
    """
    if not query or query.strip() == "":
        return None
    
    q = query.strip().lower()
    
    # Recherche exacte
    if q in ELEMENTS_INDEX:
        return ELEMENTS_INDEX[q]
    
    # Recherche partielle dans les noms
    for el in ELEMENTS:
        if q in el["nom"].lower() or q in el["symbole"].lower():
            return el
    
    return None


def afficher_element(el: Dict) -> None:
    """Affiche les informations d'un élément."""
    if not el:
        print("❌ Aucun élément trouvé.")
        return
    print(f"\n🔬 Élément trouvé :")
    print(f"   📌 Numéro : {el['numero']}")
    print(f"   📝 Nom    : {el['nom']}")
    print(f"   🔤 Symbole: {el['symbole']}")
    print(f"   ⚖️ Masse  : {el['masse']} g/mol")


# ============================================================
# 2. CALCUL DE LA MASSE MOLAIRE
# ============================================================
def parser_formule(formule: str) -> Optional[List[Tuple[str, int]]]:
    """
    Parse une formule chimique en tokens (symbole, nombre).
    Ex: H2O -> [('H', 2), ('O', 1)]
    """
    formule = formule.replace(" ", "")
    if not formule:
        return None
    
    # Pattern: lettre majuscule + minuscule optionnelle + chiffres optionnels
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formule)
    
    if not matches:
        return None
    
    tokens = []
    for symbole, count_str in matches:
        count = int(count_str) if count_str else 1
        # Vérifie si le symbole existe
        if symbole not in [el["symbole"] for el in ELEMENTS]:
            return None
        tokens.append((symbole, count))
    
    return tokens


def calculer_masse_molaire(formule: str) -> Optional[float]:
    """
    Calcule la masse molaire d'une formule chimique.
    """
    tokens = parser_formule(formule)
    if not tokens:
        return None
    
    total = 0.0
    for symbole, count in tokens:
        # Récupère l'élément
        el = next((e for e in ELEMENTS if e["symbole"] == symbole), None)
        if not el:
            return None
        total += el["masse"] * count
    
    return total


def afficher_masse_molaire(formule: str, masse: Optional[float]) -> None:
    """Affiche le résultat du calcul de masse molaire."""
    if masse is None:
        print(f"❌ Formule '{formule}' invalide ou élément inconnu.")
        return
    print(f"\n⚖️ Masse molaire de {formule} :")
    print(f"   {masse:.3f} g/mol")


# ============================================================
# 3. CALCUL DU NOMBRE DE MOLES
# ============================================================
def calculer_moles(masse: float, masse_molaire: float) -> Optional[float]:
    """
    Calcule le nombre de moles : n = m / M
    """
    if masse_molaire == 0:
        return None
    return masse / masse_molaire


def afficher_moles(m: float, M: float, n: Optional[float]) -> None:
    """Affiche le résultat du calcul de moles."""
    if n is None:
        print("❌ La masse molaire ne peut pas être nulle.")
        return
    print(f"\n🧪 Calcul du nombre de moles :")
    print(f"   n = {m} / {M}")
    print(f"   n = {n:.6f} mol")


# ============================================================
# 4. EXPORT PDF (sans bibliothèque externe)
# ============================================================
def exporter_pdf_simple(nom_fichier: str = "rapport_chimie.txt") -> None:
    """
    Exporte un rapport chimique au format texte (simule un PDF).
    Pour un vrai PDF, il faudrait installer reportlab ou fpdf.
    """
    # Récupère les données actuelles
    # (dans un vrai script, on passerait les données en paramètres)
    
    rapport = []
    rapport.append("=" * 60)
    rapport.append("                 RAPPORT CHIMIQUE")
    rapport.append("=" * 60)
    rapport.append(f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    rapport.append("")
    
    # Section 1 : Élément
    rapport.append("🔍 RECHERCHE D'ÉLÉMENT")
    rapport.append("-" * 40)
    # Exemple : on peut chercher un élément
    rapport.append("Exemple : Oxygène (O) - 15.999 g/mol")
    rapport.append("")
    
    # Section 2 : Masse molaire
    rapport.append("⚖️ MASSE MOLAIRE")
    rapport.append("-" * 40)
    rapport.append("Exemple : H2O → 18.015 g/mol")
    rapport.append("")
    
    # Section 3 : Moles
    rapport.append("🧪 NOMBRE DE MOLES")
    rapport.append("-" * 40)
    rapport.append("Formule : n = m / M")
    rapport.append("Exemple : 36 g / 18.015 g/mol = 1.998 mol")
    rapport.append("")
    
    # Section 4 : Tableau des éléments
    rapport.append("📊 TABLEAU DES ÉLÉMENTS (extrait)")
    rapport.append("-" * 40)
    rapport.append(f"{'#':<4} {'Symbole':<8} {'Nom':<15} {'Masse (g/mol)':<12}")
    rapport.append("-" * 40)
    for el in ELEMENTS[:15]:
        rapport.append(f"{el['numero']:<4} {el['symbole']:<8} {el['nom']:<15} {el['masse']:<12.3f}")
    rapport.append("")
    
    rapport.append("=" * 60)
    rapport.append("Fin du rapport - Généré par Chimie Pro")
    rapport.append("=" * 60)
    
    # Écriture dans un fichier
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        f.write("\n".join(rapport))
    
    print(f"\n📄 Rapport exporté dans : {nom_fichier}")
    print(f"   (Format texte - pour un vrai PDF, installez reportlab ou fpdf)")


# ============================================================
# 5. MENU PRINCIPAL (INTERACTIF)
# ============================================================
def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 60)
    print("         🔬 CHIMIE PRO - PoC Console")
    print("=" * 60)
    print("1. 🔍 Rechercher un élément")
    print("2. ⚖️  Calculer la masse molaire")
    print("3. 🧪 Calculer le nombre de moles")
    print("4. 📄 Exporter un rapport (texte)")
    print("5. 📊 Afficher le tableau des éléments")
    print("0. 🚪 Quitter")
    print("-" * 60)


def menu_rechercher_element():
    """Menu de recherche d'élément."""
    print("\n🔍 RECHERCHE D'ÉLÉMENT")
    print("-" * 40)
    query = input("Entrez un nom, symbole ou numéro atomique : ").strip()
    if query:
        el = rechercher_element(query)
        afficher_element(el)
    else:
        print("❌ Entrée vide.")


def menu_masse_molaire():
    """Menu de calcul de masse molaire."""
    print("\n⚖️  CALCUL DE LA MASSE MOLAIRE")
    print("-" * 40)
    formule = input("Entrez une formule chimique (ex: H2O, NaCl) : ").strip()
    if formule:
        masse = calculer_masse_molaire(formule)
        afficher_masse_molaire(formule, masse)
    else:
        print("❌ Entrée vide.")


def menu_moles():
    """Menu de calcul du nombre de moles."""
    print("\n🧪 CALCUL DU NOMBRE DE MOLES")
    print("-" * 40)
    print("Formule : n = m / M")
    
    try:
        m = float(input("Entrez la masse (m) en grammes : ").strip())
        M = float(input("Entrez la masse molaire (M) en g/mol : ").strip())
        n = calculer_moles(m, M)
        afficher_moles(m, M, n)
    except ValueError:
        print("❌ Veuillez entrer des nombres valides.")


def menu_tableau():
    """Affiche le tableau des éléments."""
    print("\n📊 TABLEAU DES ÉLÉMENTS")
    print("-" * 60)
    print(f"{'#':<4} {'Symbole':<8} {'Nom':<20} {'Masse (g/mol)':<12}")
    print("-" * 60)
    for el in ELEMENTS:
        print(f"{el['numero']:<4} {el['symbole']:<8} {el['nom']:<20} {el['masse']:<12.3f}")
    print("-" * 60)
    print(f"Total : {len(ELEMENTS)} éléments")


def menu_export():
    """Menu d'export du rapport."""
    print("\n📄 EXPORT DU RAPPORT")
    print("-" * 40)
    print("Options :")
    print("1. Rapport simple (texte)")
    print("2. Rapport avec tous les éléments")
    choix = input("Votre choix (1/2) : ").strip()
    
    if choix == "1":
        exporter_pdf_simple("rapport_simple.txt")
    elif choix == "2":
        exporter_pdf_simple("rapport_complet.txt")
    else:
        print("❌ Choix invalide.")


# ============================================================
# 6. EXÉCUTION PRINCIPALE
# ============================================================
def main():
    """Fonction principale."""
    print("\n🔬 Bienvenue dans Chimie Pro - PoC Console")
    print(f"   {len(ELEMENTS)} éléments chimiques disponibles")
    
    while True:
        afficher_menu()
        choix = input("\nVotre choix : ").strip()
        
        if choix == "0":
            print("\n👋 Au revoir !")
            break
        elif choix == "1":
            menu_rechercher_element()
        elif choix == "2":
            menu_masse_molaire()
        elif choix == "3":
            menu_moles()
        elif choix == "4":
            menu_export()
        elif choix == "5":
            menu_tableau()
        else:
            print("❌ Choix invalide. Veuillez réessayer.")
        
        input("\nAppuyez sur Entrée pour continuer...")


# ============================================================
# 7. TESTS UNITAIRES (optionnels)
# ============================================================
def test_unitaire():
    """Exécute une série de tests pour valider les fonctions."""
    print("\n🧪 Exécution des tests unitaires...")
    
    # Test recherche
    assert rechercher_element("H")["nom"] == "Hydrogène"
    assert rechercher_element("Oxygène")["symbole"] == "O"
    assert rechercher_element("8")["nom"] == "Oxygène"
    assert rechercher_element("X") is None
    
    # Test masse molaire
    assert abs(calculer_masse_molaire("H2O") - 18.015) < 0.001
    assert abs(calculer_masse_molaire("NaCl") - 58.44) < 0.01
    assert abs(calculer_masse_molaire("C6H12O6") - 180.156) < 0.01
    assert calculer_masse_molaire("X2") is None
    
    # Test moles
    assert abs(calculer_moles(36, 18.015) - 1.998) < 0.01
    
    print("✅ Tous les tests sont passés !")


# ============================================================
# 8. POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    # Décommentez pour exécuter les tests
    # test_unitaire()
    
    # Lance le programme principal
    main()