from JARVIS.modules.face_identification.face_detection import face_detection
from JARVIS.modules.face_identification.face_recognition import face_recognition


class FaceIdentificaion():
    """Face Identification class."""

    def __init__(self):
        pass

    def face_detetion(self, dataset_path=r'JARVIS\modules\face_identification\data',
                      class_name='demo',
                      no_of_samples=5,
                      width=300,
                      height=300,
                      caffemodel_path=r'JARVIS\modules\face_identification\model\res10_300x300_ssd_iter_140000.caffemodel',
                      prototxt_path=r'JARVIS\modules\face_identification\model\deploy.prototxt'):
        """
        Info : Dataset Create by face detection with OpenCV SSD.

        :param dataset_path: str (example: 'path_of_dataset')
        :param class_name: str (example: 'name_of_user')
        :param no_of_samples: int (example: 5)
        :param width: int (example: 300)
        :param height: int (example: 300)
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')
        :return: None
        """
        obj = face_detection.FaceDetection(
            dataset_path, class_name, no_of_samples, width, height, caffemodel_path, prototxt_path)
        obj.detect()

    def face_recognition(self, data_path=r'JARVIS\modules\face_identification\data',
                         img_height=224,
                         img_width=224,
                         model_path=r'JARVIS\modules\face_identification\model\model.h5',
                         caffemodel_path=r'JARVIS\modules\face_identification\model\res10_300x300_ssd_iter_140000.caffemodel',
                         prototxt_path=r'JARVIS\modules\face_identification\model\deploy.prototxt'):
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

        person_name = obj.predict_person()

        return person_name


if __name__ == '__main__':
    obj = FaceIdentificaion()
