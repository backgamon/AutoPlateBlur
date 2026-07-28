import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading


class AutoPlateBlur:
    def __init__(self, root):
        self.root = root
        root.title("AutoPlateBlur V1")
        root.geometry("500x250")

        self.video = None

        self.label = tk.Label(
            root,
            text="Dépose une vidéo MP4/MOV",
            font=("Arial", 14)
        )
        self.label.pack(pady=20)

        self.btn = tk.Button(
            root,
            text="Choisir une vidéo",
            command=self.choose
        )
        self.btn.pack()

        self.progress = tk.Label(
            root,
            text="Attente..."
        )
        self.progress.pack(pady=20)

        self.export = tk.Button(
            root,
            text="Exporter",
            command=self.start
        )
        self.export.pack()


    def choose(self):

        file = filedialog.askopenfilename(
            filetypes=[
                ("Video", "*.mp4 *.mov *.mkv")
            ]
        )

        if file:
            self.video = file
            self.label.config(
                text=os.path.basename(file)
            )


    def start(self):

        if not self.video:
            messagebox.showwarning(
                "Erreur",
                "Choisis une vidéo"
            )
            return

        thread = threading.Thread(
            target=self.convert
        )

        thread.start()


    def convert(self):

        output = os.path.splitext(
            self.video
        )[0] + "_test.mp4"


        ffmpeg = os.path.join(
            "ffmpeg",
            "ffmpeg.exe"
        )

        cmd = [
            ffmpeg,
            "-i",
            self.video,
            "-c:v",
            "h264_nvenc",
            "-preset",
            "p5",
            "-c:a",
            "copy",
            output
        ]


        self.progress.config(
            text="Conversion en cours..."
        )


        try:

            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )


            self.progress.config(
                text="Terminé : " + output
            )


        except Exception as e:

            self.progress.config(
                text=str(e)
            )



root = tk.Tk()
app = AutoPlateBlur(root)
root.mainloop()
