from sahi.utils.yolov8 import download_yolov8s_model
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
import torch

yolov8_model_path = "last.pt"
download_yolov8s_model(yolov8_model_path)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

id2name = {'0': 'storage_tank',
           '1': 'Large_Vehicle',
           '2': 'Small_Vehicle',
           '3': 'plane',
           '4': 'ship',
           '5': 'Swimming_pool',
           '6': 'Harbor',
           '7': 'tennis_court',
           '8': 'Ground_Track_Field',
           '9': 'Soccer_ball_field',
           '10': 'baseball_diamond',
           '11': 'Bridge',
           '12': 'basketball_court',
           '13': 'Roundabout',
           '14': 'Helicopter'}

detection_model = AutoDetectionModel.from_pretrained(
    model_type="yolov8",
    model_path=yolov8_model_path,
    confidence_threshold=0.3,
    category_mapping=id2name,
    device=device,
)
def get_yolo_prediction(image, confidence=0.6):
    """
           Function for detecting objects

           Parameters
           __________

           image: input image (PIL Image format)
           confidence: confidence threshold

           Returns
           __________

           sahi result
        """

    detection_model.confidence_threshold = confidence
    result = get_sliced_prediction(image,
                                   detection_model,
                                   slice_height=640,
                                   slice_width=640,
                                   overlap_width_ratio=0.25,
                                   overlap_height_ratio=0.25,
                                   )
    return result
