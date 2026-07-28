import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import sys

from detector import PlateDetector
from video import process_video



class AutoPlateBlur:


    def __init__(self, root):

        self.root=root

        root.title(
            "AutoPlateBlur V2.1"
        )

        root.geometry(
            "550x300"
        )

        self.video=None


        self.label=tk.Label(
            root,
            text="Choisir vidéo"
        )

        self.label.pack(
            pady=20
        )


        tk.Button(
            root,
            text="Choisir",
            command=self.choose
        ).pack()


        self.status=tk.Label(
            root,
            text="Attente"
        )

        self.status.pack(
            pady=20
        )


        tk.Button(
            root,
            text="Analyser",
            command=self.start
        ).pack()



    def choose(self):

        self.video=filedialog.askopenfilename(
            filetypes=[
                ("Video","*.mp4 *.mov")
            ]
        )

        if self.video:

            self.label.config(
                text=os.path.basename(
                    self.video
                )
            )



    def start(self):

        if not self.video:

            messagebox.showwarning(
                "Erreur",
                "Choisir une vidéo"
            )

            return


        threading.Thread(
            target=self.run,
            daemon=True
        ).start()



    def run(self):

        if getattr(sys,"frozen",False):

            base=sys._MEIPASS

        else:

            base=os.path.dirname(
                os.path.abspath(__file__)
            )


        model=os.path.join(
            base,
            "models",
            "plate.onnx"
        )


        detector=PlateDetector(
            model
        )


        output=self.video.replace(
            ".mp4",
            "_detect.mp4"
        )


        process_video(
            self.video,
            output,
            detector,
            self.progress
        )


        self.status.config(
            text="Terminé : "+output
        )



    def progress(
        self,
        current,
        total
    ):

        self.status.config(
            text=f"{current}/{total}"
        )




if __name__=="__main__":

    root=tk.Tk()

    app=AutoPlateBlur(
        root
    )

    root.mainloop()
