def yolo_box_to_cv2(yolo_box: list, w: int, h: int) -> tuple[tuple[int, int], tuple[int, int]]:
    left = (
        int((yolo_box[0] - yolo_box[2] / 2) * w),
        int((yolo_box[1] - yolo_box[3] / 2) * h)
    )
    right = (
        int((yolo_box[0] + yolo_box[2] / 2) * w),
        int((yolo_box[1] + yolo_box[3] / 2) * h)
    )

    return left, right


def cv2_to_yolo_box(
        left_cv2: tuple[float, float],
        right_cv2: tuple[float, float],
        w: int,
        h: int
) -> tuple[float, float, float, float]:
    left, up = left_cv2
    right, bottom = right_cv2

    width = right-left
    height = bottom-up

    x_center = left + width/2
    y_center = up + height/2

    return x_center/w, y_center/h, width/w, height/h
