import sys

try:
    from face_detection import face_detection
    from face_recognition import face_recognition
except Exception as e:
    from jarvis.modules.face_identification.face_detection import face_detection
    from jarvis.modules.face_identification.face_recognition import face_recognition


class FaceRecognition(object):
    def __init__(self):
        pass

    def face_detetion(self, dataset_path, class_name, no_of_samples, width, height, caffemodel_path, prototxt_path):
        """
        Info : Dataset Create by face detection with OpenCV SSD.

        :param dataset_path: str (example: 'path_of_dataset')
        :param class_name: str (example: 'name_of_folder')
        :param no_of_samples: int (example: 10)
        :param width: int (example: 300)
        :param height: int (example: 300)
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')
        :return: None
        """
        obj = face_detection.FaceDetection(
            dataset_path, class_name, no_of_samples, width, height, caffemodel_path, prototxt_path)
        obj.detect()

    def face_recognition(self, data_path, img_height, img_width, model_path, caffemodel_path, prototxt_path):
        """
        Info : Face_Recognition class

        :param data_path : str (example: 'Path_to_Data')
        :param img_heigth: int (example: 224)
        :param img_width: int (example: 224)
        :parma model_path: str (example: 'Path_To_Tensorflow_model')
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')

        :return: final person name
        """

        obj = face_recognition.FaceRecognition(
            data_path, img_height, img_width, model_path, caffemodel_path, prototxt_path
        )

        obj.predict_person()


if __name__ == '__main__':
    obj = FaceRecognition()
    obj.face_detetion()
    obj.face_recognition()
