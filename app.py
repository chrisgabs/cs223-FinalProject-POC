from flask import Flask, render_template, request, jsonify
from FSM import fsm_ordinances, fsm_resolutions, fsm_title, fsm_candidates, fsm_dates1, fsm_dates2, fsm_proclamations


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text')
    # Process the text here
    title = fsm_title.run(text, fsm_candidates)
    ordinances = fsm_ordinances.run(text)
    resolutions = fsm_resolutions.run(text)
    dates = fsm_dates1.run(text)
    proclamations = fsm_proclamations.run(text)
    print(proclamations)
    dates2 = []
    for token in text.split(" "):
        if fsm_dates2.run(token):
            dates2.append(token)
    response_data = {'data': {
        'title': title,
        'resolutions': resolutions,
        'ordinances': ordinances,
        'dates': dates + dates2,
        'proclamations': proclamations
    }}
    return jsonify(response_data)

# if __name__ == "__main__":
#     from asgiref.wsgi import WsgiToAsgi
#     import uvicorn
#     print("asd")
#     server = WsgiToAsgi(app)
#     uvicorn.run(server, host="0.0.0.0", port=8000)
