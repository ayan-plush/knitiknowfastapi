from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import spacy
# from allennlp.predictors.predictor import Predictor
# import allennlp_models.coref
import coreferee


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("coreferee")
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# coref_predictor = Predictor.from_path(
#     "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
# )

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def is_chunk_about_mp(chunk, mp_name):
    doc = nlp(chunk)
    return any(ent.label_ == "PERSON" and mp_name.lower() in ent.text.lower() for ent in doc.ents)

def is_chunk_about_mp_coref(chunk, mp_name):
    doc = nlp(chunk)
    if not doc._.has_coref:
        return False
    for cluster in doc._.coref_clusters:
        if mp_name.lower() in cluster.main.text.lower():
            return True
    return False

def is_relevant_chunk(chunk, mp_name):
    if is_chunk_about_mp(chunk, mp_name):
        return True
    if any(p in chunk.lower() for p in [" he ", " she ", " they ", " politician ", " minister ", "mr", "mrs"]):
        return is_chunk_about_mp_coref(chunk, mp_name)
    return False

def vectorize_article(article_text, mp_name):
    chunks = splitter.split_text(article_text)
    relevant_chunks = [c for c in chunks if is_relevant_chunk(c, mp_name)]
    embeddings = embed_model.encode(relevant_chunks).tolist()
    return list(zip(relevant_chunks, embeddings))
