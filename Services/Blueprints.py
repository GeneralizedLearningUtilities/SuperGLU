from flask import (
    Blueprint,
    g,
    request,
    url_for,
    Response,
    redirect,
    flash,
	render_template
)

indexPrint = Blueprint('index', __name__)

@indexPrint.route('/')
def index():
	return render_template('index.html')