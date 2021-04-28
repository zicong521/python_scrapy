
import cv2

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS) #获取帧率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)

fourcc = cv2.VideoWriter_fourcc(*"DIVX")
# 第三个参数则是镜头快慢的，20为正常，小于二十为慢镜头

out = cv2.VideoWriter('output.avi', fourcc, fps, size)
while True:
    # 一帧一帧的获取图像
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 1)
        # 在帧上进行操作
        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # 开始保存视频
        out.write(frame)
        # 显示结果帧
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# 释放摄像头资源
cap.release()
out.release()
cv2.destroyAllWindows()
