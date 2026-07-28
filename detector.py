import os
import sys
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


    def detect(self, frame):

        h, w = frame.shape[:2]

        img = cv2.resize(
            frame,
            (640, 640)
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


        boxes = []


        # format YOLO standard
        output = result[0][0]


        for det in output:

            score = det[4]

            if score < self.confidence:
                continue


            x1 = int(det[0] * w / 640)
            y1 = int(det[1] * h / 640)
            x2 = int(det[2] * w / 640)
            y2 = int(det[3] * h / 640)


            boxes.append(
                (
                    x1,
                    y1,
                    x2,
                    y2
                )
            )


        return boxes
