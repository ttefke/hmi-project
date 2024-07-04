import pickle
from sentence_transformers import SentenceTransformer

from db.db_select import get_learning_obj_en, get_course_contents, get_titles
import torch
import sqlite3


def get_torch_devide():
    # Training with cuda and using cpu afterwards fails with Docker #TODO: revisit later, maybe there is a solution for this
    #if torch.backends.mps.is_available():
    #    torch_device = torch.device('mps')
    #elif torch.cuda.is_available():
    #    torch_device = 'cuda'
    #else:
    #    torch_device = 'cpu'
    #return torch_device
    return 'cpu'

def generate_sentences(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS number, title, instructor, course_type, time FROM acs_modules')
    records = cursor.fetchall()
    courses = []
    for row in records:
        index = row[0]
        title = row[1]
        instructor = row[2]
        area = row[3]
        term = row[4]

        areas = []
        terms = []

        if "elective" in area:
            areas = ["elective", "optional", "selective", "voluntary", "nonobligatory"]
        elif "obligatory" in area:
            areas = ["compulsory", "obligatory", "mandatory", "required", "needed", "necessary"]
        
        if "1" in term:
            additional_terms = ["1st term", "1st semester", "winter semester", "winter term"]
            terms += additional_terms
        if "2" in term:
            additional_terms = ["2nd term", "2nd semester", "summer semester", "summer term"]
            terms += additional_terms
        if "3" in term:
            additional_terms = ["3rd term", "3rd semester", "winter semester", "winter term"]
            terms += additional_terms

        for a in areas:
            for t in terms:
                courses.append([index, title + " is a " + a + " course taught by " + instructor + " in the " + t])
                courses.append([index, instructor + " offeres the " + a + " course " + title + " in the " + t])
    conn.close()
    return courses

def train(db, llm_name, model_output):
    """
    Trains a LLM using SBERT and the description from the skills in the ESCO database
    @param db: path todatabase location
    @param llm_name: SBERT larnguage mode name
    @param model_output: output file contained the trained serialised language model
    @return:
    """

    # Retrieve learning objects
    learning_obj = get_learning_obj_en(db)
    flat_learning_obj = [item for sublist in learning_obj for item in sublist]

    # Retrieve content
    course_contents = get_course_contents(db)
    flat_course_contents = [item for sublist in course_contents for item in sublist]

    # Retrieve titles
    course_titles = get_titles(db)

    try:
        embedder = SentenceTransformer(llm_name)
        #  save model to disk
        with open(model_output, "wb") as fo:
            objectives = embedder.encode(flat_learning_obj, device=get_torch_devide(), convert_to_tensor=True)
            contents = embedder.encode(flat_course_contents, device=get_torch_devide(), convert_to_tensor=True)
            titles = embedder.encode(course_titles, device=get_torch_devide(), convert_to_tensor=True)
            
            data = {
                "cross_encoder": {
                    "sentences": generate_sentences(db)
                },
                "sentence_transformer": {
                    "learning_objectives": objectives,
                    "course_contents": contents,
                    "course_titles": titles
                }
            }
            pickle.dump(data, fo)
    except IOError as err:
        print(err)

    return 0


if __name__ == "__main__":
    # demonstration of how to call the vectorise text off-line
    location_db = "../data/db/courses.sqlite"
    llm_name = "thenlper/gte-large"
    model_vectorised_loc = "../data/models/gte-large_en.pkl"
    # train model in English
    train(location_db, llm_name, model_vectorised_loc)
