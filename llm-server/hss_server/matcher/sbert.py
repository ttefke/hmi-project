from db import db_select
from quart import jsonify

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


