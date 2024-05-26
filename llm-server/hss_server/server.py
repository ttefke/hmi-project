import logging

import ctx
from quart_cors import *
from quart import Quart, request, jsonify
from pyfiglet import Figlet
from matcher.sbert import *
from matcher.query import *

logging.getLogger('asyncio').setLevel(logging.ERROR)  # remove asyncio logging
# --------------------------------------------------------
app = Quart(__name__)
app = cors(app, allow_origin="*")

f = Figlet(font='slant')
print(f.renderText('S E R V E R'))
# --------------------------------------------------------------------------
# GLOBAL CONTEXT
ctx = ctx.handler()
logger = ctx["logger"]
# --------------------------------------------------------------------------


@app.route('/vectorise/', methods=['POST'])
async def vectorise():
    """
    {
        "language": "en",
        "vectorise": [
            "Text A to vectorise",
            "Text B to vectorise",
            "Text C to vectorise"
        ]
    }
    @return: a JSON file with dimension, llm model, text to vectorise, and the numerical vector for eact text within
    the vectorise array
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = vectorise_text(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is requiered, please check request}')
        logger.debug('{}'.format(resp))
    return resp


@app.route('/course_by_title/', methods=['POST'])
async def course_by_title():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_title(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is required, please check request}')
        logger.debug('{}'.format(resp))
    return resp

@app.route('/course_by_instructor/', methods=['POST'])
async def course_by_instructor():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_instructor(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is required, please check request}')
        logger.debug('{}'.format(resp))
    return resp

@app.route('/course_by_area/', methods=['POST'])
async def course_by_area():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_area(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is required, please check request}')
        logger.debug('{}'.format(resp))
    return resp
    
@app.route('/course_by_term/', methods=['POST'])
async def course_by_term():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_term(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is required, please check request}')
        logger.debug('{}'.format(resp))
    return resp

@app.route('/course_by_learning/', methods=['POST'])
async def course_by_learning():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_learning(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is required, please check request}')
        logger.debug('{}'.format(resp))
    return resp

@app.route('/course_by_contents/', methods=['POST'])
async def course_by_contents():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_contents(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is required, please check request}')
        logger.debug('{}'.format(resp))
    return resp

# do not use this in production, run the app as follows: $ hypercorn server:app
app.run(host="0.0.0.0", debug=False, port=3000)
