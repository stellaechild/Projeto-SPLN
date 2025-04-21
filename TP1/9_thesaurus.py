import yaml

with open('dados_brutos.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

unique_entries = set()
categories = {}

for record in data.get('Registos', []):
    record_type = record.get('type', ['Uncategorized'])[0]
    title = record.get('title', [''])[0]
    terms = record.get('subject', [])
    if terms:
        entry = (title, tuple(terms))
        if entry not in unique_entries:
            unique_entries.add(entry)
            if record_type not in categories:
                categories[record_type] = []
            categories[record_type].append((title, terms))


with open('thesaurus.html', 'w', encoding='utf-8') as output_file:
    output_file.write("<html><head><title>Registos</title></head><body>\n")
    output_file.write("<h1>Registos</h1>\n")
    output_file.write("<h2>Indices</h2>\n<ul>\n")
    for category in categories:
        output_file.write(f'<li><a href="#{category}">{category}</a></li>\n')
    output_file.write("</ul>\n")

    for category, records in categories.items():
        output_file.write(f'<h2 id="{category}">{category}</h2>\n<ul>\n')
        for title, terms in records:
            output_file.write("<li>\n")
            output_file.write(f"<h3>{title}</h3>\n")
            output_file.write("<ul>\n")
            for term in terms:
                output_file.write(f"<li>{term}</li>\n")
            output_file.write("</ul>\n")
            output_file.write("</li>\n")
        output_file.write("</ul>\n")

    output_file.write("</body></html>\n")
