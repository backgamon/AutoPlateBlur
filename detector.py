import cv2
import numpy as np
import onnxruntime as ort


class PlateDetector:

    def __init__(self, model_path, confidence=0.35):

        self.confidence = confidence


        # GPU si disponible sinon CPU
        providers = [
            "CUDAExecutionProvider",
            "CPUExecutionProvider"
        ]


        self.session = ort.InferenceSession(
            model_path,
            providers=providers
        )


        self.input_name = self.session.get_inputs()[0].name


        print("===== MODELE ONNX =====")
        print("Input :", self.session.get_inputs()[0].shape)

        for out in self.session.get_outputs():

            print(
                "Output :",
                out.name,
                out.shape
            )

        print("=======================")



    def detect(self, frame):

        h, w = frame.shape[:2]


        img = cv2.resize(
            frame,
            (640,640)
        )


        img = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )


        img = img.astype(
            np.float32
        ) / 255.0


        img = np.transpose(
            img,
            (2,0,1)
        )


        img = np.expand_dims(
            img,
            axis=0
        )


        output = self.session.run(
            None,
            {
                self.input_name: img
            }
        )[0]


        # YOLO : (1,5,8400)
        output = output[0]


        # passage en (8400,5)
        output = output.transpose(1,0)


        boxes = []


        for det in output:

            x,y,bw,bh,score = det


            if score < self.confidence:
                continue


            # conversion 640 -> image originale

            x1 = int(
                (x - bw/2) * w / 640
            )

            y1 = int(
                (y - bh/2) * h / 640
            )

            x2 = int(
                (x + bw/2) * w / 640
            )

            y2 = int(
                (y + bh/2) * h / 640
            )


            # sécurité image

            x1=max(0,x1)
            y1=max(0,y1)
            x2=min(w,x2)
            y2=min(h,y2)


            boxes.append(
                (
                    x1,
                    y1,
                    x2,
                    y2,
                    float(score)
                )
            )


        return boxes
