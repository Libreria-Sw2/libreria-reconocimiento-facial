
# import os
import cv2
# from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import database as db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# CONFIG
path = "C:/proyectos/diego_facial/img/" # your path


# devuelve la lista de caras de la imagen
def obtenerCaras(img): 
    pixeles = plt.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    return caras

def guardarCaraComoArchivo(imgOriginal, listaDeCaras, ubicacionImgCara):
    data = plt.imread(imgOriginal)
    for i in range(len(listaDeCaras)):
        x1,y1,ancho, alto = listaDeCaras[i]['box']
        x2,y2 = x1 + ancho, y1 + alto
        plt.subplot(1, len(listaDeCaras), i+1)
        plt.axis('off')
        cara_reg = data[y1:y2, x1:x2]
        cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
        cv2.imwrite(ubicacionImgCara , cara_reg) # guardar como archivo
        plt.imshow(data[y1:y2, x1:x2])



def log_rostro(img, lista_resultados,usuario_login):
    # img = usuario_login+"LOG.jpg"
    pixeles = plt.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    data = plt.imread(img)
    for i in range(len(lista_resultados)):
        x1,y1,ancho, alto = lista_resultados[i]['box']
        x2,y2 = x1 + ancho, y1 + alto
        plt.subplot(1, len(lista_resultados), i+1)
        plt.axis('off')
        cara_reg = data[y1:y2, x1:x2]
        cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
        cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
        return plt.imshow(data[y1:y2, x1:x2])
    plt.show()
    

  #-------------------------- Funcion para comparar los rostros --------------------------------------------
def orb_sim(img1,img2):
    orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
    kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
    kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

    matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

    regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
    if len(matches) == 0:
        return 0
    return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
def orb_sim(img1,img2):
     orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
     kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
     kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

     comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

     matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

     regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
     if len(matches) == 0:
         return 0
     return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
     
# root = Tk()
# root.geometry(size_screen)
# root.title("AVM")
# root.configure(bg=color_background)
# Label(text="¡Bienvenido(a)!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

# getEnter(root)
# Button(text=txt_login, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()

# getEnter(root)
# Button(text=txt_register, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register).pack()

# root.mainloop()