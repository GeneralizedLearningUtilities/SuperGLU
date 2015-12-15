from flask import (
    Blueprint,
    g,
    request,
    url_for,
    Response,
    redirect,
    flash,
	render_template,
    abort,
    Flask
)

from SuperGLU.Util.ErrorHandling import logError, logWarning


indexPrint = Blueprint('index', __name__)

@indexPrint.route('/')
def index():
	return render_template('ParentPage.html')
    

childPrint = Blueprint('ChildWindow.html', __name__)

@childPrint.route('/ChildWindow.html')
def child():
    return render_template('ChildWindow.html')

javascriptPrint = Blueprint('<path:path>', __name__)
javascriptPrint.static_folder = 'static'
    
@javascriptPrint.route('/js/<path:path>')
def javascript_imports(path):
    if path[-3:] == '.js':
        try:
            return javascriptPrint.send_static_file(path)
        except Exception as e:
            logWarning('exception=')
            logWarning(e)
            logWarning(path)
            abort(404)
    else:
        return abort(404)
