from flask import Blueprint, jsonify

content_bp = Blueprint('content', __name__)

# GET /api/content — get all movies and shows
@content_bp.route('/', methods=['GET'])
def get_all_content():
    try:
        from app import db
        result = db.session.execute(
            db.text('SELECT * FROM content ORDER BY rating DESC')
        )
        rows = result.fetchall()
        content_list = []
        for row in rows:
            content_list.append({
                'id': row.id,
                'title': row.title,
                'description': row.description,
                'genre': row.genre,
                'release_year': row.release_year,
                'rating': float(row.rating) if row.rating else None
            })
        return jsonify(content_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# GET /api/content/<id> — get single item
@content_bp.route('/<int:content_id>', methods=['GET'])
def get_content(content_id):
    try:
        from app import db
        row = db.session.execute(
            db.text('SELECT * FROM content WHERE id = :id'),
            {'id': content_id}
        ).fetchone()
        if not row:
            return jsonify({'error': 'Not found'}), 404
        return jsonify({
            'id': row.id,
            'title': row.title,
            'description': row.description,
            'genre': row.genre,
            'release_year': row.release_year,
            'rating': float(row.rating) if row.rating else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500