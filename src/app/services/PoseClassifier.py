from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms as T
from torchvision.models._meta import _COCO_PERSON_KEYPOINT_NAMES
from torchvision.models.detection import keypointrcnn_resnet50_fpn

class PoseClassifier:
    """A class for finding human body parts"""

    def __init__(self):
        """Initializing dependencies"""
        self.model = keypointrcnn_resnet50_fpn(pretrained=True)
        self.model.eval()
        self.transform = T.Compose([T.ToTensor()])
    
    @staticmethod
    def _get_point_type(kp_idx: int) -> str:
        """Determining the type of point for color selection"""
        if kp_idx in [0, 1, 2, 3, 4]:
            return "head"
        elif kp_idx in [5, 6, 7, 8, 9, 10]:
            return "hands"
        elif kp_idx in [11, 12, 13, 14, 15, 16]:
            return "legs"
        return "torso"
    
    def _image_processing(self, image, predictions, output_path: str) -> list[dict]:
        """Creating an image with the found poses and body parts"""     
        list_found_body_parts = []

        colors = {
            "head": "red",
            "hands": "green",
            "legs": "blue",
            "torso": "purple"
        }
        
        draw = ImageDraw.Draw(image)
        keypoints = predictions["keypoints"]
        scores = predictions["scores"]
        font = ImageFont.load_default(size=26)


        for kps, score in zip(keypoints, scores):
            if score < 0.7:
                continue

            for kp_idx, kp in enumerate(kps):
                x, y, conf = kp
                
                if conf > 0.3:
                    name = _COCO_PERSON_KEYPOINT_NAMES[kp_idx]
                    text_position = (x + 8, y - 10)
                    ellipse_color = self._get_point_type(kp_idx)

                    list_found_body_parts.append({"class": name, "confidence": score.item(), "position": (x.item(), y.item())})

                    draw.ellipse([(x-5, y-5), (x+5, y+5)], fill=colors.get(ellipse_color, "white"), width=3)
                    draw.text(text_position, name, fill="white", font=font)

        image.save(output_path)

        return list_found_body_parts

    def detect_poses(self, path_to_image: str, output_path: str) -> list[dict]:
        """Finding a person's poses and body parts"""
        image = Image.open(path_to_image).convert("RGB")
        img_tensor = self.transform(image)
        predictions = self.model([img_tensor])[0]

        list_found_body_parts = self._image_processing(image, predictions, output_path)

        return list_found_body_parts

