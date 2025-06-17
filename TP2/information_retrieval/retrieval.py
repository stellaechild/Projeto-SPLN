from sentence_transformers import SentenceTransformer, util
from jjcli import clfilter
from pathlib import Path
from importlib import resources


class SimilarityCalculator:
    def __init__(self):
        with resources.path("information_retrieval.output", "repositorium-similarity-model") as model_path:
            self.model = SentenceTransformer(str(model_path))

    def compute_pairwise_similarity(self, texts):

        if len(texts) < 2:
            raise ValueError("É necessário pelo menos dois textos para calcular similaridade.")

        embeddings = self.model.encode(texts, convert_to_tensor=True)
        similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

        return similarity_matrix

    def most_similar_pairs(self, texts, filenames, top_n=None):
  
        similarity_matrix = self.compute_pairwise_similarity(texts)
        pairs = []

        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                pairs.append(((filenames[i], filenames[j]), similarity_matrix[i][j].item()))

        pairs.sort(key=lambda x: x[1], reverse=True)

        return pairs if top_n is None else pairs[:top_n]


def main():
    cl = clfilter(opt="n:", man=__doc__)

    abstracts = {}

    for abstract in cl.input():
        name = cl.filename()
        abstracts[name] = abstract

    if len(abstracts) < 2:
        print("Erro: São necessários pelo menos dois documentos válidos para comparar.")
        return

    filenames = list(abstracts.keys())
    texts = list(abstracts.values())

    sim_calc = SimilarityCalculator()
    
    top_n = int(cl.opt.get("-n", len(filenames) * (len(filenames) - 1) // 2))

    similar_pairs = sim_calc.most_similar_pairs(texts, filenames, top_n)

    for (file1, file2), score in similar_pairs:
        print(f"{file1} <-> {file2}: Similaridade = {score:.4f}")


if __name__ == "__main__":
    main()
