import json
from flask import Flask, jsonify, request
import database as db
import base64
import facial_recognition as facial
import pathlib

from PIL import Image
from io import BytesIO


import os
import cv2



app = Flask(__name__)


# CONFIG
path = str(pathlib.Path().absolute()) + "/img/" # "C:/proyectos/diego_facial/img/" # your path



# ---------------------- REGISTRAR USUARIO  ---------------------- 
@app.route('/register_user', methods=['POST'])
def register_user():
  dataRecibida=json.loads(request.data)
  nombreUsuario = dataRecibida['name']
  imgName= path + nombreUsuario + ".jpg"
  
  saveBase64ToImage(dataRecibida['photo'], imgName) # se guarda de forma temporal, ya que despues se remplaza por la imagen de la cara
  misCaras = facial.obtenerCaras(imgName)
  facial.guardarCaraComoArchivo(imgName, misCaras, imgName)
  

  respRegistroUser = db.registerUser(nombreUsuario, imgName)
  return jsonify(respRegistroUser), 200


# ---------------------- VALIDAR USUARIO  ---------------------- 
@app.route('/validate_user', methods=['POST'])
def validate_user():
  dataRecibida=json.loads(request.data)
  
  nombreUsuario = dataRecibida['name']
  img = f"{nombreUsuario}_login.jpg"
  img_user = f"{nombreUsuario}.jpg"
  # imgName = path + img_user

  pathImgToValidate = path + img
  saveBase64ToImage(dataRecibida['photo'], pathImgToValidate)
  misCaras = facial.obtenerCaras(pathImgToValidate)
  facial.guardarCaraComoArchivo(pathImgToValidate, misCaras, path+img)


  res_db =db.getUser(nombreUsuario, path+img_user)
  print("lista de conincidencais",res_db)
  if(res_db["affected"]):
      my_files = os.listdir(path)
      print(my_files)
      if img_user in my_files:
          face_reg = cv2.imread(path + img_user, 0)
          face_log = cv2.imread(path + img, 0)
          comp = facial.orb_sim(face_reg, face_log)
          print(comp)
          # os.remove(img_user)
          # os.remove(img)
          if comp >= 0.94:
             return jsonify(comp), 200
          else:
              return jsonify(comp), 400
      
      else:
         return jsonify("¡Error! Usuario no encontrado"), 400
        
  else:
    return jsonify("¡Error! Usuario no encontrado, general"), 400


  




def saveBase64ToImage(base64Img, nombreImagen):
  bytes_decoded = base64.b64decode(base64Img)  
  img = Image.open(BytesIO(bytes_decoded))
  out_jpg = img.convert("RGB")  
  out_jpg.save(nombreImagen)


app.run()


