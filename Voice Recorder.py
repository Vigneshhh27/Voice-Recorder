import pyaudio  # FOR RECORDING AUDIO
import wave  # FOR SAVING AUDIO
import tkinter
from tkinter import messagebox
import threading  #for unkown error handling
import os  # for saving recorded file on desktop


# file Parameters
stream = False
audio = False
FORMAT = pyaudio.paInt16  # determining audio parameters
CHANNELS = 1  # monoaudio
RATE = 44100  # or 16000 HZ
frms_per_buf = 1024
OUTPUT_FILENAME = "recordedFi1e.wav"
frames = []
# Creating audio & stream object using Pyaudio lib
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=frms_per_buf)

rec_start_label=0


#Start Recording
def Start_Rec():
    global rec_label ,stream ,audio ,frames,rec_start_label
    print("Recording Started!")
    rec_start_label = 1
    rec_label = True

    def record():
        while rec_label:
            data = stream.read(frms_per_buf)  # reading data
            frames.append(data)  # read data from signal is converted to list

    threading.Thread(target=record).start()


#Stop Recording
def Stop_Rec():
    global rec_label , stream ,audio,rec_start_label
    rec_label = False
    if rec_start_label==0:
        messagebox.showerror("Error", "No Recording has Started")
        return
    if rec_start_label==1:
        if (not(stream)):
            messagebox.showerror("Error", "No Recording has Started")
            return
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Recording Stopped!")


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_name=os.path.join(desktop_path, "Vignesh_audio_rec.wav")

#Saving Recording as Wave File
def Save_Rec():
    if(not(frames)):
        messagebox.showerror("Error", "No Recording to Save")
        return
    try:
        obj = wave.open(file_name, "wb")
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(audio.get_sample_size(FORMAT))
        obj.setframerate(RATE)
        obj.writeframes(b"".join(frames))
        obj.close()
        messagebox.showinfo('Voice Recorder', "  Recording Saved Successfully !\nFile Saved as Wave File on Desktop")
        print("Recording Saved as Wave File! (On Desktop)")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save recording: {e}")


window = tkinter.Tk()
window.title("Voice Recorder")  # for title

window.geometry('365x500')
window.configure(bg="#6d6d6d")

bt1 = tkinter.Button(window, text="Start Recording",font=("Arial Bold",15), bg="#7cc837" , fg="black", command=Start_Rec)
bt1.grid(columnspan=3, row= 0,padx =100,pady=50)


bt2 = tkinter.Button(window, text="Stop Recording",font=("Arial Bold",15), bg="#2bd4d0" , fg="black",command=Stop_Rec)
bt2.grid(columnspan=3, row=1,padx =100,pady=50)


bt3 = tkinter.Button(window, text="Save Recording",font=("Arial Bold",15),bg="#fab805" , fg="black", command= Save_Rec)
bt3.grid(columnspan=3, row=2,padx =0,pady=50)


l1 = tkinter.Label(window, text="~Vignesh",font=("Arial Bold",15),bg="#6d6d6d" )
l1.grid(column=2, row=3,padx=0,pady=5)

window.mainloop()



