import cv2
import sys

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("Please set args")
        sys.exit()

    cap = cv2.VideoCapture('output.mp4')

    if (cap.isOpened()== False):
        print("File Open Error") 

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    time = int(args[1])

    cap.set(cv2.CAP_PROP_POS_FRAMES, time*fps)
    ret, frame = cap.read()
    while True:
        if ret == True:
            cv2.imshow("Video", frame)
            cv2.imwrite("Video.png", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()

    cv2.destroyAllWindows()
