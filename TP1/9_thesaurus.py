import yaml

with open('dados_brutos.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

unique_entries = set()
categorias = {}

for registo in data.get('Registos', []):
    registo_type = registo.get('type', ['Uncategorized'])[0]
    title = registo.get('title', [''])[0]
    terms = registo.get('subject', [])
    if terms:
        entry = (title, tuple(terms))
        if entry not in unique_entries:
            unique_entries.add(entry)
            if registo_type not in categorias:
                categorias[registo_type] = []
            categorias[registo_type].append((title, terms))


with open('thesaurus.html', 'w', encoding='utf-8') as output_file:
    output_file.write("<html><head><title>Registos</title></head><body>\n")
    output_file.write("<h1>Registos</h1>\n")
    output_file.write("<h2>Índice</h2>\n<ul>\n")
    for categoria in categorias:
        output_file.write(f'<li><a href="#{categoria}">{categoria}</a></li>\n')
    output_file.write("</ul>\n")

    for categoria, registos in categorias.items():
        output_file.write(f'<h2 id="{categoria}">{categoria}</h2>\n<ul>\n')
        for title, terms in registos:
            output_file.write("<li>\n")
            output_file.write(f"<h3>{title}</h3>\n")
            output_file.write("<ul>\n")
            for term in terms:
                output_file.write(f"<li>{term}</li>\n")
            output_file.write("</ul>\n")
            output_file.write("</li>\n")
        output_file.write("</ul>\n")

    output_file.write("</body></html>\n")
