# flask_testing/test_base.py
from flask_testing import TestCase

class BaseTestCase(TestCase):
	"""A base test case for flask-tracking."""
	SQLALCHEMY_DATABASE_URI = "postgresql://"
	TESTING = True

	def create_app(self):
		app = Flask(__name__)
		app.config.from_object('config.TestConfiguration')
		app.config['TESTING'] = True
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


