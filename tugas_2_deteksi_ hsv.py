import cv2
import numpy as np

# ====== Rentang HSV (lebih ketat) ======
color_ranges = {
    "MERAH": [
        {"lower": np.array([0, 150, 80]), "upper": np.array([10, 255, 255])},
        {"lower": np.array([170, 150, 80]), "upper": np.array([180, 255, 255])}
    ],
    "HIJAU": [
        {"lower": np.array([40, 120, 70]), "upper": np.array([80, 255, 255])}
    ],
    "BIRU": [
        {"lower": np.array([100, 150, 70]), "upper": np.array([140, 255, 255])}
    ]
}

# Batas minimal agar warna pucat tidak dihitung
MIN_SAT = 80
MIN_VAL = 80

# Batas ukuran contour (menghindari noise)
MIN_AREA = 1200

box_colors = {
    "MERAH": (0, 0, 255),
    "HIJAU": (0, 255, 0),
    "BIRU":  (255, 0, 0)
}

cap = cv2.VideoCapture(0)

cv2.namedWindow("Multi Mode Viewer", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Multi Mode Viewer", 1280, 900)

mode = 1


def clean_mask(mask):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    return mask


def apply_sv_filter(hsv, mask):
    h, s, v = cv2.split(hsv)
    sv_mask = cv2.inRange(s, MIN_SAT, 255)
    sv_mask2 = cv2.inRange(v, MIN_VAL, 255)
    final = cv2.bitwise_and(mask, mask, mask=cv2.bitwise_and(sv_mask, sv_mask2))
    return final


def mode_tracking(frame, hsv):
    detected_list = []
    masks = []

    for color_name, ranges in color_ranges.items():
        mask_total = None

        for r in ranges:
            mask = cv2.inRange(hsv, r["lower"], r["upper"])
            mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

        mask_total = apply_sv_filter(hsv, mask_total)
        mask_total = clean_mask(mask_total)
        masks.append(mask_total)

        contours, _ = cv2.findContours(mask_total, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            # Hindari deteksi random
            if area < MIN_AREA:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            aspect = w / float(h)

            # Hanya bentuk yang mendekati kotak
            if aspect < 0.3 or aspect > 3:
                continue

            cv2.rectangle(frame, (x, y), (x + w, y + h), box_colors[color_name], 2)
            cv2.putText(frame, color_name, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_colors[color_name], 2)

            if color_name not in detected_list:
                detected_list.append(color_name)

    if detected_list:
        cv2.putText(frame, "Terdeteksi: " + ", ".join(detected_list),
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Tidak ada warna terdeteksi",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    try:
        mask_combined = np.hstack(masks)
        mask_combined = cv2.resize(mask_combined, (330, 230))
    except:
        mask_combined = np.zeros((230, 330), dtype=np.uint8)

    mask_color = cv2.cvtColor(mask_combined, cv2.COLOR_GRAY2BGR)

    h, w = frame.shape[:2]
    frame[10:10+230, w-350:w-20] = mask_color

    return frame


def mode_hsv_viewer(hsv):
    h_ch, s_ch, v_ch = cv2.split(hsv)

    hue_color = cv2.merge([h_ch, np.full_like(h_ch, 255), np.full_like(h_ch, 255)])
    hue_color = cv2.cvtColor(hue_color, cv2.COLOR_HSV2BGR)

    hsv_display = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    s_color = cv2.cvtColor(s_ch, cv2.COLOR_GRAY2BGR)
    v_color = cv2.cvtColor(v_ch, cv2.COLOR_GRAY2BGR)

    W, H = 360, 260
    hsv_display = cv2.resize(hsv_display, (W, H))
    hue_color = cv2.resize(hue_color, (W, H))
    s_color = cv2.resize(s_color, (W, H))
    v_color = cv2.resize(v_color, (W, H))

    top = np.hstack((hsv_display, hue_color))
    bottom = np.hstack((s_color, v_color))
    grid = np.vstack((top, bottom))

    cv2.putText(grid, "HSV Color", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.putText(grid, "Hue Color", (380, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.putText(grid, "Saturation", (15, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.putText(grid, "Value", (380, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    return grid


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    frame = cv2.resize(frame, None, fx=1.2, fy=1.2)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if mode == 1:
        output = mode_tracking(frame.copy(), hsv)
        cv2.putText(output, "MODE 1: TRACKING WARNA (tekan 2)",
                    (10, output.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    elif mode == 2:
        output = mode_hsv_viewer(hsv)
        cv2.putText(output, "MODE 2: HSV VIEWER (tekan 1)",
                    (10, output.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Multi Mode Viewer", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        mode = 1
    elif key == ord('2'):
        mode = 2
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()