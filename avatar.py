import cv2

def face_tracking():
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Capture video from default camera (can be changed to a video file path)
    cap = cv2.VideoCapture(0)

    # Initialize tracker using the first detected face
    tracker = cv2.TrackerKCF_create()
    initBB = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If a face is detected and we're not currently tracking
        if len(faces) > 0 and initBB is None:
            x, y, w, h = faces[0]
            initBB = (x, y, w, h)
            tracker.init(frame, initBB)

        # Update tracker and draw bounding box
        if initBB is not None:
            success, box = tracker.update(frame)

            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Face Tracking', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

face_tracking()
