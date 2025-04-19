import xml.etree.ElementTree as ET
import yaml
import sys
import os

def parse_record_to_dict(record_xml):
    ns = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/'
    }

    root = ET.fromstring(record_xml)

    # Header
    header = root.find('oai:header', ns)
    identifier = header.find('oai:identifier', ns).text.strip()
    sets = [s.text.strip() for s in header.findall('oai:setSpec', ns)]

    # Metadata
    metadata = root.find('oai:metadata/oai_dc:dc', ns)

    def get_dc(tag):
        return [e.text.strip() for e in metadata.findall(f'dc:{tag}', ns)]

    data = get_dc('date')
    date_inicio = data[0] if len(data) > 0 else None
    date_fim = data[1] if len(data) > 1 else None

    record = {
        'id': identifier,
        'titulo': get_dc('title')[0] if get_dc('title') else None,
        'datas': {
            'inicio': date_inicio,
            'fim': date_fim,
        },
        'editor': get_dc('publisher')[0] if get_dc('publisher') else None,
        'assunto': get_dc('subject')[0] if get_dc('subject') else None,
        'tipo': get_dc('type')[0] if get_dc('type') else None,
        'formato': get_dc('format')[0] if get_dc('format') else None,
        'lingua': get_dc('language')[0] if get_dc('language') else None,
        'identificadores': get_dc('identifier'),
        'thumbnail': get_dc('relation')[0] if get_dc('relation') else None,
        'colecoes': sets,
    }
    return record
    
def save_records_yaml():
    os.makedirs("records_yaml", exist_ok=True)
    for i in range(0,101):
        with open(f"records_yaml/record_{i}.yaml", "w", encoding="utf-8") as f:
            xml = open(f"records/record_{i}.xml", "r", encoding="utf-8").read()
            r = parse_record_to_dict(xml)
            f.write(yaml.dump(r, allow_unicode=True, sort_keys=False))
            print(f"Registo {i} convertido e guardado em YAML.")
     
            
if __name__ == "__main__":
    save_records_yaml()

    