import os
import yaml
from typing import Dict, List, Optional

class ArchivalNode:
    def __init__(self, 
                 id: str, 
                 title: str, 
                 tipo: str,
                 full_id: str,
                 parent_id: Optional[str] = None,
                 children: Optional[List['ArchivalNode']] = None):
        self.id = id
        self.title = title
        self.tipo = tipo
        self.full_id = full_id
        self.parent_id = parent_id
        self.children = children if children is not None else []

    def __repr__(self, level=0):
        tipo_label = f" [{self.tipo}]" if self.tipo else ""
        ret = "\t" * level + f"{self.id}{tipo_label} - {self.title}\n"
        for child in sorted(self.children, key=lambda x: x.id):
            ret += child.__repr__(level + 1)
        return ret

def load_yaml_records(directory: str) -> Dict[str, ArchivalNode]:
    """Load all YAML records and construct full node hierarchy."""
    nodes = {}
    records_by_id = {}

    # Carregar todos os records e armazenar por identificador
    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                record = yaml.safe_load(f)
                full_id = next((id for id in record.get('identificadores', []) if id.startswith('PT/')), None)
                if not full_id:
                    continue
                records_by_id[full_id] = record

    # Criar toda a cadeia hierárquica
    def ensure_node_chain(full_id):
        parts = full_id.split("/")
        for i in range(1, len(parts) + 1):
            sub_id = "/".join(parts[:i])
            if sub_id not in nodes:
                node_id = parts[i - 1]
                record = records_by_id.get(sub_id, {})
                title = record.get("titulo", f"({node_id})")
                tipo = record.get("tipo")

                # Inferir tipo, se não existir
                if tipo is None:
                    if i == 1:
                        tipo = 'F'
                    elif i == 2:
                        tipo = 'SC'
                    elif i == 3:
                        tipo = 'SSC'
                    elif i == 4:
                        tipo = 'SR'
                    else:
                        tipo = 'UI'

                parent_id = "/".join(parts[:i - 1]) if i > 1 else None

                nodes[sub_id] = ArchivalNode(
                    id=node_id,
                    title=title,
                    tipo=tipo,
                    full_id=sub_id,
                    parent_id=parent_id
                )

    for full_id in records_by_id:
        ensure_node_chain(full_id)

    # Criar relações pai-filho
    for node in nodes.values():
        if node.parent_id in nodes:
            nodes[node.parent_id].children.append(node)

    return nodes


def generate_directory_structure(nodes: Dict[str, ArchivalNode], base_path: str = "output/arvore"):
    os.makedirs(base_path, exist_ok=True)
    
    # Find root nodes (nodes with no parent or parent not in nodes)
    root_nodes = [node for node in nodes.values() 
                 if node.parent_id is None or node.parent_id not in nodes]
    
    # Process each root node
    for root in sorted(root_nodes, key=lambda x: x.id):
        _create_directory_structure(root, base_path, nodes)

def _create_directory_structure(node: ArchivalNode, current_path: str, nodes: Dict[str, ArchivalNode]):
    # Create directory name with format: ID-TIPO-Title
    dir_name = f"{node.id}-{node.tipo}-{node.title.replace('/', '_')}"
    dir_path = os.path.join(current_path, dir_name)
    
    # Create the directory
    os.makedirs(dir_path, exist_ok=True)
    
    # Create a README file with node information
    with open(os.path.join(dir_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(f"# {node.id} {node.tipo} - {node.title}\n\n")
        f.write(f"- **ID Completo**: {node.full_id}\n")
        if node.parent_id:
            f.write(f"- **Parent ID**: {node.parent_id}\n")
    
    # Process children
    for child in sorted(node.children, key=lambda x: x.id):
        _create_directory_structure(child, dir_path, nodes)

def generate_text_tree(nodes: Dict[str, ArchivalNode]) -> str:
    # Find root nodes
    root_nodes = [node for node in nodes.values() 
                 if node.parent_id is None or node.parent_id not in nodes]
    
    output = ""
    for root in sorted(root_nodes, key=lambda x: x.id):
        output += root.__repr__()
    return output

def generate_html_tree_with_links(nodes: Dict[str, ArchivalNode], html_output: str, record_dir: str):
    root_nodes = [n for n in nodes.values() if n.parent_id not in nodes]

    def build_html(node: ArchivalNode) -> str:
        filename = None
        for fname in os.listdir(record_dir):
            if fname.endswith(".yaml"):
                path = os.path.join(record_dir, fname)
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if node.full_id in data.get("identificadores", []):
                        filename = fname
                        break

        label = f"{node.id}-{node.tipo}-{node.title}".replace("/", "_")
        if filename:
            label = f'<a href="../{record_dir}/{filename}">{label}</a>'

        html = [f"<li>{label}"]
        if node.children:
            html.append("<ul>")
            for child in sorted(node.children, key=lambda x: x.id):
                html.append(build_html(child))
            html.append("</ul>")
        html.append("</li>")
        return '\n'.join(html)

    html_lines = [
        "<html><head><meta charset='UTF-8'><title>Árvore Arquivística</title></head><body>",
        "<h1>Árvore Arquivística</h1>",
        "<ul>"
    ]

    for root in sorted(root_nodes, key=lambda x: x.id):
        html_lines.append(build_html(root))

    html_lines += ["</ul>", "</body></html>"]

    os.makedirs(os.path.dirname(html_output), exist_ok=True)
    with open(html_output, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))


def save_output(content: str, filename: str):
    """Save output to file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    yaml_dir = "records_yaml"
    nodes = load_yaml_records(yaml_dir)

    # Gerar árvore textual
    text_tree = generate_text_tree(nodes)
    save_output(text_tree, "output/archival_tree.txt")

    # Gerar estrutura de diretórios
    generate_directory_structure(nodes, "output/arvore_diretorios")

    # Gerar HTML com links
    generate_html_tree_with_links(nodes, "output/html_arvore/index.html", yaml_dir)

    print("Operações concluídas:")
    print("- Árvore textual gerada em: output/archival_tree.txt")
    print("- Estrutura de diretórios criada em: output/arvore_diretorios/")
    print("- HTML com links gerado em: output/html_arvore/index.html")
