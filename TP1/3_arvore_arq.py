import os
import yaml

class Node:
    def __init__(self, id, title, tipo, full_id, parent_id=None):
        self.id = id
        self.title = title
        self.tipo = tipo
        self.full_id = full_id
        self.parent_id = parent_id
        self.children = []

    def __repr__(self, level=0):
        tipo_label = f" [{self.tipo}]" if self.tipo else ""
        ret = "\t" * level + f"{self.id}{tipo_label} - {self.title}\n"
        for child in sorted(self.children, key=lambda x: x.id):
            ret += child.__repr__(level + 1)
        return ret

# 1. Carregar YAMLs
records = []
for filename in os.listdir("records_yaml"):
    if filename.startswith("record_") and filename.endswith(".yaml"):
        with open(os.path.join("records_yaml", filename), encoding="utf-8") as f:
            data = yaml.safe_load(f)
            records.append(data)

# 2. Criar dicionário por ID completo (ex: PT/MVNF/AMAS/CSC/006-003)
records_by_id = {}
for record in records:
    full_id = None
    for ident in record.get("identificadores", []):
        if ident.startswith("PT/"):
            full_id = ident
            break
    if not full_id:
        continue
    records_by_id[full_id] = record

# 3. Criar todos os nós, incluindo caminhos fictícios
nodes = {}

def ensure_node_chain(full_id):
    parts = full_id.split("/")
    for i in range(1, len(parts)+1):
        sub_id = "/".join(parts[:i])
        if sub_id not in nodes:
            node_id = parts[i-1]
            record = records_by_id.get(sub_id, {})
            title = record.get("titulo", f"({node_id})")
            tipo = record.get("tipo") if record else None

            if tipo == None:
                if i == 1:
                    tipo = 'F'  
                elif i == 2:
                    tipo = 'SC'  
                elif i == 3:
                    tipo = 'SSC'  
                elif i == 4:
                    tipo = 'SR'  
                elif i >= 5:
                    tipo = 'UI'
                    
            parent_id = "/".join(parts[:i-1]) if i > 1 else None
            nodes[sub_id] = Node(
                id=node_id,
                title=title,
                tipo=tipo,
                full_id=sub_id,
                parent_id=parent_id
            )

for full_id in records_by_id:
    ensure_node_chain(full_id)

root_nodes = []
for node in nodes.values():
    if node.parent_id and node.parent_id in nodes:
        nodes[node.parent_id].children.append(node)
    else:
        root_nodes.append(node)

for root in sorted(root_nodes, key=lambda x: x.id):
    print(root)


