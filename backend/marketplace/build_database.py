import marketplace.models as models
import marketplace.server as server

app = server.init_flask_app()

with app.app_context():
    models.db.init_app(app)
    models.db.create_all()
