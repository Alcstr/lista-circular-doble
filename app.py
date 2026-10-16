from flask import Flask, jsonify, request, render_template

# Use relative imports for package modules
from .catalog import initialize_catalog
from .content import Content

app = Flask(__name__, template_folder='templates', static_folder='static')

# Global catalog instance
catalog = initialize_catalog()

def serialize_content(item: Content) -> dict:
    return item.to_dict()

@app.route('/')
def index():
    return render_template('index.html')

# API endpoints
@app.route('/api/catalog', methods=['GET'])
def get_catalog():
    items = [serialize_content(item) for item in catalog.traverse_forward()]
    current = serialize_content(catalog.get_current()) if catalog.get_current() else None
    return jsonify({
        'items': items,
        'current': current,
        'size': len(catalog)
    })

@app.route('/api/current', methods=['GET'])
def get_current():
    curr = catalog.get_current()
    if not curr:
        return jsonify({'message': 'Catalog is empty'}), 404
    return jsonify(serialize_content(curr))

@app.route('/api/next', methods=['POST'])
def next_item():
    item = catalog.next_item()
    if not item:
        return jsonify({'message': 'Catalog is empty'}), 404
    return jsonify(serialize_content(item))

@app.route('/api/previous', methods=['POST'])
def previous_item():
    item = catalog.previous_item()
    if not item:
        return jsonify({'message': 'Catalog is empty'}), 404
    return jsonify(serialize_content(item))

@app.route('/api/select/<string:content_id>', methods=['POST'])
def select_item(content_id):
    item = catalog.select(content_id)
    if not item:
        return jsonify({'error': f'Content id {content_id} not found'}), 404
    return jsonify(serialize_content(item))

@app.route('/api/content/<string:content_id>', methods=['GET'])
def get_content(content_id):
    node = catalog.find(content_id)
    if not node:
        return jsonify({'error': f'Content id {content_id} not found'}), 404
    return jsonify(serialize_content(node.data))

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'error': 'Query parameter "q" required'}), 400
    results = []
    node = catalog.head
    if node:
        for _ in range(len(catalog)):
            if query in node.data.title.lower() or query in node.data.description.lower():
                results.append(serialize_content(node.data))
            node = node.next
    return jsonify({'results': results})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = set()
    node = catalog.head
    if node:
        for _ in range(len(catalog)):
            categories.add(node.data.category)
            node = node.next
    return jsonify(sorted(list(categories)))

@app.route('/api/category/<string:category>', methods=['GET'])
def get_by_category(category):
    matches = []
    node = catalog.head
    if node:
        for _ in range(len(catalog)):
            if node.data.category.lower() == category.lower():
                matches.append(serialize_content(node.data))
            node = node.next
    return jsonify({'items': matches})

@app.route('/api/reset', methods=['POST'])
def reset_catalog():
    global catalog
    catalog = initialize_catalog()
    return jsonify({'message': 'Catalog reset'}), 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'size': len(catalog),
        'current_id': catalog.get_current().id if catalog.get_current() else None
    })

@app.route('/api/validate', methods=['POST'])
def validate():
    result = catalog.validate_integrity()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
