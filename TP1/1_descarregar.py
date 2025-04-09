import os
from sickle import Sickle

# Descarregar os registos OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting)
url = "https://www.arquivoalbertosampaio.org/OAI-PMH/"

sickle = Sickle(url) # obj sickle do url
records = sickle.ListRecords(metadataPrefix='oai_dc') # padrão simples e comum

def save_records(directory_name="records"): 
    os.makedirs(directory_name, exist_ok=True)
       
    for i, record in enumerate(records):
        with open(f"records/record_{i}.xml", "w", encoding="utf-8") as f:
            f.write(str(record.raw))
        if i > 100:  # limite de 100 + 1
            break

if __name__ == "__main__":
    save_records()
    print("Registos descarregados com sucesso.")

