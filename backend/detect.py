import cv2

# Load the image
image = cv2.imread('./simon.jpg')
print(image.shape)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the pre-trained Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Perform eye detection
eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

# Check if 2 or more eyes are detected
if len(eyes) >= 2:
    # Sort eyes by x coordinate
    sorted_eyes = sorted(eyes, key=lambda x: x[0])

    # Get the leftmost and rightmost eyes
    left_eye = sorted_eyes[0]
    right_eye = sorted_eyes[-1]

    # Create a bounding box that encompasses both eyes
    box_start = (left_eye[0], min(left_eye[1], right_eye[1]))
    box_end = (right_eye[0] + right_eye[2], max(left_eye[1] + left_eye[3], right_eye[1] + right_eye[3]))

    # Draw the bounding box
    cv2.rectangle(image, box_start, box_end, (0, 255, 0), 2)

    # Display the image
    cv2.imwrite('output.jpg', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Less than two eyes detected")
