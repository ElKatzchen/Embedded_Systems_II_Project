import cv2
import mediapipe as mp
import numpy as np
import serial as sl

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar VideoCapture
cap = cv2.VideoCapture(0)

# Inicializar conexión serial
ser = sl.Serial("/dev/ttyACM0", 9600)
ser.reset_input_buffer()

def get_direction(landmarks, image_shape, threshold=20):
    h, w, _ = image_shape
    
    # Extraer puntos clave relevantes
    nose_tip = landmarks[1]
    left_eye_inner = landmarks[133]
    right_eye_inner = landmarks[362]

    # Convertir coordenadas normalizadas a coordenadas de imagen
    nose_tip_coords = (int(nose_tip.x * w), int(nose_tip.y * h))
    left_eye_coords = (int(left_eye_inner.x * w), int(left_eye_inner.y * h))
    right_eye_coords = (int(right_eye_inner.x * w), int(right_eye_inner.y * h))

    # Calcular el centro de los ojos
    eye_center_x = (left_eye_coords[0] + right_eye_coords[0]) // 2
    eye_center_y = (left_eye_coords[1] + right_eye_coords[1]) // 2

    # Calcular desplazamiento de la nariz desde el centro de los ojos
    dx = nose_tip_coords[0] - eye_center_x
    dy = nose_tip_coords[1] - eye_center_y

    # Determinar la dirección basado en el desplazamiento
    if dx > threshold:
        return "Izquierda", 4
    elif dx < -threshold:
        return "Derecha", 3
    elif dy > threshold + 50:
        return "Abajo", 1
    elif dy < -threshold + 50:
        return "Arriba", 2
    else:
        return "Frente", 5

last_value = None

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convertir la imagen a RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe Face Mesh
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            direction, value = get_direction(landmarks, image.shape)
            
            if value != last_value:
                print(value)
                # Enviar el valor por UART solo si ha cambiado
                ser.write(bytearray(f"{value}\n", encoding='utf-8'))
                last_value = value
            
            # Mostrar la dirección en la imagen
            cv2.putText(image, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Dibujar los puntos clave grandes en la imagen
            keypoints = [landmarks[1], landmarks[133], landmarks[362]]  # Nariz y ojos internos
            for landmark in keypoints:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    # Mostrar la imagen
    cv2.imshow('MediaPipe Face Mesh', image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
