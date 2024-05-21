import pickle
from sentence_transformers import SentenceTransformer

from db.db_select import get_learning_obj_en, get_course_contents
import torch


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

    try:
        embedder = SentenceTransformer(llm_name)
        #  save model to disk
        with open(model_output, "wb") as fo:
            objectives = embedder.encode(flat_learning_obj, device=get_torch_devide(), convert_to_tensor=True)
            contents = embedder.encode(flat_course_contents, device=get_torch_devide(), convert_to_tensor=True)
            
            data = {
                "learning_objectives": objectives,
                "course_contents": contents
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
