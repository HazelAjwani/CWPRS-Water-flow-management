import cv2
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import torch

class ObjectEdgeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection with Dimensions")
        self.video_label = Label(root)
        self.video_label.pack()
        self.capture_button = Button(root, text="Capture", command=self.capture_frame)
        self.capture_button.pack()
        self.stop_button = Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()
        self.running = True
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.capture = cv2.VideoCapture(0) 
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.pixels_per_meter = None
        self.update_frame()

    def calibrate_pixels_per_meter(self, reference_width_pixels, reference_real_width_m):
        self.pixels_per_meter = reference_width_pixels / reference_real_width_m

    def update_frame(self):
        if not self.running:
            return
        ret, frame = self.capture.read()
        if not ret:
            print("Error: Could not read frame from camera")
            return
        results = self.model(frame)
        for detection in results.xyxy[0]:
            x1, y1, x2, y2, confidence, class_id = detection.tolist()
            class_name = self.model.names[int(class_id)]
            pixel_width = x2 - x1
            pixel_height = y2 - y1
            if self.pixels_per_meter is not None:
                real_width_m = pixel_width / self.pixels_per_meter
                real_height_m = pixel_height / self.pixels_per_meter
                if class_name == "person":
                    continue
                print(f"Detected: {class_name}")
                print(f"Width: {real_width_m:.2f} m")
                print(f"Height: {real_height_m:.2f} m\n")
            else:
                print("Calibration needed. Please calibrate with a reference object.")
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.video_label.configure(image=frame_image)
        self.video_label.image = frame_image
        self.root.after(10, self.update_frame)

    def capture_frame(self):
        ret, frame = self.capture.read()
        if ret:
            reference_object_width_pixels = 100 
            reference_object_real_width_m = 0.3 
            self.calibrate_pixels_per_meter(reference_object_width_pixels, reference_object_real_width_m)
            print("Calibration complete. Pixels per meter:", self.pixels_per_meter)

    def stop(self):
        self.running = False
        self.capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = ObjectEdgeDetectionApp(root)
    root.mainloop()
