import flask
import uuid
import queue.queue

app = flask.Flask(__name__)

@app.route('/')
def index():
    queue_size, source = queue.queue.get_queue_size(True)
    return flask.jsonify({'status': 'OK', 'queue_size': queue_size, 'queue_size_source': source})

@app.route('/publish', methods=['POST'])
def publish():
    try:
        data = flask.request.form['data']
        item_id = queue.queue.publish(data)
        return flask.jsonify({'item_id': item_id}), 200
    except Exception as e:
        # no, I'm not doing anything with the errors
        error_id=uuid.uuid1()
        return flask.jsonify({'error_id': error_id}), 500
