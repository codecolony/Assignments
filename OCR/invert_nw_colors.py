import cv2


src = cv2.imread("text_crop.jpg", 0)
dst = cv2.bitwise_not ( src )
cv2.imwrite("col3_hor_clean_neg.jpg", dst)