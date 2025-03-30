import yaml
from sickle import Sickle

# OAI-PMH endpoint: Famalicão (Alberto Sampaio)
endpoint = "https://www.arquivoalbertosampaio.org/OAI-PMH/"
sickle = Sickle(endpoint)

dados = {"Registos": []}

def save_to_file():
    with open("dados_brutos.yaml", "w", encoding="utf-8") as f:
        yaml.dump(dados, f, allow_unicode=True, default_flow_style=False)
    print("Dados parciais salvos no ficheiro 'dados_brutos.yaml'.")


print("\nComeçando a registar...")
registos = sickle.ListRecords(metadataPrefix='oai_dc')

for i, registo in enumerate(registos, start=1):
    dados["Registos"].append(dict(registo)) 

    if i % 10 == 0:  # Salvando a cada 10 registos e parando quando chegam a 500 (para eficiência nos testes)
        save_to_file()
        print(f"{i} registos...")
    if i == 500 : 
        break

# Caso tivesse um ficheiro em falta para salvar
save_to_file()
print("Concluído. Todos os dados encontram-se no ficheiro 'dados_brutos.yaml'.")


def pretty_print(registo, output_format='text', config=None):
    # função para dar print (pretty) em html, wiki e yaml
    if config is None:
        config = {
            'title': {'prefix': 'Title: ', 'format': '{value}'},
            'date': {'prefix': 'Date: ', 'format': '{value[0]} - {value[1]}'},
            'format': {'prefix': 'Format: ', 'format': '{value}'},
            'identifier': {'prefix': 'ID: ', 'format': '{value[0]}'},
            'default': {'prefix': '', 'format': '{value}'}
        }
    
    if output_format == 'html':
        output = ['<div class="registo">']
        for field, value in registo.items():
            field_config = config.get(field, config['default'])
            formatted_value = field_config['format'].format(value=value)
            output.append(f'<p><strong>{field_config["prefix"]}</strong>{formatted_value}</p>')
        output.append('</div>')
        return '\n'.join(output)
    
    elif output_format == 'wiki':
        output = []
        for field, value in registo.items():
            field_config = config.get(field, config['default'])
            formatted_value = field_config['format'].format(value=value)
            output.append(f"* {field_config['prefix']}{formatted_value}")
        return '\n'.join(output)
    
    elif output_format == 'yaml':
        return yaml.dump(registo, allow_unicode=True, default_flow_style=False)
    
    else:
        raise ValueError(f"Unsupported format: {output_format}")

# Salvar os dados num ficheiro HTML
def save_records_html(registos, filename="registos_output.html"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Arquivos de Famalicão (Alberto Sampaio)</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
        .registo { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; }
        h1 { color: #333; }
        .summary { margin: 30px 0; }
        table { border-collapse: collapse; width: 50%; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Arquivos de Famalicão (Alberto Sampaio)</h1>
''')
        
        for i, registo in enumerate(registos, 1):
            f.write(f'<h3>Registo {i}</h3>')
            f.write(pretty_print(registo, 'html'))
        
        f.write('</body>\n</html>')
    print(f"Todos os registos armazenados em {filename}.\n")

def analyze_data_structure(data):
    field_counts = {}
    constant_fields = {}
    keys = set()
    
    for registo in data["Registos"]:
        for field in registo:
            field_counts[field] = field_counts.get(field, 0) + 1
            
            if field in constant_fields:
                if constant_fields[field] != registo[field]:
                    constant_fields[field] = None  # Marcar como não constante
            else:
                constant_fields[field] = registo[field]

    total_records = len(data["Registos"])
    for field, count in field_counts.items():
        if count == total_records:
            keys.add(field)
    
    print("Field counts:", field_counts)
    print("Constant fields:", {k:v for k,v in constant_fields.items() if v is not None})
    print("Potential keys:", keys)

analyze_data_structure(dados)

def simplify_date(date_values):
    if not date_values:
        return {'start': None, 'end': None, 'certainty': 'unknown'}
    
    # Handle cases where date might be a single year or range
    if len(date_values) == 1:
        date_str = date_values[0]
        if '-' in date_str:
            start, end = date_str.split('-')[:2]
            return {'start': start.strip(), 'end': end.strip(), 'certainty': 'range'}
        else:
            return {'start': date_str, 'end': date_str, 'certainty': 'exact'}
    else:
        return {'start': date_values[0], 'end': date_values[-1], 'certainty': 'range'}
    
def aggregate_by_type(data):
    from collections import defaultdict
    by_type = defaultdict(list)
    
    for registo in data["Registos"]:
        if 'type' in registo:
            for t in registo['type']:
                by_type[t].append(registo)
    
    return by_type

for registo in dados["Registos"]:
    if 'date' in registo:
        print("\n--- WIKI ---\n")
        print(pretty_print(registo, 'wiki'))
        registo['date_normalized'] = simplify_date(registo['date'])
        save_records_html(dados["Registos"], "registos.html")


