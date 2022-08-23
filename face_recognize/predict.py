from PIL import Image

from face_recognize.facenet import Facenet


def face_recognize():
    model = Facenet()
        
    image_1 = Image.open('D:\\WorkRoom\\postgraduate\\Task\pytq5\\face_recognize\img\\face1.jpg')
    image_2 = Image.open('D:\\WorkRoom\\postgraduate\\Task\pytq5\\face.jpg')
    probability = model.detect_image(image_1, image_2)
    print(probability)
    return probability

if __name__ == '__main__':
    face_recognize()