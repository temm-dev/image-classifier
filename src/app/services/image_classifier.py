from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms as T
from torchvision.models._meta import _COCO_CATEGORIES
from torchvision.models.detection import (
    fasterrcnn_resnet50_fpn_v2
)


class ImageClassifier:
    """A class for working with the classification of objects in an image"""

    def __init__(self) -> None:
        """Initializing dependencies"""
        self.model = fasterrcnn_resnet50_fpn_v2(pretrained=True)
        self.model.eval()
        self.transform = T.Compose([T.ToTensor()])

    def _classifying_objects_process(self, img_tensor) -> dict:
        """A method for classifying objects in an image"""
        outputs = self.model([img_tensor])
        output = outputs[0]

        return output

    @staticmethod
    def _image_processing(image, output, output_filename) -> None:
        """A method for creating an image with found objects"""
        draw = ImageDraw.Draw(image)
        boxes = output["boxes"].cpu()
        scores = output["scores"].cpu()
        labels = output["labels"].cpu()

        font = ImageFont.load_default(size=16)

        for box, score, label in zip(boxes, scores, labels):
            if score < 0.7:
                continue

            x1, y1, x2, y2 = box.tolist()
            draw.rectangle([x1, y1, x2, y2], outline="blue", width=2)

            caption = f"{_COCO_CATEGORIES[label.item()]} {score:.2f}"
            draw.text((x1, y1 - 30), caption, fill="white", font=font)

        image.save(output_filename)

    def classification_process(self, path_to_image: str, output_filename: str) -> None:
        """A method for classifying objects in an image"""
        img = Image.open(path_to_image).convert("RGB")
        img_tensor = self.transform(img)

        output = self._classifying_objects_process(img_tensor)

        self._image_processing(img, output, output_filename)
