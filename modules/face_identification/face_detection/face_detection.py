import cv2
import os
import pandas as pd


class FaceDetection:
    def __init__(self, dataset_path=r'JARVIS\modules\face_identification\data',
                 class_name='demo',
                 no_of_samples=10,
                 width=300,
                 height=300,
                 caffemodel_path=r'JARVIS\modules\face_identification\model\res10_300x300_ssd_iter_140000.caffemodel',
                 prototxt_path=r'JARVIS\modules\face_identification\model\deploy.prototxt'):
        """
        Info : Face_detection class

        :param dataset_path: str (example: 'path_of_dataset')
        :param class_name: str (example: 'name_of_user')
        :param no_of_samples: int (example: 10)
        :param width: int (300)
        :param height: int (300)
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')
        :return: None
        """
        self.dataset_path = dataset_path
        self.class_name = class_name
        self.no_of_samples = no_of_samples
        self.width = width
        self.height = height
        self.caffemodel_path = caffemodel_path
        self.prototxt_path = prototxt_path

    def load_model(self):
        """
        Info : Load OpenCV CAFFE Model.
        :return: model
        """
        prototxt = self.prototxt_path
        model = self.caffemodel_path
        detector = cv2.dnn.readNetFromCaffe(prototxt, model)
        print("Model loaded...")

        return detector

    def detect_face(self, image):
        """
        Info : Detect face from image.
        """
        detector = self.load_model()
        original_size = image.shape
        target_size = (self.height, self.width)
        image = cv2.resize(image, target_size)
        aspect_ratio_x = original_size[1] / target_size[1]
        aspect_ratio_y = original_size[0] / target_size[0]
        imageBlob = cv2.dnn.blobFromImage(image=image)
        detector.setInput(imageBlob)
        detections = detector.forward()

        return detections, aspect_ratio_x, aspect_ratio_y

    def save_and_show(self, count, img):
        """
        Info : Show and save detected person images.
        """
        try:
            print(
                f'Generated {self.dataset_path}\\face_{self.class_name}_{count}.jpg')
            img = cv2.resize(img, (self.width, self.height))
            cv2.imshow('img', img)
            cv2.imwrite(
                f"{self.dataset_path}\\face_{self.class_name}_{str(count)}.jpg", img)
            count += 1

            return count
        except Exception as e:
            print(e)

    def detect(self):
        """
        Info : Create dataset of person form webcam.
        """
        try:

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            print("\nFace Detection start Look at camera and smile :)...\n")
            count = 0

            if not os.path.exists(self.dataset_path):
                os.makedirs(self.dataset_path)

            while True:
                _, img = cap.read()
                base_img = img.copy()
                detections, aspect_ratio_x, aspect_ratio_y = self.detect_face(
                    image=img)
                detections_df = pd.DataFrame(
                    detections[0][0],
                    columns=[
                        "img_id",
                        "is_face",
                        "confidence",
                        "left",
                        "top",
                        "right",
                        "bottom",
                    ],
                )
                try:
                    detections_df = detections_df[detections_df["is_face"] == 1]
                    detections_df = detections_df[detections_df["confidence"] >= 0.93]
                    for i, instance in detections_df.iterrows():
                        left = int(instance["left"] * 300)
                        bottom = int(instance["bottom"] * 300)
                        right = int(instance["right"] * 300)
                        top = int(instance["top"] * 300)
                        # draw rectangle to main image
                        cv2.rectangle(
                            img,
                            (int(left * aspect_ratio_x),
                             int(top * aspect_ratio_y)),
                            (int(right * aspect_ratio_x),
                             int(bottom * aspect_ratio_y)),
                            (255, 0, 0),
                            2,
                        )
                        if len(detections_df) != 0:
                            detected_face = base_img[
                                int(top * aspect_ratio_y) - 100: int(bottom * aspect_ratio_y) + 100,
                                int(left * aspect_ratio_x) - 100: int(right * aspect_ratio_x) + 100,
                            ]
                            count = self.save_and_show(count, detected_face)
                    cv2.imshow("img", img)
                    if count == self.no_of_samples:
                        break
                    # Stop if 'q' key is pressed
                    key = cv2.waitKey(30) & 0xFF
                    if key == ord("q"):
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                except Exception as e:
                    print('Face data is not generated please try again.')
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)
        finally:
            cv2.destroyAllWindows()
            exit


if __name__ == '__main__':
    obj = FaceDetection()
