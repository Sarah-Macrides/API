import sys
import requests
import csv

# Fonction pour extraire les références d'un gène pour une espèce donnée
def extract_references(species, gene):
  # URL de l'API Ensembl pour obtenir les références en fonction des symboles
  url = f"https://rest.ensembl.org/xrefs/symbol/{species}/{gene}?content-type=application/json"
  r = requests.get(url)
  if not r.ok:
    r.raise_for_status()
    sys.exit()

  decoded = r.json()
  return decoded

# Extraction les informations d'un gène pour une espèce donnée
def extract_info(species, gene):
  references = extract_references(species, gene)
  
  gene_symbol = gene
  gene_id = references[0]['id'] if references else "N/A" 
  genome_browser = f"https://www.ensembl.org/{species}/Gene/Summary?g={gene_id}"
  rna_access_number = references[0]['id'] if references else "N/A"
  protein_access_number = references[0]['id'] if references else "N/A"
  
  # Dico avec les informations
  return {
    "species": species,
    "gene_symbol": gene_symbol,
    "gene_id": gene_id,
    "genome_browser": genome_browser,
    "rna_access_number": rna_access_number,
    "protein_access_number": protein_access_number
  }

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

# Exécution et création du fichier résultats
def main():
    # Lire le fichier GenSymbol_45.txt
    gene_file = "GeneSymbols_45.txt"
    gene_dict = read_gene_file(gene_file)

    output_file = "results_ensembl.csv"
    fieldnames = ["species", "gene_symbol", "gene_id", "genome_browser", "rna_access_number", "protein_access_number"]
  
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for species, gene in gene_dict.items():
            if species.lower() == "escherichia_coli":
                species_id = "escherichia_coli_gca_005395625"
            else:
                species_id = species

            try:
                info = extract_info(species_id, gene)
                if info["gene_id"] != "N/A":  # Vérifier si les données sont valides
                    writer.writerow(info)
                    print(f"Données enregistrées pour {gene} ({species})")
                else:
                    print(f"Aucune donnée trouvée pour {gene} ({species})")
            except Exception as e:
                print(f"Erreur lors de la récupération des données pour {gene} ({species}): {e}")

if __name__ == "__main__":
    main()
