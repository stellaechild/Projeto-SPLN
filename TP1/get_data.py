import yaml
import re
from sickle import Sickle
from langcodes import Language

# OAI-PMH endpoint: Famalicão (Alberto Sampaio)
endpoint = "https://www.arquivoalbertosampaio.org/OAI-PMH/"
sickle = Sickle(endpoint)

dados = {"Registos": []}

def save_to_file():
    with open("./TP1/dados_brutos.yaml", "w", encoding="utf-8") as f:
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

from langcodes import Language

def get_language_name(lang_code):
    """
    Converte códigos de idioma para nomes completos de forma robusta:
    - 'por' → 'Portuguese'
    - ['por'] → 'Portuguese'
    - 'pt' → 'Portuguese'
    - 'glg' → 'Galician'
    - Valores inválidos retornam o original
    """
    if isinstance(lang_code, list):
        lang_code = lang_code[0] if lang_code else ''
    
    if not lang_code:
        return ''
    
    try:
        lang = Language.get(str(lang_code))  # Converte para string para segurança
        return lang.display_name() if lang.is_valid() else lang_code
    except:
        return lang_code


def pretty_print(registo, output_format='text', config=None, registo_num=None):
    # função para dar print (pretty) em html, wiki e yaml
    if config is None:
        config = {
            'title': {'prefix': 'Title: ', 'format': '{value}'},
            'date': {'prefix': 'Date: ', 'format': '{value[0]} - {value[1]}'},
            'format': {'prefix': 'Format: ', 'format': '{value}'},
            'identifier': {'prefix': 'ID: ', 'format': '{value[0]}'},
            'language': {'prefix': 'Language: ', 'format': '{value}'},
            'publisher': {'prefix': 'Publisher: ', 'format': '{value[0]}'},
            'relation': {'prefix': 'Relation: ', 'format': '{value[0]}'},
            'subject': {'prefix': 'Subject: ', 'format': '{value[0]}'},
            'type': {'prefix': 'Type: ', 'format': '{value[0]}'},
            'default': {'prefix': '', 'format': '{value}'}
        }

    def format_field(field, value):
        if not value:
            return ""
        
        field_config = config.get(field, config['default'])
        
        if field == 'language':
            value = get_language_name(value)
        
        # Se for uma lista, junta os elementos corretamente, garantindo que não é uma string acidentalmente tratada como lista
        if field =='title' or field == 'format':
            value = ", ".join(value)
        
        try:
            return field_config['format'].format(value=value)
        except (IndexError, KeyError):
            return str(value)  # Fallback para dados malformados


    if output_format == 'html':
        output = ['<div class="registo">']
        output.append('<dl class="registo-metadata">')
        for field, value in registo.items():
            if value:
                formatted_value = format_field(field, value)
                output.append(f'<dt>{config.get(field, config["default"])["prefix"].strip(": ")}</dt>')
                output.append(f'<dd>{formatted_value}</dd>')
        output.append('</dl></div>')
        return '\n'.join(output)
    
    elif output_format == 'wiki':
        output = []
        for field, value in registo.items():
            if value:
                formatted_value = format_field(field, value)
                prefix = config.get(field, config['default'])['prefix']
                output.append(f"* {prefix}{formatted_value}")
        return '\n'.join(output)
    
    elif output_format == 'yaml':
        with open('./TP1/dados_brutos.yaml', 'r', encoding='utf-8') as f:
            content = f.read()
        print(content) 
    
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
        save_records_html(dados["Registos"], "./TP1/registos.html")


