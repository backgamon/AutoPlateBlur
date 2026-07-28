import cv2
import numpy as np
import onnxruntime as ort


class PlateDetector:

    def __init__(self, model_path, confidence=0.35):

        self.confidence = confidence

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

        print(
            "Input :",
            self.session.get_inputs()[0].shape
        )

        print(
            "Output(s) :"
        )

        for out in self.session.get_outputs():

            print(
                out.name,
                out.shape,
                out.type
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


        result = self.session.run(
            None,
            {
                self.input_name: img
            }
        )


        print(
            "SORTIE MODELE :",
            result[0].shape
        )


        # Pas de détection pour l'instant
        # On veut uniquement connaître le format

        return []
