import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import sys


class AutoPlateBlur:

    def __init__(self, root):

        self.root = root
        root.title("AutoPlateBlur V1")
        root.geometry("500x250")

        self.video = None

        self.label = tk.Label(
            root,
            text="Choisir une vidéo MP4/MOV",
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
                ("Vidéos", "*.mp4 *.mov *.mkv")
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



        # Gestion chemin PyInstaller
        if getattr(sys, "frozen", False):

            base = sys._MEIPASS

        else:

            base = os.path.dirname(
                os.path.abspath(__file__)
            )


        ffmpeg = os.path.join(
            base,
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

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )


            if result.returncode == 0:

                self.progress.config(
                    text="Terminé :\n" + output
                )


            else:

                error = result.stderr.decode(
                    errors="ignore"
                )

                self.progress.config(
                    text="Erreur FFmpeg"
                )

                messagebox.showerror(
                    "FFmpeg",
                    error[-1000:]
                )



        except Exception as e:

            self.progress.config(
                text="Erreur"
            )

            messagebox.showerror(
                "Erreur",
                str(e)
            )





if __name__ == "__main__":

    root = tk.Tk()

    app = AutoPlateBlur(root)

    root.mainloop()
