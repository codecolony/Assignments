import cv2


# void deskew(const char* filename, double angle)
# {
#   cv::Mat img = cv::imread(filename, 0);
 
#   cv::bitwise_not(img, img);
 
#   std::vector<cv::Point> points;
#   cv::Mat_<uchar>::iterator it = img.begin<uchar>();
#   cv::Mat_<uchar>::iterator end = img.end<uchar>();
#   for (; it != end; ++it)
#     if (*it)
#       points.push_back(it.pos());
 
#   cv::RotatedRect box = cv::minAreaRect(cv::Mat(points));

# filename = "col3.jpg"
# img = cv2.imread(filename)

# cv2.biwise_not(img)


img = cv2.imread('col2.jpg')
rows,cols,ch = img.shape

M = cv2.getRotationMatrix2D((cols/2,rows/2),-4,1)
dst = cv2.warpAffine(img,M,(cols,rows))


cv2.imshow('hhh', dst)
cv2.imwrite("out_hor.jpg", dst)
cv2.waitKey(0)

# points = []

# img