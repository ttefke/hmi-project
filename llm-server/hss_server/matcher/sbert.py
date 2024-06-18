from db import db_select
from quart import jsonify
import pickle
import torch

from sentence_transformers import util

def vectorise_text(ctx, json_payload):
    """
    This method returns the vector representation of a string for a given model
    @param ctx: contexter
    @param json_payload: string to vectorise
    @return: json with componenys language_model, dimension, vector
    """
    logger = ctx["logger"]
    llm_name = ctx["llm_name"]
    embedder = ctx["st_object_model"]
    device = ctx["torch_device"]

    # Input validate language

    if not "language" in json_payload:
        return jsonify('{No language specified}')

    lang = json_payload["language"]
    
    if not isinstance(lang, str):
        return jsonify('{Language must be string}')   
    
    lang = lang.strip().lower()

    # Input validate text to be vectorised (check if vectorise field exists and is either list type of string)
    if not "vectorise" in json_payload:
        return jsonify('{No text to be vectorised specified}')
    
    if not (isinstance(json_payload['vectorise'], list) or isinstance(json_payload['vectorise'], str)):
        return jsonify('{Text to be vectorised must be list of strings or string}')
    
    logger.debug('GET /sbert_get_vector/{}'.format(json_payload))

    match = {}
    cnt = 0
    for query in json_payload['vectorise']:
        # Input validate text to be vectorised (check if each element of the list is string)
        if not isinstance(query, str):
            return jsonify('{Text to be vectorised must be list of strings or string}')
        
        query_embedding = embedder.encode(query, device=device, show_progress_bar=False)
        dim = len(query_embedding)
        vector = query_embedding.tolist()
        match[cnt] = {
            'llm': llm_name,
            'dimension': dim,
            'language': lang,
            'text': query,
            'vector': vector
        }
        cnt += 1
        logger.debug('{0}'.format(match))

    return match


def read_learned_model():
    try:
        with open("data/models/gte-large_en.pkl", "rb") as fo:
            return pickle.load(fo)
    except IOError as err:
        print(err)

def get_course_by_similarity(ctx, query, similarity_indicator):
    # similarity_indicator is either "learning_objectives" or "course_contents"
    embedder = ctx["st_object_model"]
    device = ctx["torch_device"]

    # Load already known sentences
    vectorised_modules = read_learned_model()[similarity_indicator]

    # Encode learning object handed over by user
    vectorised = embedder.encode(query, device=device, show_progress_bar=False)
    combinations = []

    # Calculate cosine distance for each sentence <-> learning goal combination 
    for i in range(len(vectorised_modules)):
        combinations.append([i+1, util.cos_sim(vectorised, vectorised_modules[i]).item()])

    # Sort by match rate
    combinations = sorted(combinations, key=lambda x:x[1], reverse=True)

    # Return details for courses having a match rate >= 0.8
    matching_courses = []
    for index, score in combinations:
        if (score >= 0.75):
            db_record = db_select.get_course_by_index(ctx["db_courses"], index)
            matching_courses.append([score, db_record])

    return matching_courses