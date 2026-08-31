from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json, os, time

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# GET all data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(read_data())

# PROJECTS
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(read_data()['projects'])

@app.route('/api/projects', methods=['POST'])
def add_project():
    data = read_data()
    project = request.get_json()
    project['id'] = 'p_' + str(int(time.time() * 1000))
    data['projects'].insert(0, project)
    write_data(data)
    return jsonify(project), 201

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    data = read_data()
    for i, p in enumerate(data['projects']):
        if p['id'] == project_id:
            data['projects'][i].update(request.get_json())
            write_data(data)
            return jsonify(data['projects'][i])
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    data = read_data()
    data['projects'] = [p for p in data['projects'] if p['id'] != project_id]
    write_data(data)
    return jsonify({'ok': True})

# VIDEOS
@app.route('/api/videos', methods=['GET'])
def get_videos():
    return jsonify(read_data()['videos'])

@app.route('/api/videos', methods=['POST'])
def add_video():
    data = read_data()
    video = request.get_json()
    video['id'] = 'v_' + str(int(time.time() * 1000))
    data['videos'].insert(0, video)
    write_data(data)
    return jsonify(video), 201

@app.route('/api/videos/<video_id>', methods=['PUT'])
def update_video(video_id):
    data = read_data()
    for i, v in enumerate(data['videos']):
        if v['id'] == video_id:
            data['videos'][i].update(request.get_json())
            write_data(data)
            return jsonify(data['videos'][i])
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/videos/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    data = read_data()
    data['videos'] = [v for v in data['videos'] if v['id'] != video_id]
    write_data(data)
    return jsonify({'ok': True})

# Serve portfolio static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), path)

if __name__ == '__main__':
    print("\n🚀 Portfolio API running at http://localhost:5000")
    print("   GET    /api/data")
    print("   GET    /api/projects")
    print("   POST   /api/projects")
    print("   PUT    /api/projects/<id>")
    print("   DELETE /api/projects/<id>")
    print("   GET    /api/videos")
    print("   POST   /api/videos")
    print("   PUT    /api/videos/<id>")
    print("   DELETE /api/videos/<id>\n")
    app.run(debug=True, port=5000)
