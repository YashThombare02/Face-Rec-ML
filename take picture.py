import cv2
import tkinter.filedialog

camera_input = False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if not camera_input:
    filename = tkinter.filedialog.askopenfilename()
    print(filename)

    if not filename:
        print("No file selected.")
        exit()

    frame = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    if frame is None:
        print("Failed to load image.")
        exit()

    # Process the image
    try:
        if len(frame.shape) == 2 or (len(frame.shape) == 3 and frame.shape[2] == 1):
            gray = frame
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            print('no face')
        else:
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]

            # resize image
            output = cv2.resize(roi_gray, (50, 50))
            cv2.imwrite(filename='subjects_photos/' + input('file number (1~100)?') + '.png', img=output)
            print("Image saved.")
    except Exception as er:
        print(er)

    print("Program ended.")

else:
    webcam = cv2.VideoCapture(0)
    key = cv2.waitKey(1)

    while True:
        try:
            check, frame = webcam.read()
            if not check:
                print("Failed to capture frame.")
                break

            key = cv2.waitKey(1)
            image = frame
            if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
                gray = image
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x-4, y-4), (x+w+4, y+h+4), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]

            cv2.imshow("Capturing", image)

            if key == ord('s'):
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        roi_gray = gray[y:y+h, x:x+w]

                    # resize image
                    output = cv2.resize(roi_gray, (50, 50))
                    cv2.imwrite(filename='subjects_photos/' + input('file number (1~100)?') + '.png', img=output)
                    print("Image saved.")
                except Exception as er:
                    print(er)

            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

        except Exception as er:
            if "name 'y' is not defined" in str(er):
                print('no face')
                break
            else:
                print(er)
 
