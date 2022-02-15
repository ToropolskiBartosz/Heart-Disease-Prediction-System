from app import creat_app, db
from flask_migrate import Migrate

app = creat_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)