
import cv2


def process_video(
        input_file,
        output_file,
        detector,
        callback=None):


    cap = cv2.VideoCapture(
        input_file
    )


    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )


    writer = cv2.VideoWriter(
        output_file,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width,height)
    )


    total = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    count = 0


    while True:

        ret, frame = cap.read()

        if not ret:
            break


        boxes = detector.detect(
            frame
        )


        for box in boxes:

            x1,y1,x2,y2 = box

            cv2.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                (0,0,255),
                3
            )


        writer.write(
            frame
        )


        count += 1


        if callback:

            callback(
                count,
                total
            )


    cap.release()
    writer.release()
