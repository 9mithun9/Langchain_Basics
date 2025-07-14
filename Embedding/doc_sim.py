from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity


load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=300)

docs = [
    "Blue is the warmest color is a 2013 French romantic coming-of-age drama film directed by Abdellatif Kechiche.",
    "Pulp Fiction is a 1994 American neo-noir black comedy crime film written and directed by Quentin Tarantino.",
    "The Shawshank Redemption is a 1994 American drama film written and directed by Frank Darabont.",
    "The Godfather is a 1972 American crime film directed by Francis Ford Coppola.",
    "The Dark Knight is a 2008 superhero film directed by Christopher Nolan."
]


query = "Tell me about 1994 American drama"

query_embeddings = embedding.embed_query(query)
doc_embeddings = embedding.embed_documents(docs)


cosine_similarity_scores = cosine_similarity([query_embeddings], doc_embeddings)[0]

index, scores = sorted(list(enumerate(cosine_similarity_scores)), key=lambda x: x[1])[-1]

print(docs[index], scores)
