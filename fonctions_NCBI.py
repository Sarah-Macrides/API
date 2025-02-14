from Bio import Entrez

def get_ncbi_gene_id(species_name, gene_name, email="sarah.m76@outlook.fr"):
    
    """
    Recherche l'identifiant NCBI d'un gène donné pour une espèce spécifique.
    """
    
    Entrez.email = email  # Configuration de l'email

    try:
        # Requête à NCBI Gene pour récupérer l'ID du gène correspondant
        query = f"{gene_name}[Gene Name] AND {species_name}[Organism]"
        handle = Entrez.esearch(db="gene", term=query)
        record = Entrez.read(handle)
        handle.close()
        

        # Vérification si des résultats ont été trouvés
        if record["IdList"]:
            return record["IdList"][0]# Renvoie le premier ID trouvé
        else:
            return f"Aucun identifiant trouvé pour {gene_name} chez {species_name}."

    except Exception as e:
        return f"Erreur lors de la requête NCBI : {e}"


def id_intern(gene_id, db, linkname) : 
    
    """
    Pour un gene_id, interroge la base 'db' via elink avec le lien 'linkname'
    pour obtenir la liste d'IDs internes puis renvoie la liste d'accessions
    
    """
    id_list = []
    
    query= Entrez.elink(dbfrom = "gene", db = db, linkname = linkname, id = gene_id)
    links = Entrez.read(query)
    
    if "LinkSetDb" in links[0]:
        for linkset in links[0]["LinkSetDb"]:
            if linkset["LinkName"] == linkname:
                id_list = [link["Id"] for link in linkset["Link"]]
    else : 
        id_list=["none"]
        
    return id_list

def get_refseq_accessions(id_list, db ):
    """
    Pour une liste d'IDs internes dans la base 'db' (nuccore ou protein),
    interroge esummary pour récupérer le champ 'AccessionVersion'
    Retourne une liste d'accessions.
    """
    if not id_list:
        liste = ["No data found"]
        return liste
    try:
        with Entrez.esummary(db=db, id=",".join(id_list), retmode="xml") as handle:
            records = Entrez.read(handle)
    except Exception as e:
        print(f"Erreur esummary dans {db}: {e}")
        return []
    
    return [record.get("AccessionVersion", "") for record in records]