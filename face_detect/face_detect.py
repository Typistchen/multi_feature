# 人脸识别
import cv2


# 图片中人脸识别

def face_detect():
    img = cv2.imread("D:\\WorkRoom\\postgraduate\\Task\pytq5\\test.jpg")
    # 1、转灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # cv2.imshow("gray", gray)

    # 2、训练一组人脸
    face_detector = cv2.CascadeClassifier(
        "D:\\ProgramFiles\\opencv\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt.xml")

    # 3、检测人脸（用灰度图检测，返回人脸矩形坐标(4个角)）
    faces_rect = face_detector.detectMultiScale(gray, 1.05, 3)
    #                                          灰度图  图像尺寸缩小比例  至少检测次数（若为3，表示一个目标至少检测到3次才是真正目标）
    # print("人脸矩形坐标faces_rect：", faces_rect)

    # 4、遍历每个人脸，画出矩形框
    dst = img.copy()
    for x, y, w, h in faces_rect:
        cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 0, 255), 3)  # 画出矩形框
        cut = dst[y:y + h, x: x + w]
        cv2.imwrite('face.jpg', cut)

    # 显示
    # cv2.imshow("dst", dst)


if __name__ == "__main__":
    # 读取图片
    face_detect()

