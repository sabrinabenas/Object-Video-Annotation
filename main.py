import tkinter as tk
from tkinter import filedialog, simpledialog
import cv2
import os 
import video_scroll

#global
click_positions = [] 
labels = [] 
labels_keys = [] 


def select_video():
    global cap, click_positions, labels, labels_keys , video_path,fps,frame_count , time
    video_path = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    
    if video_path:
        cap = cv2.VideoCapture(video_path)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        time =  int(frame_count/fps)
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Image with Annotations", frame)
            cv2.setMouseCallback("Image with Annotations", on_mouse_click)
        else:
            print("No se pudo leer el video")
    else:
        print("No se seleccionó ningún video")

def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        label_text = simpledialog.askstring("Nombre del objeto", "Name:  ")
        label_key = simpledialog.askstring("Key del objeto", "one letter: \n ('p' reserved)")
        if label_text:
            click_positions.append((x, y))
            labels.append(label_text)
            labels_keys.append(label_key)
            draw_circles_and_labels()

def draw_circles_and_labels():
    global cap, click_positions, labels, labels_keys, frame_with_annotations
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Volver al primer frame
    ret, frame = cap.read()
    if ret:
        for (pos, text,text_key) in zip(click_positions, labels,labels_keys):
            cv2.circle(frame, pos, 10, (0, 255, 0), -1)
            cv2.putText(frame, text, (pos[0] + 15, pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, text_key, (pos[0] + 15, pos[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Image with Annotations", frame)
        frame_with_annotations = frame

def save_image():
    global frame_with_annotations ,video_path 
    if frame_with_annotations is not None:
        project_folder = os.path.dirname(video_path) + '/'
        save_path = "imagewithobjects.png"
        cv2.imwrite(project_folder  + save_path, frame_with_annotations)
        print(f"Imagen guardada en {save_path}")
    else:
        print("No hay anotaciones para guardar")

def create_gui(root):
    root.geometry("400x200")
    btn_select_video = tk.Button(root, text="Seleccionar Video", command=select_video)
    btn_select_video.pack(pady=20)

    btn_finish = tk.Button(root, text="Finish", command=lambda: finish_and_exit(root))
    btn_finish.pack(pady=20)

def finish_and_exit(root):
    save_image()
    root.destroy()


def main():
    root = tk.Tk()
    root.title("Video Annotation")
    create_gui(root)
    root.mainloop()
    print(os.path.dirname(video_path))
    dic = video_scroll.video_scroll(video_path, labels, labels_keys)

    ##save info
    L = ['sampled video: \n',str(video_path),'\n','\n',
    'video duration: \n',str(time),'\n','\n',
    'fps: \n',str(fps),'\n','\n',
    'number of frames \n',str(frame_count),'\n','\n',
    'objects: \n',str(labels_keys),'\n','\n',
    'Object frames: \n',str(dic)]
    project_folder = os.path.dirname(video_path) + '/'
    f = open(os.path.join(project_folder,'logfile_' + str(video_path.split('/')[-1].split('.')[0])), "w+") 
    f.writelines(L) 
    f.close()

if __name__ == "__main__":
    main()
