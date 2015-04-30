import cv2 as cv
import numpy as np
import img_utils as iu
import math
import os

test_image = os.path.abspath(os.path.join(os.path.dirname("__file__"),
                                          "../resources/", "test_image.png"))

test_cnt1 = [[615, 21], [638, 31]]
test_cnt2 = [[715, 31], [738, 51]]
test_contours = [test_cnt1, test_cnt2]

test_cor1 = [632, 37]
test_cor2 = [298, 133]
test_corners = [test_cor1, test_cor2]


def contours_close(cnt1, cnt2, min_dist=20):
    """
    #>>> contours_close(None, test_cnt2)
    #TODO

    >>> contours_close(None, test_cnt2)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be None.

    >>> contours_close(test_cnt1, [])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be void.

    >>> contours_close(test_cnt1, test_cnt2, -20)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_dist value must be greater than 0.
    """

    # Checking arguments
    check_contour(cnt1)
    check_contour(cnt2)
    check_min_dist(min_dist)

    result = False

    for i in xrange(cnt1.shape[0]):
        for j in xrange(cnt2.shape[0]):
            dist = np.linalg.norm(cnt1[i] - cnt2[j])
            if abs(dist) <= min_dist:
                result = True

    return result


def delete_border_noise(input_file, width=20, color=(255, 255, 255)):
    """
    #>>> delete_boder_noise(test_image)
    #TODO

    >>> delete_border_noise(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be a None object

    >>> delete_border_noise("")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be ''.

    >>> delete_border_noise("fakeRoute")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: Input file not found.

    >>> delete_border_noise(test_image, width=-10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Width value must be greater than 0.

    >>> delete_border_noise(test_image, color=(-10, 0, 0))
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Color value must be: (0-255, 0-255, 0-255).
    """

    # Checking arguments
    check_color(color)
    check_width(width)

    image = iu.get_image(input_file)

    image = iu.pyramid_clean(image)

    image[0:width, :] = color
    image[:, 0:width] = color
    image[:, -width:] = color
    image[-width:, :] = color

    return image


def delete_small_contours(contours, min_dim=1000):
    """
    #>>> delete_small_contours(test_contours)
    #TODO

    >>> delete_small_contours(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be None.

    >>> delete_small_contours([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be void.

    >>> delete_small_contours(test_contours, min_dim=-10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_dim value must be greater than 0.
    """

    # Checking arguments
    check_contours(contours)
    check_min_dim(min_dim)

    new_contours = []

    for i in contours:
        if get_contour_dimension(i) > min_dim:
            new_contours.append(i)

    return new_contours


def detect_contours(input_file, thresh_val=255):
    """
    #>>> delete_boder_noise(test_image)
    #TODO

    >>> detect_contours(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be a None object

    >>> detect_contours("")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be ''.

    >>> detect_contours("fakeRoute")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: Input file not found.

    >>> detect_contours(test_contours, thresh_val=270)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: All threshold values must be between 0 and 255.
    """

    # Checking arguments
    check_threshold(thresh_val)

    gray = iu.get_image(input_file, 0)

    gray = iu.pyramid_clean(gray)

    th2 = cv.adaptiveThreshold(gray, thresh_val, cv.ADAPTIVE_THRESH_MEAN_C,
                               cv.THRESH_BINARY, 11, 2)

    th2 = cv.erode(th2, kernel=(5, 5), iterations=30)

    th2 = cv.bitwise_not(th2)

    contours, h = cv.findContours(th2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    return contours


def detect_corners(input_file, max_corners=10, min_dist=50, trust_val=0.5):
    """
    #>>> detect_corners(test_image)
    #TODO

    >>> detect_corners(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be a None object

    >>> detect_corners("")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be ''.

    >>> detect_corners("fakeRoute")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: Input file not found.

    >>> detect_corners(test_image, max_corners=-5)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Max_corners value must be greater than 0.

    >>> detect_corners(test_image, min_dist=-100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_dist value must be greater than 0.

    >>> detect_corners(test_image, trust_val=5)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Trust_val value must be between 0 and 1.
    """

    # Checking arguments
    check_max_corners(max_corners)
    check_min_dist(min_dist)
    check_trust_val(trust_val)

    image = iu.get_image(input_file)

    contours = detect_contours(image)

    blank = image
    blank[:] = 255

    img = draw_contours(blank, contours, 10, color=(0, 0, 0))

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    corners = cv.goodFeaturesToTrack(img, max_corners, trust_val, min_dist)

    return corners


def draw_contours(input_file, contours, thickness=0, color=(0, 0, 255)):

    """
    #>>> draw_contours(test_image, test_contours)
    #TODO

    >>> draw_contours(None, test_contours)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be a None object

    >>> draw_contours("", test_contours)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be ''.

    >>> draw_contours("fakeRoute", test_contours)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: Input file not found.

    >>> draw_contours(test_image, None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be None.

    >>> draw_contours(test_image, [])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be void.

    >>> draw_contours(test_image, test_contours, color=(-10, 0, 0))
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Color value must be: (0-255, 0-255, 0-255).
    """

    # Checking arguments
    check_contours(contours)
    check_color(color)

    image = iu.get_image(input_file)

    for cnt in contours:
        cv.drawContours(image, [cnt], 0, color, thickness)

    return image


def draw_corners(input_file, corners, radius=5, color=(0, 0, 255), thickness=-1):
    """
    #>>> draw_corners(test_image, test_corners)
    #TODO

    >>> draw_corners(None, test_corners)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be a None object

    >>> draw_corners("", test_corners)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be ''.

    >>> draw_corners("fakeRoute", test_corners)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: Input file not found.

    >>> draw_corners(test_image, None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Corners can't be None.

    >>> draw_corners(test_image, [])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Corners can't be void.

    >>> draw_corners(test_image, test_corners, color=(-10, 0, 0))
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Color value must be: (0-255, 0-255, 0-255).

    >>> draw_corners(test_image, test_corners, radius=-5)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Radius value must be greater than 0.
    """

    # Checking arguments
    check_corners(corners)
    check_radius(radius)
    check_color(color)

    img = iu.get_image(input_file)

    for i in corners:
        x, y = i.ravel()
        cv.circle(img, (x, y), radius, color, thickness)

    return img


def get_contour_area(contour):
    """
    #>>> get_contour_area(test_cnt1)
    #TODO

    >>> get_contour_area(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be None.

    >>> get_contour_area([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be void.
    """

    # Checking arguments
    check_contour(contour)

    return math.floor(cv.contourArea(contour))


def get_contour_coord(contour):
    """
    #>>> get_contour_coord(test_cnt1)
    #TODO

    >>> get_contour_coord(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be None.

    >>> get_contour_coord([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be void.
    """

    # Checking arguments
    check_contour(contour)

    return contour


def get_contour_dimension(contour, closed=1):
    """
    #>>> get_contour_dimension(test_cnt1)
    #TODO

    >>> get_contour_dimension(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be None.

    >>> get_contour_dimension([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contour can't be void.
    """

    # Checking arguments
    check_contour(contour)

    return math.floor(cv.arcLength(contour, closed))


def get_corner_number(input_file, max_corners=10, min_dist=20, trust_val=0.2):
    """
    #>>> get_corner_number(test_image)
    #TODO

    >>> get_corner_number(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be a None object

    >>> get_corner_number("")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: The input file can't be ''.

    >>> get_corner_number("fakeRoute")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IOError: Input file not found.

    >>> get_corner_number(test_image, max_corners=-10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Max_corners value must be greater than 0.

    >>> get_corner_number(test_image, min_dist=-10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_dist value must be greater than 0.

    >>> get_corner_number(test_image, trust_val=2)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Trust_val value must be between 0 and 1.
    """

    # Checking arguments
    check_max_corners(max_corners)
    check_min_dist(min_dist)
    check_trust_val(trust_val)

    return len(detect_corners(input_file, max_corners, min_dist, trust_val))


def get_squares(contours, min_length=1000):
    """
    #>>> get_squares(test_contours)
    #TODO

    >>> get_squares(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be None.

    >>> get_squares([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be void.

    >>> get_squares(test_contours, min_length=-100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_length value must be greater than 0.
    """

    # Checking arguments
    check_contours(contours)
    check_min_length(min_length)

    results = []

    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
        if len(approx) >= 4 and abs(get_contour_dimension(approx)) >= min_length:
            results = [approx] + results

    return results


def get_square_number(contours, min_length=1000):
    """
    #>>> get_squares(test_contours)
    #TODO

    >>> get_squares(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be None.

    >>> get_squares([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be void.

    >>> get_squares(test_contours, min_length=-100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_length value must be greater than 0.
    """

    # Checking arguments
    check_contours(contours)
    check_min_length(min_length)

    return len(get_squares(contours, min_length))


def join_contours(contours, min_dist=20):
    """
    #>>> join_contours(test_contours)
    #TODO

    >>> join_contours(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be None.

    >>> join_contours([])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Contours can't be void.

    >>> join_contours(test_contours, min_dist=-100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ValueError: Min_dist value must be greater than 0.
    """

    # Checking arguments
    check_contours(contours)
    check_min_dist(min_dist)

    length = len(contours)
    status = np.zeros((length, 1))
    for i, c1 in enumerate(contours):
        x = i
        for c2 in contours[i+1:]:
            if contours_close(c1, c2, min_dist) is True:
                val = min(status[i], status[x])
                status[x] = status[i] = val
            else:
                if status[x] == status[i]:
                    status[x] = i+1

        unified = []
        maximum = int(status.max())+1
        for i in xrange(maximum):
            pos = np.where(status == i)[0]
            if pos.size != 0:
                cont = np.vstack(contours[i] for i in pos)
                hull = cv.convexHull(cont)
                unified.append(hull)

    return unified


# CHECKING ARGUMENTS


def check_color(color):
    if len(color) == 3:
        if (color[0] < 0 or color[0] > 255 or color[1] < 0 or color[1] > 255 or
                color[2] < 0 or color[2] > 255):
            raise ValueError("Color value must be: (0-255, 0-255, 0-255).")
    else:
        raise ValueError("Color value must be: (0-255, 0-255, 0-255).")
    return 0


def check_contour(contour):

    if contour is None:
        raise ValueError("Contour can't be None.")
    if contour == []:
        raise ValueError("Contour can't be void.")
    return 0


def check_contours(contours):

    if contours is None:
        raise ValueError("Contours can't be None.")
    if contours == []:
        raise ValueError("Contours can't be void.")
    return 0


def check_corners(corners):

    if corners is None:
        raise ValueError("Corners can't be None.")
    if corners == []:
        raise ValueError("Corners can't be void.")
    return 0


def check_max_corners(max_corners):

    if max_corners <= 0:
        raise ValueError("Max_corners value must be greater than 0.")
    return 0


def check_min_dim(min_dim):

    if min_dim <= 0:
        raise ValueError("Min_dim value must be greater than 0.")
    return 0


def check_min_dist(min_dist):

    if min_dist <= 0:
        raise ValueError("Min_dist value must be greater than 0.")
    return 0


def check_min_length(min_length):

    if min_length <= 0:
        raise ValueError("Min_length value must be greater than 0.")
    return 0


def check_radius(radius):

    if radius <= 0:
        raise ValueError("Radius value must be greater than 0.")
    return 0


def check_threshold(value):

    if value < 0 or value > 255:
        raise ValueError("All threshold values must be between 0 and 255.")

    return 0


def check_trust_val(trust_val):

    if trust_val < 0 or trust_val > 1:
        raise ValueError("Trust_val value must be between 0 and 1.")
    return 0


def check_width(width):

    if width < 0:
        raise ValueError("Width value must be greater than 0.")
    return 0