import tkinter
import tkinter.messagebox
import customtkinter
from pytubefix import *
from pydub import AudioSegment
import os

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

typeToConvert = "mp4"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("YTGreen Downloader")
        self.geometry(f"{720}x{480}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="YTGreen Downloader", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.quality_download_label = customtkinter.CTkLabel(self.sidebar_frame, text="Quality to Download:", anchor="w")
        self.quality_download_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.quality_download_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["High", "Medium", "Low"],
                                                                        command=lambda x: print("Quality:", x))
        self.quality_download_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        self.folder_to_download_entry_env = customtkinter.StringVar(value="./")
        self.folder_to_download_label = customtkinter.CTkLabel(self.sidebar_frame, text="Folder to Download:", anchor="w")
        self.folder_to_download_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.folder_to_download_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Write the folder path here", textvariable=self.folder_to_download_entry_env)
        self.folder_to_download_entry.grid(row=4, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #progressbar
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progress_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Download Progress ", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.progress_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.error_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="", font=customtkinter.CTkFont(size=10, weight="bold"), text_color="red")
        self.error_label.grid(row=3, column=0, padx=10, pady=(10, 10))
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="YouTube URL")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Download", command=self.download)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Type of download:")
        self.label_radio_group.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0, text="Unique")
        self.radio_button_1.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1, text="Playlist")
        self.radio_button_2.grid(row=2, column=1, pady=10, padx=20, sticky="n")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Configurantions")
        self.scrollable_frame.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        
        self.switchMP3env = customtkinter.StringVar(value="off")
        self.switchMP3 = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Convert to .MP3", variable=self.switchMP3env, command=self.change_type_convert, onvalue="on", offvalue="off")
        self.switchMP3.grid(row=0, column=0, padx=10, pady=(0, 20))   
        self.scrollable_frame_switches.append(self.switchMP3)

        self.switchMP4env = customtkinter.StringVar(value="off")
        self.switchMP4 = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Convert to .MP4", command=self.change_type_convert, variable=self.switchMP4env, onvalue="on", offvalue="off")
        self.switchMP4.grid(row=1, column=0, padx=10, pady=(0, 20))   
        self.scrollable_frame_switches.append(self.switchMP4)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def change_type_convert(self):
        if self.switchMP3env.get() == "on":
            self.switchMP4.deselect()
            typeToConvert = "mp3"
        elif self.switchMP4env.get() == "on":
            self.switchMP3.deselect()
            typeToConvert = "mp4"
        else:
            typeToConvert = "none"

        print(typeToConvert)
    
    def download(self):
        
        try:
            print(self.folder_to_download_entry_env.get())
            print(self.radio_var.get())
            self.check_and_create_path(self.folder_to_download_entry_env.get())
            if self.radio_var.get() == 0:
                print(self.entry.get())
                yt = YouTube(self.entry.get())
                ys = yt.streams.get_highest_resolution()
                ys.download(self.folder_to_download_entry_env.get())
                print(typeToConvert)
                if typeToConvert == "mp3":
                    self.convert_to_mp3(self.folder_to_download_entry_env.get())
            else:
                print(self.entry.get())
                ytPlaylist = Playlist(self.entry.get())
                for video in ytPlaylist.videos:
                    ys = video.streams.get_highest_resolution()
                    ys.download(self.folder_to_download_entry_env.get())
                print(self.switchMP3env.get())
                if self.switchMP3env.get() == "on":
                    print("Convertendo para mp3")
                    self.convert_to_mp3(self.folder_to_download_entry_env.get())
        except Exception as e:
            print(e)
            self.error_label.configure(text="Error: "+str(e))

    def check_and_create_path(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Pasta criada: {path}")
            except OSError as e:
                print(f"Erro ao criar a pasta: {e}")
                return False
        return True
    
    def convert_to_mp3(self, path):
        for file_name in os.listdir(path):
            if file_name.endswith(".m4a") or file_name.endswith(".webm"):
                file_path = os.path.join(path, file_name)
                audio = AudioSegment.from_file(file_path)
                mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
                audio.export(mp3_file_path, format="mp3")
                os.remove(file_path)
    
if __name__ == "__main__":
    app = App()
    app.mainloop()