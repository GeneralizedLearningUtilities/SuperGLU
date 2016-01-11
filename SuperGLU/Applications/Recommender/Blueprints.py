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


BASIC_BLUEPRINT = Blueprint('', __name__)
BASIC_BLUEPRINT.static_folder = 'static'

@BASIC_BLUEPRINT.route('/')
def index():
	return render_template('ParentPage.html')
  
@BASIC_BLUEPRINT.route('/ChildWindow.html')
def activityWindow():
    return render_template('ChildWindow.html')

@BASIC_BLUEPRINT.route('/LoggerWindow.html')
def loggingWindow():
    return render_template('LoggerWindow.html')
    
@BASIC_BLUEPRINT.route('/js/<path:path>')
def javascriptImports(path):
    if path[-3:] == '.js':
        try:
            return BASIC_BLUEPRINT.send_static_file(path)
        except Exception as e:
            logWarning('exception=')
            logWarning(e)
            logWarning(path)
            abort(404)
    else:
        return abort(404)
