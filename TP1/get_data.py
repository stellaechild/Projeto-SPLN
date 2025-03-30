import yaml
from sickle import Sickle

# OAI-PMH endpoint: Famalicão (Alberto Sampaio)
endpoint = "https://www.arquivoalbertosampaio.org/OAI-PMH/"
sickle = Sickle(endpoint)

dados = {"Registos": []}

def save_to_file():
    with open("dados_brutos.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dados, f, allow_unicode=True, default_flow_style=False)
    print("Partial data saved to 'dados_brutos.yaml'.")

# Start harvesting records
print("\nHarvesting records...")
records = sickle.ListRecords(metadataPrefix='oai_dc')

for i, record in enumerate(records, start=1):
    dados["Registos"].append(dict(record))  # Convert to dictionary

    if i % 10 == 0:  # Save every 10 records
        save_to_file()
        print(f"Saved {i} records so far...")

# Final save to make sure all records are written
save_to_file()
print("\nHarvesting complete. All data saved to 'dados_brutos.yaml'.")


