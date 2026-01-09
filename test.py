import cv2
import easyocr
from ultralytics import YOLO

# 1. Carrega o novo modelo de área única e o leitor OCR
model = YOLO('/models/model-plates.pt')  # Certifique-se que o best.pt está na pasta
reader = easyocr.Reader(['pt'], gpu=False) #

# 2. Inicializa a Webcam
cap = cv2.VideoCapture(0)

print("--- Iniciando Teste de Reconhecimento ---")
print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Detecta a placa
    # conf=0.5 ajuda a evitar falsos positivos
    results = model(frame, conf=0.5, verbose=False)

    for r in results:
        for box in r.boxes:
            # Coordenadas do retângulo
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            
            # Recorta a placa com uma pequena margem (padding)
            recorte = frame[max(0, y1-10):y2+10, max(0, x1-10):x2+10]
            
            if recorte.size > 0:
                # 4. Tenta ler o texto da placa
                # detail=0 retorna apenas a string de texto
                resultado_ocr = reader.readtext(recorte, detail=0)
                
                if resultado_ocr:
                    texto = "".join(resultado_ocr).replace(" ", "").upper()
                    print(f"PLACA DETECTADA: {texto}")
                    
                    # Desenha o texto na tela acima do retângulo
                    cv2.putText(frame, texto, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Desenha o retângulo da placa
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Exibe o vídeo
    cv2.imshow("Teste Simples LPR", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()