from flask import Flask, render_template, request, jsonify
from FSM import fsm_ordinances, fsm_resolutions, fsm_title, fsm_candidates


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
    print(ordinances)
    resolutions = fsm_resolutions.run(text)
    response_data = {'data': {
        'title': title,
        'resolutions': resolutions,
        'ordinances': ordinances
    }}
    return jsonify(response_data)
