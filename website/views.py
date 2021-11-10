# import dependencies
from flask import Blueprint, render_template, request, flash, jsonify
from flask.json import jsonify
from flask_login import login_required, current_user
from .models import Notes
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('comment too small', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note added.', category='success')




    return render_template("home.html", users=current_user)

# having difficulties with this for now, will troubleshoot tmrw

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Notes.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(noteId)
#             db.session.commit()
#             print(note)
#             print(noteId)
            
#     return jsonify({})
