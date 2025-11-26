import cv2
import numpy as np

def make_gaussian_kernel(ksize=9, sigma=1.5):
    g1d = cv2.getGaussianKernel(ksize, sigma)
    g2d = g1d @ g1d.T
    return g2d

gauss_kernel = make_gaussian_kernel(9, 1.5)

k_sharpen = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
], dtype=np.float32)

mode = 0

cap = cv2.VideoCapture(0)

print("== TUGAS 1 CONTROL ==")
print("0 = Normal")
print("1 = Average Blur 5x5")
print("2 = Average Blur 9x9")
print("3 = Gaussian Blur (custom kernel)")
print("4 = Sharpen")
print("q = Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()

    if mode == 1:
        output = cv2.blur(frame, (5, 5))
    elif mode == 2:
        output = cv2.blur(frame, (9, 9))
    elif mode == 3:
        output = cv2.filter2D(frame, -1, gauss_kernel)
    elif mode == 4:
        output = cv2.filter2D(frame, -1, k_sharpen)

    cv2.putText(output, f"Mode = {mode}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow("Tugas 1 - Filtering", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4')]:
        mode = int(chr(key))

cap.release()
cv2.destroyAllWindows()