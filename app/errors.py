from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('non existent url requested:' + str(error))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Internal error:' + str(error))
    db.session.rollback()
    return render_template('500.html'), 500