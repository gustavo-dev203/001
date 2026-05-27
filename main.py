from app import create_app
from app.db import db

# Chama a "Fábrica" que criámos no __init__.py
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)