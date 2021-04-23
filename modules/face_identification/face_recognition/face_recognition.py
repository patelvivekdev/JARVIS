import os
import cv2
import tensorflow as tf
import numpy as np
import pandas as pd


def find_cosine_similarity(source_representation, test_representation):
    """Find CosinesSimilarity"""
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))

    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


class FaceRecognition:
    def __init__(self,
                 data_path=r'JARVIS\modules\face_identification\data',
                 img_height=224,
                 img_width=224,
                 model_path=r'JARVIS\modules\face_identification\model\model.h5',
                 caffemodel_path=r'JARVIS\modules\face_identification\model\res10_300x300_ssd_iter_140000.caffemodel',
                 prototxt_path=r'JARVIS\modules\face_identification\model\deploy.prototxt'):
        """
        Info : Face_Recognition class

        :param data_path : str (example: 'Path_to_Data')
        :param img_height: int (example: 224)
        :param img_width: int (example: 224)
        :param model_path: str (example: 'Path_To_Tensorflow_model')
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')

        :return: final person name
        """
        self.img_height = img_height
        self.img_width = img_width
        self.model_path = model_path
        self.caffemodel_path = caffemodel_path
        self.prototxt_path = prototxt_path
        self.data_path = data_path

    def create_model(self):
        """
        Info : Load Model with tf.keras load_model function.
        :return : Tensorflow model
        """
        model = tf.keras.models.load_model(self.model_path)
        print("Model Loaded...")

        return model

    def preprocess_image(self, image_path):
        """
        Info : Loads image from path and resizes it
        :return : resize image
        """
        img = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(self.img_height, self.img_width))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = tf.keras.applications.imagenet_utils.preprocess_input(img)

        return img

    def load_detector(self):
        """
        Info :  Load caffe model for face detection.
        :return : detector
        """
        prototxt = self.prototxt_path
        caff_model = self.caffemodel_path
        detector = cv2.dnn.readNetFromCaffe(prototxt, caff_model)

        return detector

    def detect_face(self, img):
        """
        Info : Detect face from image.
        :return : detections, aspect_ratio
        """
        original_size = img.shape
        target_size = (300, 300)
        img = cv2.resize(img, target_size)  # Resize to target_size
        aspect_ratio_x = original_size[1] / target_size[1]
        aspect_ratio_y = original_size[0] / target_size[0]
        imageBlob = cv2.dnn.blobFromImage(image=img)
        detector = self.load_detector()
        detector.setInput(imageBlob)
        detections = detector.forward()

        return detections, aspect_ratio_x, aspect_ratio_y

    def predict_person(self):
        """
        Info : Predict on webcam and return name of detected person if it's already known.
        :return : user_name
        """
        found = 0
        user_name = ""
        try:
            model = self.create_model()

            mypath = self.data_path
            all_people_faces = dict()
            for file in os.listdir(mypath):
                person_face = file.split(".")[0]
                all_people_faces[person_face] = model.predict(
                    self.preprocess_image(f'{mypath}/{person_face}.jpg')
                )[0, :]

            print("Face representations retrieved successfully")

            cap = cv2.VideoCapture(
                0, cv2.CAP_DSHOW
            )
            print("Start Recognition.....")
            while True:
                ret, img = cap.read()
                base_img = img.copy()
                detections, aspect_ratio_x, aspect_ratio_y = self.detect_face(
                    img)
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
                detections_df = detections_df[detections_df["is_face"] == 1]
                detections_df = detections_df[detections_df["confidence"] >= 0.95]
                if len(detections_df) != 0:
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
                        cv2.imshow("img", img)
                        detected_face = base_img[
                            int(top * aspect_ratio_y)
                            - 100: int(bottom * aspect_ratio_y) + 100,
                            int(left * aspect_ratio_x)
                            - 100: int(right * aspect_ratio_x) + 100,
                        ]
                        if len(detected_face) != 0:
                            try:
                                detected_face = cv2.resize(
                                    detected_face, (self.img_height,
                                                    self.img_width)
                                )
                                img_pixels = tf.keras.preprocessing.image.img_to_array(
                                    detected_face
                                )
                                img_pixels = np.expand_dims(img_pixels, axis=0)
                                img_pixels /= 255
                                captured_representation = model.predict(img_pixels)[
                                    0, :]
                                for person in all_people_faces:
                                    person_name = person
                                    representation = all_people_faces[person]
                                    similarity = find_cosine_similarity(
                                        representation, captured_representation
                                    )
                                    if similarity < 0.30:
                                        user_name = person_name.split("_")[1]
                                        found = 1
                                        break
                            except Exception as e:
                                print(e)
                cv2.imshow("img", img)
                if found == 1:
                    break
                if cv2.waitKey(1) == 13:  # 13 is the Enter Key
                    break
            return user_name
        except Exception as e:
            print(e)
        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    obj = FaceRecognition()
