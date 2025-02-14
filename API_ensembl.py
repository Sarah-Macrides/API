import sys
import requests
import csv

# Dictionnaire des espèces et leurs gènes
dico_especes = {
  'homo_sapiens': 'RAD51',
  'arabidopsis_thaliana': 'PHYB',
  'saccharomyces_cerevisiae': 'SFA1',
  'leishmania_major': 'ACP',
  'escherichia_coli_gca_005395625': 'HYBE'
}

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

# Exécution et création du fichier résultats
def run_ensembl():
  output_file = "results_ensembl.csv"
  fieldnames = ["species", "gene_symbol", "gene_id", "genome_browser", "rna_access_number", "protein_access_number"]
  
  with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for gene, species in dico_especes.items():
      info = extract_info(gene, species)
      if info:
        writer.writerow(info)
        print(f"Données enregistrées pour {gene} ({species})")
      else:
        print(f"Aucune donnée enregistrée pour {gene} ({species})")