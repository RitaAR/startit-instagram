from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
import os
from modules import picmethods, commethods
app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def root():
  #Attēli ir linki uz pixabay attēliem; attēlu saraksts atrodas static/pictures.bin
  #Ja tiek pievienots jauns attēls
  if request.method == 'POST':
    newPicture = request.form['newPicture']
    pictureExistsAlready = picmethods.checkIfPictureExists(newPicture)
    if pictureExistsAlready:
      print('Duplicate picture error.')
    else:
      picmethods.addNewPicture(newPicture)
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures)
  #Ja lapa tiek vienkārši ielādēta
  else:
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures,comments=commethods.findCommentCount)

@app.route('/bildes',methods = ['POST', 'GET'])
def visasBildes():
  #Ja tiek pievienots jauns attēls
  if request.method == 'POST':
    newPicture = request.form['newPicture']
    pictureExistsAlready = picmethods.checkIfPictureExists(newPicture)
    if pictureExistsAlready:
      print('Duplicate picture error.')
    else:
      picmethods.addNewPicture(newPicture)
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures)
  #Ja lapa tiek vienkārši ielādēta
  else:
    pictures = picmethods.loadAllPictures()
    return render_template("bildes.html", pictures=pictures)

@app.route('/bilde',methods = ['POST', 'GET'])
def bilde():
  pictureName = request.args.get('picture')
  pictureID = picmethods.findPictureIdByName(pictureName)
  #Ja tiek pievienots jauns komentārs no formas
  if request.method == 'POST':
    comments = commethods.searchAllComments(pictureID)
    newComment = request.form['newComment']
    commethods.addNewComment(pictureID,newComment)
    return render_template(
    "bilde.html", picture = pictureName,comm = comments)
  #Ja lapa tiek vienkārši ielādēta
  else:
    comments = commethods.searchAllComments(pictureID)
    return render_template(
    "bilde.html", picture = pictureName,comm = comments
  )

@app.route('/komentari/<komentaraID>')
def komentars(komentaraID):
  atrastaisKomentars = ""
  try:
    fp = open('komentari.txt')
    line = fp.readline()
    cnt = 0
    while line:
      print("cnt: {}, komentaraID: {}".format(cnt, komentaraID))
      if cnt == int(komentaraID):
        print("Line {}: {}".format(cnt, line.strip()))
        atrastaisKomentars = line
      line = fp.readline()
      cnt += 1
  finally:
    fp.close()
  return render_template('komentars.html', komentars = atrastaisKomentars)

@app.route('/mainit',methods = ['POST', 'GET'])
#Dzeesh, maina pret citu komentaru
def del_komentars():
  pictureID = "2"  # jaasanejem no lapas
  oldComID = "1"   # jasanjem no lapas, ja "", tad dzesh visus vildes komentarus
  newComment = "Rūķis viens pats"  # jasanjem no lapas, ja "xxx", tad ar sho nomaina veco, ja "", tad dzesh esosho komentaru
  commethods.deleteComment(pictureID,oldComID,newComment)
  return "OK"


@app.route('/health')
def health():
  return "OK"

if __name__ == '__main__':
  app.run()
