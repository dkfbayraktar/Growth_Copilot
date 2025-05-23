from flask import Flask, jsonify, send_file, abort, make_response, request
import os
import json
import io
import pandas as pd
import numpy as np
import faiss

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'Data')
VECTORS_DIR = os.path.join(os.path.dirname(__file__), 'Vectors')
INDEX_PATH = os.path.join(VECTORS_DIR, 'faiss_index.bin')

# Dummy embedding fonksiyonu (gerçek embedding için OpenAI API entegrasyonu eklenecek)
def get_embedding(text):
    np.random.seed(abs(hash(text)) % (10 ** 8))
    return np.random.rand(512).astype('float32')

@app.route('/')
def home():
    return 'Growth Copilot API is running!'

@app.route('/data/<filename>')
def get_data(filename):
    if not filename.endswith('.json'):
        filename += '.json'
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        abort(404, description='Data file not found')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/export-excel/<filename>')
def export_excel(filename):
    if not filename.endswith('.json'):
        filename += '.json'
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        abort(404, description='Data file not found')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    # Dinamik dosya adı
    custom_filename = request.args.get('filename')
    if not custom_filename:
        # filename parametresinden .json uzantısını çıkarıp .xlsx ekle
        custom_filename = filename.replace('.json', '') + '.xlsx'
    else:
        # Kullanıcı verdiği ismin sonuna .xlsx ekle (varsa tekrar eklenmesin)
        if not custom_filename.lower().endswith('.xlsx'):
            custom_filename += '.xlsx'
    response = make_response(output.read())
    response.headers['Content-Disposition'] = f'attachment; filename={custom_filename}'
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return response

@app.route('/search-vector', methods=['POST'])
def search_vector():
    data = request.get_json()
    query = data.get('query')
    top_k = int(data.get('top_k', 3))
    if not query:
        return jsonify({'error': 'query parametresi zorunlu'}), 400
    if not os.path.exists(INDEX_PATH):
        return jsonify({'error': 'FAISS index bulunamadı'}), 500
    # Embedding oluştur
    query_emb = get_embedding(query).reshape(1, -1)
    # FAISS indexi yükle
    index = faiss.read_index(INDEX_PATH)
    D, I = index.search(query_emb, top_k)
    # Tüm blokları yükle
    blocks = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.json'):
            with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                for item in json_data:
                    text = ' '.join([f"{k}: {v}" for k, v in item.items()])
                    blocks.append(text)
    results = []
    for idx in I[0]:
        if 0 <= idx < len(blocks):
            results.append(blocks[idx])
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True) 