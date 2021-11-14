# import dependencies
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Comments
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home')
#@login_required
def home():
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('comment too small', category='error')
    #     else:
    #         new_note = Comments(content=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('comment added.', category='success')




    return render_template("home.html", users=current_user)