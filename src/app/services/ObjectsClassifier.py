from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms as T
from torchvision.models._meta import _COCO_CATEGORIES
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2


class ObjectsClassifier:
    """A class for working with the classification of objects in an image"""

    def __init__(self) -> None:
        """Initializing dependencies"""
        self.model = fasterrcnn_resnet50_fpn_v2(pretrained=True)
        self.model.eval()
        self.transform = T.Compose([T.ToTensor()])

    @staticmethod
    def _image_processing(image, predictions, output_path: str) -> list[dict[str, list]]:
        """Creating an image with found objects"""
        list_found_objects = []

        draw = ImageDraw.Draw(image)
        boxes = predictions["boxes"].cpu()
        scores = predictions["scores"].cpu()
        labels = predictions["labels"].cpu()

        font = ImageFont.load_default(size=16)

        for box, score, label in zip(boxes, scores, labels):
            if score < 0.7:
                continue

            class_object = _COCO_CATEGORIES[label.item()]
            list_found_objects.append(
                {"class": class_object, "confidence": score.item(), "box": box.tolist()}
            )

            x1, y1, x2, y2 = box.tolist()
            # print(
            #     f"Found {_COCO_CATEGORIES[label.item()]} with confidence {score:.2f} at [{x1}, {y1}, {x2}, {y2}]"
            # )

            draw.rectangle([x1, y1, x2, y2], outline="blue", width=2)

            caption = f"{class_object} {score:.2f}"
            draw.text((x1, y1 - 30), caption, fill="white", font=font)

        image.save(output_path)

        return list_found_objects

    def detect_objects(
        self, image_path: str, output_path: str
    ) -> list[dict[str, list]]:
        """Detecting poses and body parts"""
        img = Image.open(image_path).convert("RGB")
        img_tensor = self.transform(img)
        predictions = self.model([img_tensor])[0]

        list_found_objects = self._image_processing(img, predictions, output_path)

        return list_found_objects
