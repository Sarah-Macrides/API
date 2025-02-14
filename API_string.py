import requests
import json
import csv
import re

def get_string_interactions(gene, species):
    # URL de base de l'API de STRING
    base_url = "https://string-db.org/api"
    output_format = "json"  # Format de sortie (json, xml, tsv, etc.)
    method = "network"  # Méthode de l'API (network, enrichment, etc.)

    # Paramètres de la requête
    params = {
        "identifiers": gene,  # Identifiant du gène
        "species": species,  # Identifiant de l'espèce (taxon ID)
        "caller_identity": "your_app_name"  # Nom de votre application
    }

    # Construire l'URL complète
    url = f"{base_url}/{output_format}/{method}"

    # Envoyer la requête GET à l'API de STRING
    response = requests.get(url, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Convertir la réponse en JSON
        interactions = response.json()
        # Filtrer pour obtenir uniquement l'identifiant principal du gène
        if interactions:
            primary_interaction = interactions[0]
            if re.match(r'^\d+\.[a-zA-Z0-9]+$', primary_interaction['stringId_A']):
                return primary_interaction['stringId_A']
    else:
        print(f"Erreur lors de l'appel à l'API de STRING: {response.status_code}")
        return None

def read_gene_file(file_path):
    gene_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                gene, species = parts
                gene_dict[species] = gene
            else:
                print(f"Ligne ignorée (format incorrect) : {line.strip()}")
    return gene_dict

def main():
    # Lire le fichier GenSymbol_45.txt
    gene_file = "GeneSymbols_45.txt"
    gene_dict = read_gene_file(gene_file)

    # Fichier de sortie CSV
    output_file = "string_interactions.csv"
    fieldnames = ["species", "gene_symbol", "interaction_link"]

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for species, gene in gene_dict.items():
            # Gérer le cas particulier d'Escherichia coli
            if species.lower() == "escherichia_coli":
                species_id = 511145
            else:
                species_id = species

            # Appeler l'API de STRING pour chaque gène et espèce
            string_id = get_string_interactions(gene, species_id)
            if string_id:
                interaction_link = f"https://string-db.org/network/{string_id}"
                writer.writerow({
                    "species": species,
                    "gene_symbol": gene,
                    "interaction_link": interaction_link
                })
                print(f"Interaction enregistrée pour {gene} ({species})")
            else:
                print(f"Aucune interaction trouvée pour {gene} ({species})")

    print(f"Fichier {output_file} généré avec succès !")

if __name__ == "__main__":
    main()