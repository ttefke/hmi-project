from quart import jsonify
import pickle
import torch

from sentence_transformers import util

from db.db_select import *
from .formatter import *

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

def get_course_by_similarity(ctx, query, similarity_indicator, match_rate=0.75):
    # similarity_indicator is either "learning_objectives" or "course_contents"
    embedder = ctx["st_object_model"]
    device = ctx["torch_device"]

    # Load already known sentences
    vectorised_modules = read_learned_model()["sentence_transformer"][similarity_indicator]

    # Encode learning object handed over by user
    vectorised = embedder.encode(query, device=device, show_progress_bar=False)
    combinations = []

    # Calculate cosine distance for each sentence <-> learning goal combination 
    for i in range(len(vectorised_modules)):
        combinations.append([i+1, util.cos_sim(vectorised, vectorised_modules[i]).item()])

    # Sort by match rate
    combinations = sorted(combinations, key=lambda x:x[1], reverse=True)

    # Return details for courses having a match rate >= 0.75
    matching_courses = []
    for index, score in combinations:
        if (score >= match_rate):
            db_record = get_course_by_index(ctx["db_courses"], index)
            matching_courses.append([score, db_record])
    return matching_courses

def flatten_courses(courses):
    result = []
    for course in courses:
        result.append(course[1])
    return result


def list_courses_freeform(ctx, json_payload):
    db_courses = ctx["db_courses"]

    if not "query" in json_payload:
        return jsonify('{No course query given}')
    
    query = json_payload["query"]

    if not isinstance(query, str):
        return jsonify({'Query must be of type string'})

    match = {}

    question_words = ["what", "when", "where", "which", "who", "why", "how"]
    if any(x in query.lower() for x in question_words):

        # Read and rank sentences. This might take a couple of seconds
        # if using the CPU as pytorch device.
        # because the ranking has to be calculated each time
        # Crossencoders do not allow prior vectorization to speed up the search.
        courses = read_learned_model()["cross_encoder"]["sentences"]
        model = ctx["cross_encoder"]
        ranks = model.rank(query, flatten_courses(courses), show_progress_bar=False)

        # get best matches
        result = {}
        for rank in ranks:
            index = courses[rank['corpus_id']][0]
            answer = courses[rank['corpus_id']][1]
            score = rank['score']
            if index in result:
                if result[index] < score:
                    result[index] = score
            else:
                result[index] = score
        
        # get courses to filter them
        result_courses = []
        for k, v in result.items():
            if v > 0.9:
                result_courses.append([v, get_course_by_index(db_courses, k)])
        
        match = toDict(result_courses, existingCourses=match)
    else:
        match = toDict(get_course_by_similarity(ctx, query, "learning_objectives", 0.8))
        match = toDict(get_course_by_similarity(ctx, query, "course_contents", 0.8), existingCourses=match)
        match = toDict(get_course_by_similarity(ctx, query, "course_titles", 0.85), existingCourses=match)


    return match