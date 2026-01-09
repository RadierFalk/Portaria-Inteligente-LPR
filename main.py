import cv2
import easyocr
import threading
import re
from ultralytics import YOLO
import database 


MODEL_PATH = 'model-plates.pt' 
CONF_THRESHOLD = 0.5   
PADDING = 15

database.init_db()
yolo = YOLO(MODEL_PATH)
reader = easyocr.Reader(['pt'], gpu=False)

class ControladorPortaria:
    def __init__(self):
        self.placa_atual = ""
        self.status = "SISTEMA ATIVO"
        self.ocupado = False

    def validar_placa(self, texto):
        # Regex para Mercosul (ABC1D23) ou Antiga (ABC1234)
        padrao = re.compile(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}')
        return padrao.match(texto)

    def processar_ia(self, corte):
        self.ocupado = True
        try:
            
            resultados = reader.readtext(corte, detail=0)
            
            texto_bruto = "".join(resultados).upper()
            texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_bruto)
            
            if len(texto_limpo) >= 7:
                
                for i in range(len(texto_limpo) - 6):
                    candidato = list(texto_limpo[i:i+7])
                    
                    for j in range(3):
                        if candidato[j] == '0': candidato[j] = 'O'
                        if candidato[j] == '1': candidato[j] = 'I'
                    
                    placa_final = "".join(candidato)
                    
                    if self.validar_placa(placa_final):
                        self.placa_atual = placa_final
                        nome = database.verificar_placa(placa_final)
                        
                        if nome:
                            self.status = f"LIBERADO: {nome}"
                            print(f">>> {placa_final} - {nome} <<<")
                        else:
                            self.status = f"BLOQUEADO: {placa_final}"
                        return # Sucesso!
            
            if self.status == "SISTEMA ATIVO":
                self.status = "AGUARDANDO..."

        except Exception as e:
            print(f"Erro no OCR: {e}")
        finally:
            self.ocupado = False


controle = ControladorPortaria()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    
    results = yolo(frame, conf=CONF_THRESHOLD, verbose=False)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            
            
            h, w, _ = frame.shape
            x1_p, y1_p = max(0, x1 - PADDING), max(0, y1 - PADDING)
            x2_p, y2_p = min(w, x2 + PADDING), min(h, y2 + PADDING)

            
            cor = (0, 255, 0) if "LIBERADO" in controle.status else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)

            if not controle.ocupado:
                recorte = frame[y1_p:y2_p, x1_p:x2_p]
                if recorte.size > 0:
                    threading.Thread(target=controle.processar_ia, args=(recorte,), daemon=True).start()

    cv2.rectangle(frame, (0, 0), (500, 90), (0, 0, 0), -1)
    cv2.putText(frame, f"PLACA: {controle.placa_atual}", (10, 35), 1, 1.8, (255, 255, 255), 2)
    cv2.putText(frame, controle.status, (10, 75), 1, 1.4, (0, 255, 255), 2)

    cv2.imshow("Portaria LPR - Modelo Area Unica", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()