import cv2
import numpy as np

# Charger l'image
image = cv2.imread('balise.jpg')

# Définir le facteur de réduction
scale_percent = 20  # Par exemple, réduire l'image de 20 %

# Calculer les nouvelles dimensions de l'image
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# Redimensionner l'image
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Convertir l'image en RVB
rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

# Définir les plages de couleur rouge en RVB
lower_red = np.array([0, 0, 100])
upper_red = np.array([100, 100, 255])

# Créer un masque pour les pixels rouges dans l'image
mask = cv2.inRange(rgb, lower_red, upper_red)

# Trouver les contours dans le masque
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrer les contours pour ne garder que ceux qui ressemblent à un rectangle
rectangles = []
for contour in contours:
    # Approximer le contour pour un polygone
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    # Si le polygone a 4 côtés, il est probablement un rectangle
    if len(approx) == 4:
        rectangles.append(approx)

# Dessiner les rectangles rouges sur l'image redimensionnée
for rectangle in rectangles:
    cv2.drawContours(resized, [rectangle], -1, (0, 0, 255), 2)

# Afficher l'image avec les rectangles rouges détectés
cv2.imshow('Rectangles rouges détectés', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
