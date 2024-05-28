import cv2
from box_formate import yolo_box_to_cv2, cv2_to_yolo_box


class Splitter:
    res = {}

    def __init__(
        self,
        image_file: str,
        label_file: str,
        split_frame_size: int,
    ) -> None:
        self.image = cv2.imread(image_file)
        self.height, self.width = self.image.shape[:2]
        self.frame_size = split_frame_size
        labels = []
        with open(label_file, "r") as f:
            for row in f:
                yolo_box = [float(coord) for coord in row.strip().split(" ")[1:]]
                label = int(row.strip().split(" ")[0])
                left, right = yolo_box_to_cv2(yolo_box, self.width, self.height)
                labels.append(((left, right), label))
        self.labels = labels

    def split_by_vertical(self, left: int, right: int, hor_number: int) -> None:
        up = 0
        vert_number = 0
        while up + self.frame_size <= self.height:
            self.crop_and_save(left, up, right, hor_number, vert_number)
            vert_number += 1
            up += self.frame_size // 2
        if up < self.height:
            self.crop_and_save(left, up, right, hor_number, vert_number)

    def crop_and_save(self, left: int, up: int, right: int, hor_number: int, vert_number: int) -> None:
        frame_left = (left, up)
        frame_right = (right, up + self.frame_size)
        frame = (frame_left, frame_right)
        in_frame_labels = [label for label in self.labels if self.define_if_label_in_frame(label[0], frame)]
        labels_relatively_to_frame = [(self.make_label_relatively_to_frame(label[0], frame), label[1]) for label in in_frame_labels]

        cropped_image = self.image[frame_left[1]:frame_right[1], frame_left[0]:frame_right[0]]
        height, width = cropped_image.shape[:2]

        res_labels = []
        for label in labels_relatively_to_frame:
            yolo_label = cv2_to_yolo_box(label[0][0], label[0][1], width, height)
            yolo_label = [str(round(elem, 6)) for elem in yolo_label]
            yolo_label = [elem + "0"*(8-len(elem)) for elem in yolo_label]
            line = f"{label[1]} {' '.join(yolo_label)}"
            res_labels.append(line)

        self.res[f"{hor_number}_{vert_number}"] = {
            "labels": "\n".join(res_labels),
            "image": cropped_image
        }

    def crop(self) -> dict[str, dict[str]]:
        left = 0
        hor_number = 0
        while left + self.frame_size <= self.width:
            self.split_by_vertical(left, left+self.frame_size, hor_number)
            left += self.frame_size // 2
            hor_number += 1

        if left < self.width:
            self.split_by_vertical(left, left + self.frame_size, hor_number)

        return self.res

    @staticmethod
    def define_if_label_in_frame(
            label: tuple[tuple[float, float], tuple[float, float]],
            frame: tuple[tuple[float, float], tuple[float, float]]
    ) -> bool:
        label_left, label_right = label
        frame_left, frame_right = frame

        if (
            label_left[0] > frame_left[0] and
            label_left[1] > frame_left[1] and
            label_right[0] < frame_right[0] and
            label_right[1] < frame_right[1]
        ):
            return True
        else:
            return False

    @staticmethod
    def make_label_relatively_to_frame(
            label: tuple[tuple[float, float], tuple[float, float]],
            frame: tuple[tuple[float, float], tuple[float, float]]
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        label_left, label_right = label
        frame_left, frame_right = frame
        res_label_left = (label_left[0]-frame_left[0], label_left[1]-frame_left[1])
        res_label_right = (label_right[0] - frame_left[0], label_right[1] - frame_left[1])

        return res_label_left, res_label_right

