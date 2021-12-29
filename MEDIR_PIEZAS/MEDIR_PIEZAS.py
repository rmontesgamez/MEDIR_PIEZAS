import opencv as cv
import numpy as np
from scipy.spatial import distance as dist
# Definir el cálculo de coordenadas del punto medio
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
def measure(img):
         # A escala de grises
	gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
	 # Imagen binaria
	ret, thresh = cv.threshold(gray, 127, 255, 0)
	 # Calcula las coordenadas de las 4 esquinas del cuadrado negro
	contours, hierarchy = cv.findContours(thresh, 1, 2)
	for cnt in contours:
	 # Encuentra la distancia geométrica del contorno
	  	M = cv.moments(cnt)
    	     # Obtenga el rectángulo circunscrito del contorno, x, y son las coordenadas de píxeles de la esquina superior izquierda del marco verde, w, h son la longitud y el ancho del marco verde
    	x, y, w, h = cv.boundingRect(cnt)
    	     # Calcule el contorno mínimo, cuadro rojo
    	rect = cv.minAreaRect(cnt)
    	     # Calcula las coordenadas de la imagen de las 4 esquinas del cuadro rojo
    	box = cv.boxPoints(rect)
    	     # El número de la imagen es un número entero, así que convierta las coordenadas en un número entero
    	box = np.int0(box)


    	if M['m00'] != 0:
        	# print(M)
        	cx = int(M['m10'] / M['m00'])
        	cy = int(M['m01'] / M['m00'])
        	         #Según el punto central obtenido por la distancia geométrica, dibuje el círculo central, que está bloqueado por la línea azul, por lo que no se puede ver
        	cv.circle(image,(np.int(cx),np.int(cy)),2,(0,255,255),-1) 
        	         #     Marco
        	cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        	         #Pintando cuadro rojo 4 esquinas
        	cv.drawContours(img, [box], 0, (0, 0, 255), 2)
        	for (x, y) in box:
                cv.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            	             # tl coordenadas del número de la imagen de la esquina superior izquierda, tr coordenadas del número de la imagen de la esquina superior derecha, br coordenadas del número de la imagen de la esquina inferior derecha, bl coordenadas del número de la imagen de la esquina inferior izquierda
            	(tl, tr, br, bl) = box
            	             # Calcule los puntos centrales de los 4 lados del cuadro rojo
            	(tltrX, tltrY) = midpoint(tl, tr)
            	(blbrX, blbrY) = midpoint(bl, br)
            	(tlblX, tlblY) = midpoint(tl, bl)
            	(trbrX, trbrY) = midpoint(tr, br)
            	             # Dibuja algunos
            	cv2.circle(img, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            	cv2.circle(img, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            	cv2.circle(img, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            	cv2.circle(img, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
            	             # Dibuja una línea para conectar 4 puntos, es decir, 2 líneas azules en la imagen.

            	cv2.line(img, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                     (255, 0, 0), 2)
            	cv2.line(img, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                     (255, 0, 0), 2)
                                 # Calcula las coordenadas del punto central
            	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            	             # Convierta la longitud del número de imagen a la longitud real, 6.5 equivale a la escala, yo uso la unidad mm, es decir, 1 mm equivale a 6.5 imágenes

            	dimA = dA / 6.5
            	dimB = dB / 6.5
            	             # Imprima el resultado del cálculo en la imagen original, que es el contenido amarillo

            	cv.putText(img, "{:.1f}mm".format(dimA),
                        (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 255, 255), 2)
            	cv.putText(img, "{:.1f}mm".format(dimB),
                        (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 255, 255), 2)
	cv.imshow("mo", img)
 # Enciende la cámara, configura la resolución
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
while(cap.isOpened()):
	ret, frame = cap.read()
	img = cv2.flip(frame, -1)
	 #Cree una ventana GUI en forma de adaptación
	cv.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
	 #Conecta la imagen a la ventana por nombre
	cv.imshow("input image", img)
	measure(img)
	 # Si presiona la tecla P, la imagen se guardará en D: / Archivos de programa / kk.jpg y saldrá
	if cv.waitKey(1) & 0xFF == ord('p'):
        cv.imwrite("D:/Program Files/kk.jpg", img)
    	break

