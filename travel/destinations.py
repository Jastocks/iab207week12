from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

#Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
destbp = Blueprint('destination', __name__, url_prefix = '/destinations')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    cform = CommentForm()
    print('filepath from db: '+ destination.image)
    return render_template('destinations/show.html', destination = destination, form=cform)

@destbp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    destination = Destination(name=form.name.data,
                              description=form.description.data,
                              image=db_file_path,
                              currency=form.currency.data)
    #add object
    db.session.add(destination)
    #commit
    db.session.commit()
    print('Successfully created new travel destination')
    print('uploaded file: '+ db_file_path)
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

@destbp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
  form = CommentForm()
  destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
  if form.validate_on_submit():	#this is true only in case of POST method
    comment = Comment(text=form.text.data, destination=destination, user=current_user)
    db.session.add(comment)
    db.session.commit()
    print('Your comment has been added', 'success')
  # notice the signature of url_for
  return redirect(url_for('destination.show', id=id))


def get_destination():
  # creating the description of Brazil
  b_desc = """Brazil is considered an advanced emerging economy.
   It has the ninth largest GDP in the world by nominal, and eight by PPP measures. 
   It is one of the world\'s major breadbaskets, being the largest producer of coffee for the last 150 years."""
   # an image location
  image_loc = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFyC8pBJI2AAHLpAVih41_yWx2xxLleTtdshAdk1HOZQd9ZM8-Ag'
  destination = Destination('Brazil', b_desc,image_loc, 'R$10')
  # a comment
  comment = Comment("Sam", "Visited during the olympics, was great", '2023-08-12 11:00:00')
  destination.set_comments(comment)
  comment = Comment("Bill", "free food!", '2023-08-12 11:00:00')
  destination.set_comments(comment)
  comment = Comment("Sally", "free face masks!", '2023-08-12 11:00:00')
  destination.set_comments(comment)
  return destination

def check_upload_file(form):
  #get file data from form
  fp = form.image.data
  filename = fp.filename
  #get current path
  BASE_PATH = os.path.dirname(__file__)
  #upload file location
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in html is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path
