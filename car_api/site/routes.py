from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

"""
In above code, some arguments are specified when creating the Blueprint object. This first
argument 'site' is the blueprint's name, which will be used by flask's routing
mechanism. The second parameter, __name__, is the blueprint's import name, which flask uses 
to locate resources
"""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')