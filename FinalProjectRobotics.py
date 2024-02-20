import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox


def create_root_and_canvas():
    """
    Create a canvas and root for our program taking advantage of tkinter lib
    :return: A tuple (tk_root, tk_canvas) representing the root and canvas created
    """
    # Create the main window
    tk_root = tk.Tk()
    tk_root.title("2D Robotic System")

    # Calculate 80% of the screen width and height
    screen_width = tk_root.winfo_screenwidth()
    screen_height = tk_root.winfo_screenheight()
    width = int(screen_width * 0.8)
    height = int(screen_height * 0.8)

    # Set the window size
    tk_root.geometry(f"{width}x{height}")

    # Create a canvas for drawing
    tk_canvas = tk.Canvas(tk_root, bg="white", width=width, height=height)
    tk_canvas.pack(expand=True, fill=tk.BOTH)

    return tk_root, tk_canvas


def draw_axes():
    """
    Draw X,Y axes to canvas
    """
    # Retrieve width, height from created canvas
    width, height = get_canvas_width_height()
    # Draw axes
    canvas.create_line(width / 2, 0, width / 2, height, fill="green")  # y-axis
    canvas.create_line(0, height / 2, width, height / 2, fill="green")  # x-axis


def draw_workspace_circles(l1, l2):
    """
    Draw the necessary workspace circles
    :param l1: The arm length L1
    :param l2: The arm length L2
    """
    # Get the center of the canvas
    center_x, center_y = get_center_xy()

    # Get internal and external radius
    ext_r, int_r = get_workspace_radius(l1, l2)

    # Coordinates for the smaller circle
    small_circle_coords = (center_x - int_r, center_y - int_r, center_x + int_r, center_y + int_r)

    # Coordinates for the larger circle
    large_circle_coords = (center_x - ext_r, center_y - ext_r, center_x + ext_r, center_y + ext_r)

    # Draw the smaller circle filled with yellow and outlined in blue
    canvas.create_oval(small_circle_coords, fill='yellow', outline='blue')

    # Draw the larger circle, outlined in blue
    canvas.create_oval(large_circle_coords, outline='blue')


def get_canvas_width_height():
    """
    Retrieve defined canvas width and height
    :return: A tuple (width, height) representing the dimensions of the defined canvas
    """
    return canvas.winfo_width(), canvas.winfo_height()


def get_user_input_data():
    """
    Get L1, L2, clock-wise as 1 or counter clock-wise move as 0, (x2, y2) coordinates from User
    :return: A tuple (l1, l2, direction, x2, y2) representing the initial necessary input from User
    """
    # Get L1, L2
    l1, l2 = get_arm_lengths_input("Give arm length")
    # Get arm direction in format 0,1
    direction = get_arm_direction_input()
    # Get (x2, y2)
    x2, y2 = get_arm2_coordinates(l1, l2)

    return l1, l2, direction, x2, y2


def get_arm_lengths_input(message):
    """
    Pop-up for input data L1, L2 with integer and screen check
    :param message: The desired message to print in pop up window
    :return: A tuple (l1, l2) representing the arm lengths
    """
    while True:
        # Get L1 and L2 while checking for proper integer format
        l1 = abs(ask_int_number_input(message + " L1"))
        l2 = abs(ask_int_number_input(message + " L2"))

        # Check that L1, L2 greater than 0, and that L1,L2 fit the canvas
        if l1 > 0 and l2 > 0 and check_arm_lengths_fit_canvas(l1, l2):
            break
        else:
            messagebox.showerror("Length error", "Length outside canvas or 0. Press OK to re enter values")

    print(f"Arm length L1: {l1}")
    print(f"Arm length L2: {l2}")
    return l1, l2


def get_arm_direction_input():
    """
    Get direction of arm turn
    :return: The number 1 for clockwise or 0 for counterclockwise direction
    """
    # Ask a yes/no question - Returns boolean True if Yes is clicked - False if No is clicked
    response = messagebox.askyesno("Choose Direction", "Is the direction clockwise?")

    # Convert the response to 1 for Yes (clockwise) and 0 for No (counterclockwise)
    if response:
        print("Direction: Clockwise")
        return 1
    else:
        print("Direction: Counterclockwise")
        return 0


def get_arm2_coordinates(l1, l2):
    """
    Get arm2 coordinates (x2, y2), while checking if they are inside in the valid workspace
    :param l1: The arm length L1
    :param l2: The arm length L1
    :return: A tuple (x2, y2) representing the valid arm2 coordinates
    """
    while True:
        x2 = ask_int_number_input("Give coordinate x2 for arm 2")
        y2 = ask_int_number_input("Give coordinate y2 for arm 2")

        # Make sure that (x2, y2) is not (0, 0) as this would destroy robot
        if (x2, y2) == (0, 0):
            messagebox.showerror("Coordinates error", "Coordinates (x2,y2) cannot be (0, 0). "
                                                      "Press OK to re enter values")
            continue

        # Check if (x2, y2) inside workspace
        if are_coords_inside_workspace(l1, l2, x2, y2):
            break
        else:
            messagebox.showerror("Coordinates error", "Coordinates not inside workspace. Press OK to re enter values")

    print(f"Coordinates (x2, y2): ({x2}, {y2})")
    return x2, y2


def are_coords_inside_workspace(l1, l2, x, y):
    """
    Check if provided (x, y) coordinate is inside workspace
    :param l1: The arm1 length
    :param l2: The arm2 length
    :param x: The x coordinate to check
    :param y: The y coordinate to check
    :return: Boolean True if provided (x, y) is inside workspace or False if not
    """
    # Retrieve the R and r radius
    ext_r, int_r = get_workspace_radius(l1, l2)

    # Check booleans by computing specific functions for R and r
    is_lower_ext_radius = x ** 2 + y ** 2 < ext_r ** 2
    is_higher_int_radius = x ** 2 + y ** 2 > int_r ** 2

    if is_lower_ext_radius and is_higher_int_radius:
        return True
    else:
        return False


def get_arm1_coords(l1, l2, x2, y2):
    """
    Compute the 2 different coordinate solutions for arm1
    :param l1: The arm length L1
    :param l2: The arm length L2
    :param x2: The coordinate x2 from arm2
    :param y2: The coordinate y2 from arm2
    :return: A tuple (x1a, y1a, x1b, y1b) representing the different coordinate solutions for arm1
    """
    # Compute the variable c from provided lab notes
    c = (y2 ** 2 + x2 ** 2 + l1 ** 2 - l2 ** 2) / 2

    # Compute the 2 possible coordinate solutions from provided lab notes
    if x2 != 0:
        # Compute delta from provided lab notes
        delta = (4 * c ** 2 * y2 ** 2) - 4 * ((y2 ** 2 + x2 ** 2) * (c ** 2 - (l1 ** 2 * x2 ** 2)))

        y1a = (2 * c * y2 + math.sqrt(delta)) / (2 * (x2 ** 2 + y2 ** 2))
        x1a = calculate_arm1_x1(c, y1a, x2, y2)

        y1b = (2 * c * y2 - math.sqrt(delta)) / (2 * (x2 ** 2 + y2 ** 2))
        x1b = calculate_arm1_x1(c, y1b, x2, y2)
    else:
        # We are safe from arm_y2 = 0, as arm_x2 is already 0 and this combination (0, 0) has already been excluded
        # in previous step
        y1a = c / y2
        x1a = math.sqrt(l1 ** 2 - (c ** 2 / y2 ** 2))

        y1b = y1a
        x1b = -x1a

    print(f"Coordinate solution (x1a, y1a): ({x1a}, {y1a})")
    print(f"Coordinate solution (x1b, y1b): ({x1b}, {y1b})")
    return x1a, y1a, x1b, y1b


def calculate_arm1_x1(c, y1, x2, y2):
    """
    Compute arm1 x1 coordinate when x2 from arm2 is not 0
    :param c: The stable c number as defined in robotics lab notes
    :param y1: The coordinate y1 from arm1
    :param x2: The coordinate x2 from arm2
    :param y2: The coordinate y2 from arm2
    :return: The coordinate x1 from arm1
    """
    return (c - (y2 * y1)) / x2


def get_single_arm1_coords_from_direction(x2, y2, x1a, y1a, x1b, y1b, direction):
    """
    Pick a single arm1 coordinates from the double coordinate solutions according to user's desire
    :param x2: The x2 coordinate of arm2
    :param y2: The y2 coordinate of arm2
    :param x1a: The x1a coordinate of arm1
    :param y1a: The y1a coordinate of arm1
    :param x1b: The x1b coordinate of arm1
    :param y1b: The y1b coordinate of arm1
    :param direction: The user's picked direction
    :return: A tuple (x1, y1) representing arm1's coordinates
    """
    # Calculate negative f1 for (arm_x1b, arm_y1b)
    f1 = - atn2(x1b, y1b)

    # Calculate new coordinates in the new system - First move and then rotate
    x2_move = x2 - x1b
    y2_move = y2 - y1b

    x2_rot = (x2_move * math.cos(f1)) - (y2_move * math.sin(f1))
    y2_rot = (x2_move * math.sin(f1)) + (y2_move * math.cos(f1))

    # Calculate f2 for (x2_rot, y2_rot) - Enough to make final decision on arm1 coordinates
    f2 = atn2(x2_rot, y2_rot)

    # Check if f2 is left or right turn view
    if 0 < f2 < math.pi:
        # Counterclockwise
        turn_view = 0
    else:
        # Clockwise
        turn_view = 1

    # Check what the user picked as desired direction
    if direction == turn_view:
        print_arm1_coordinates(x1b, y1b)
        return x1b, y1b
    else:
        print_arm1_coordinates(x1a, y1a)
        return x1a, y1a


def draw_robotic_arm(x1, y1, x2, y2):
    """
    Draw the final robotic arm as for the given arm1 and arm2 coordinates
    :param x1: The x1 coordinate of arm1
    :param y1: The y1 coordinate of arm1
    :param x2: The x2 coordinate of arm2
    :param y2: The y2 coordinate of arm2
    :return: A tuple (arm1, arm2, oval1, oval2) representing the robotic arm lines with the corresponding oval points
    """
    # Get the center of the canvas
    center_x, center_y = get_center_xy()

    # Translate (x1, y1) and (x2, y2) to canvas coordinates
    canvas_x1 = center_x + x1
    canvas_y1 = center_y - y1
    canvas_x2 = center_x + x2
    canvas_y2 = center_y - y2

    # Draw lines from center to (x1, y1) and (x1, y1) to (x2, y2)
    line_thickness = 3
    arm1 = canvas.create_line(center_x, center_y, canvas_x1, canvas_y1, fill="black", width=line_thickness)
    arm2 = canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="black", width=line_thickness)

    # Draw small red circles at (x1, y1) and (x2, y2)
    circle_radius = 3
    oval1 = canvas.create_oval(canvas_x1 - circle_radius, canvas_y1 - circle_radius,
                       canvas_x1 + circle_radius, canvas_y1 + circle_radius,
                       fill="red", outline="red")
    oval2 = canvas.create_oval(canvas_x2 - circle_radius, canvas_y2 - circle_radius,
                       canvas_x2 + circle_radius, canvas_y2 + circle_radius,
                       fill="red", outline="red")

    return arm1, arm2, oval1, oval2


def get_user_move_arm_data(l1, l2, x2, y2):
    """
    Get new arm move coordinates (xt, yt) from User with several checks
    :param l1: The length L1 of arm1
    :param l2: The length L2 of arm2
    :param x2: The x coordinate of arm2
    :param y2: The y coordinate of arm2
    :return: A tuple (xt, yt) of valid move coordinates and the moving red line
    """
    while True:
        # Pop up message for data input from user
        xt = ask_int_number_input("Give coordinate xt for new robotic move")
        yt = ask_int_number_input("Give coordinate yt for new robotic move")

        # Init check if new desired (xt, yt) is inside workspace. If not re-enter input data
        if are_coords_inside_workspace(l1, l2, xt, yt):
            if xt != x2:
                # Calculate a and b constant values
                a = (yt - y2) / (xt - x2)
                b = y2 - a * x2
                delta = (4 * a ** 2 * b ** 2) - (4 * ((a ** 2 + 1) * (b ** 2 - (l1 - l2) ** 2)))

                # Check delta
                if delta <= 0:
                    # Check special case where L1 = L2 and move path goes through (0 , 0) coordinate point
                    # This should be treated as invalid move
                    if l1 == l2:
                        if x2 == xt * (-1) and y2 == yt * (-1):
                            line, inter_point1, inter_point2 = draw_move_scene(x2, y2, xt, yt, None, None, None, None)
                            # The following message box takes either True or False according to User's click,
                            # If True (so User clicked OK) clear the drawn line from canvas to start fresh
                            if messagebox.showerror("Coordinates error",
                                                 "Move to provided coordinates is crossing by (0, 0). "
                                                 "Press OK to re enter values"):
                                clear_from_canvas(line)
                            continue
                    # Valid move - Draw the moving red line in canvas and return (xt, yt)
                    print(f"Valid move to coordinate (xt, yt): {xt, yt}")
                    draw_move_scene(x2, y2, xt, yt, None, None, None, None)
                    return xt, yt
                else:
                    # Find the 2 intersection points (xs1, ys1) and (xs2, ys2)
                    xs1 = ((-2 * a * b) + math.sqrt(delta)) / (2 * (a ** 2 + 1))
                    ys1 = (a * xs1) + b

                    xs2 = ((-2 * a * b) - math.sqrt(delta)) / (2 * (a ** 2 + 1))
                    ys2 = (a * xs2) + b

                    # Check intersection distances and define if valid move
                    if is_valid_arm_move_as_for_distances_check(x2, y2, xt, yt, xs1, ys1, xs2, ys2):
                        # Valid move - Draw the moving red line in canvas and return (xt, yt)
                        print(f"Valid move to coordinate (xt, yt): {xt, yt}")
                        draw_move_scene(x2, y2, xt, yt, None, None, None, None)
                        return xt, yt
                    else:
                        # Invalid move - Draw the moving line intersecting with the small internal circle
                        # Once the user presses OK to pop up window, remove drawn objects from canvas
                        line, inter_point1, inter_point2 = draw_move_scene(x2, y2, xt, yt, xs1, ys1,
                                                                           xs2, ys2)
                        show_coordinates_error(inter_point1, inter_point2, line)
                        continue
            else:
                if abs(x2) > abs(l1 - l2):
                    # Valid move - Draw the moving red line in canvas and return (xt, yt)
                    print(f"Valid move to coordinate (xt, yt): {xt, yt}")
                    draw_move_scene(x2, y2, xt, yt, None, None, None, None)
                    return xt, yt
                else:
                    # Find the 2 intersection points (xs1, ys1) and (xs2, ys2)
                    xs1 = x2
                    ys1 = math.sqrt((l1 - l2) ** 2 - xs1 ** 2)

                    xs2 = x2
                    ys2 = -ys1

                    # Check intersection distances and define if valid move
                    if is_valid_arm_move_as_for_distances_check(x2, y2, xt, yt, xs1, ys1, xs2, ys2):
                        # Valid move - Draw the moving red line in canvas and return (xt, yt)
                        print(f"Valid move to coordinate (xt, yt): {xt, yt}")
                        draw_move_scene(x2, y2, xt, yt, None, None, None, None)
                        return xt, yt
                    else:
                        # Invalid move - Draw the moving line intersecting with the small internal circle
                        # Once the user presses OK to pop up window, remove drawn objects from canvas
                        line, inter_point1, inter_point2 = draw_move_scene(x2, y2, xt, yt, xs1, ys1,
                                                                           xs2, ys2)
                        show_coordinates_error(inter_point1, inter_point2, line)
                        continue
        else:
            messagebox.showerror("Coordinates error",
                                 "Move to provided coordinates is outside workspace. "
                                 "Press OK to re enter values")
            continue


def show_coordinates_error(inter_point1, inter_point2, line):
    """
    Show message error to User. If User clicks OK clear line and intersection points from canvas
    :param inter_point1: The small blue oval circle at (xs1, ys1)
    :param inter_point2: The small blue oval circle at (xs2, ys2)
    :param line: The red line connecting (x2, y2) with (xt, yt)
    """
    if messagebox.showerror("Coordinates error",
                            "Move to provided coordinates is not possible as for intersecting points. "
                            "Press OK to re enter values"):
        clear_from_canvas(line)
        clear_from_canvas(inter_point1)
        clear_from_canvas(inter_point2)


def is_valid_arm_move_as_for_distances_check(x2, y2, xt, yt, xs1, ys1, xs2, ys2):
    """
    Check if an arm move is valid as for calculated distances between arm edge coordinates,
    new desired coordinates, and the intersection points with the small round circle r
    :param x2: The x2 coordinate of arm2
    :param y2: The y2 coordinate of arm2
    :param xt: The desired x coordinate to move to
    :param yt: The desired y coordinate to move to
    :param xs1: The x coordinate of intersection 1 with small round circle r
    :param ys1: The y coordinate of intersection 1 with small round circle r
    :param xs2: The x coordinate of intersection 2 with small round circle r
    :param ys2: The y coordinate of intersection 2 with small round circle r
    :return: Boolean True if move is valid or False if not
    """
    # Compute different distances between arm points and intersections
    dis_2t = math.sqrt((yt - y2) ** 2 + (xt - x2) ** 2)
    dis_2s1 = math.sqrt((ys1 - y2) ** 2 + (xs1 - x2) ** 2)
    dis_2s2 = math.sqrt((ys2 - y2) ** 2 + (xs2 - x2) ** 2)
    dis_ts1 = math.sqrt((ys1 - yt) ** 2 + (xs1 - xt) ** 2)
    dis_ts2 = math.sqrt((ys2 - yt) ** 2 + (xs2 - xt) ** 2)

    # Find min between dis_2s1 and dis_2s2
    min_dis_2s = min(dis_2s1, dis_2s2)

    # Find min between dis_ts1 and dis_ts2
    min_dis_ts = min(dis_ts1, dis_ts2)

    # Find max between min_dis_2s and min_dis_ts
    max_dis = max(min_dis_2s, min_dis_ts)

    # Compare max_dis to dis_2t
    if max_dis > dis_2t:
        # Valid move
        return True
    else:
        return False


def draw_move_scene(x2, y2, xt, yt, xs1, ys1, xs2, ys2):
    """
    Draw in canvas the moving line and intersection points if any
    :param x2: The x2 coordinate of arm2
    :param y2: The y2 coordinate of arm2
    :param xt: The new xt coordinate of moving arm
    :param yt: The new yt coordinate of moving arm
    :param xs1: The x1 intersection coordinate if defined. Otherwise, set None
    :param ys1: The y1 intersection coordinate if defined. Otherwise, set None
    :param xs2: The x2 intersection coordinate if defined. Otherwise, set None
    :param ys2: The y2 intersection coordinate if defined. Otherwise, set None
    :return: The moving line and intersection points if any
    """
    # Get actual center xy of canvas
    center_x, center_y = get_center_xy()

    # Translate coordinates to canvas coordinates
    canvas_x2 = center_x + x2
    canvas_y2 = center_y - y2
    canvas_xt = center_x + xt
    canvas_yt = center_y - yt

    # Draw the red line
    line = canvas.create_line(canvas_x2, canvas_y2, canvas_xt, canvas_yt, fill="red")

    if xs1 is not None:
        # Translate intersection coordinates to canvas coordinates
        canvas_xs1 = center_x + xs1
        canvas_ys1 = center_y - ys1
        canvas_xs2 = center_x + xs2
        canvas_ys2 = center_y - ys2

        # Draw small green circles at the intersection points
        intersection_radius = 3  # Radius of intersection point
        point1 = canvas.create_oval(canvas_xs1 - intersection_radius, canvas_ys1 - intersection_radius,
                                    canvas_xs1 + intersection_radius, canvas_ys1 + intersection_radius,
                                    fill="blue", outline="blue")
        point2 = canvas.create_oval(canvas_xs2 - intersection_radius, canvas_ys2 - intersection_radius,
                                    canvas_xs2 + intersection_radius, canvas_ys2 + intersection_radius,
                                    fill="blue", outline="blue")

        return line, point1, point2
    else:
        return line, None, None


def clear_from_canvas(item):
    """
    Delete specific item from defined canvas
    :param item: The object to remove from canvas
    """
    canvas.delete(item)


def print_arm1_coordinates(x1, x2):
    """
    Console print the arm1 coordinates
    :param x1: The x1 coordinate of arm1
    :param x2: The y1 coordinate of arm1
    """
    print(f"Coordinates (x1, y1): ({x1}, {x2})")


def ask_int_number_input(message):
    """
    Pop-up to get an integer number by the user
    :param message: The message for the pop-up window
    :return: An integer number that the user has defined
    """
    while True:
        root.update()
        user_inp = simpledialog.askinteger(title="Input Data", prompt=message, parent=root)
        break

    return user_inp


def check_arm_lengths_fit_canvas(l1, l2):
    """
    Check if the provided arm lengths fit the opened canvas created
    :param l1: The arm length L1
    :param l2: The arm length L2
    :return: Boolean True if arm lengths fit canvas or False if not
    """
    # Get canvas size
    width, height = get_canvas_width_height()

    # Check if L1 and L2 are smaller than the canvas size when stretched
    return (l1 + l2) <= width / 2 and (l1 + l2) <= height / 2


def get_workspace_radius(l1, l2):
    """
    Calculate the external R and internal r radius for workspace
    :param l1: The arm length L1
    :param l2: The arm length L2
    :return: A tuple (ext_r, int_r) representing the external and internal workspace radius accordingly
    """
    ext_r = l1 + l2
    int_r = abs(l1 - l2)

    return ext_r, int_r


def atn2(x, y):
    """
    Angle of arm and axis OX in RAD - Copied from robotics lab notes
    :param x: The x arm coordinate
    :param y: The y arm coordinate
    :return: The angle of arm in RAD
    """
    # if the value of X moves to infinity on the y-axis
    if abs(x) < 0.0001:
        if y > 0:  # 90o or P/2
            return math.pi / 2
        else:  # 270o - P/2
            return 3 * math.pi / 2
    else:  # x greater than 0.0001
        if x > 0 and y >= 0:  # 1st quarter
            return math.atan(y / x)
        elif x > 0 > y:  # 4th quarter
            return math.atan(y / x) + 2 * math.pi
        else:
            return math.atan(y / x) + math.pi


def calculate_first_arm(x2, y2, l1, l2, direction):
    """
    Calculate the movement of the arm1 (x1, y1) while arm2 takes a new position
    :param x2: The updated x coordinate of arm2
    :param y2: The updated y coordinate of arm2
    :param l1: The fixed arm1 length L1
    :param l2: The fixed arm2 length L2
    :param direction: The chosen direction from User - 1 for clockwise and 0 for counterclockwise
    :return: A tuple (x1, y1) representing the updated coordinates of arm1
    """
    # Calculate the distance from the origin (0,0) to the second arm's endpoint
    distance = math.sqrt(x2 ** 2 + y2 ** 2)

    # Check if the point is reachable
    if distance > l1 + l2 or distance < abs(l1 - l2):
        return None, None  # The point is not reachable

    # Angle between the line connecting origin (0,0) with the second arm's endpoint and X axis
    angle_to_endpoint = math.atan2(y2, x2)

    # Use the law of cosines to find the angle between the first arm
    # and the line connecting origin (0,0) with second arm endpoint
    cos_angle = (l1 ** 2 + distance ** 2 - l2 ** 2) / (2 * l1 * distance)
    angle1 = math.acos(cos_angle)

    # Based on User's picked arm direction, the final angle between first arm and X axis will be either
    # the subtraction of angle1 from angle_to_endpoint in case of counterclockwise
    # Or the sum of angle1 and angle_to_endpoint in case of clockwise
    if direction == 0:
        # For counterclockwise
        final_angle = angle_to_endpoint - angle1
    else:
        # For clockwise
        final_angle = angle_to_endpoint + angle1

    # Calculate the new (x1, y1) for the first arm
    x1 = l1 * math.cos(final_angle)
    y1 = l1 * math.sin(final_angle)

    return x1, y1


def animate_movement(direction, arm1, arm2, x1, y1, x2, y2, xt, yt, l1, l2, steps, delay):
    """
    Function to animate the movement of robotic arm across a specific defined path
    :param direction: The chosen direction from User - 1 for clockwise and 0 for counterclockwise
    :param arm1: The robotic arm line 1
    :param arm2: The robotic arm line 2
    :param x1: The initial x coordinate of arm1
    :param y1: The initial y coordinate of arm1
    :param x2: The initial x coordinate of arm2
    :param y2: The initial y coordinate of arm2
    :param xt: The final target x coordinate of robotic movement
    :param yt: The final target y coordinate of robotic movement
    :param l1: The fixed arm1 length L1
    :param l2: The fixed arm1 length L2
    :param steps: Number of steps for the animation
    :param delay: Delay of movement for the animation
    """
    # Define the center of the canvas
    center_x, center_y = get_center_xy()

    # Calculate the increments for each animation step
    dx = (xt - x2) / steps
    dy = (yt - y2) / steps

    # Function to update the position of the arms
    def update_position(step):
        # Known variables - Coords change over the duration of animation
        nonlocal x2, y2, x1, y1

        # Update the positions
        x2 += dx
        y2 += dy

        # Calculate the new position for the first arm
        new_x1, new_y1 = calculate_first_arm(x2, y2, l1, l2, direction)

        if new_x1 is not None and new_y1 is not None:
            x1, y1 = new_x1, new_y1
            # Redraw the arms
            canvas.coords(arm1, center_x, center_y, center_x + x1, center_y - y1)
            canvas.coords(arm2, center_x + x1, center_y - y1, center_x + x2, center_y - y2)
            # Continue the animation until the final position is reached
            if step < steps:
                canvas.after(delay, update_position, step+1)

    # Start the animation
    update_position(1)


def get_center_xy():
    """
    Calculate the center x,y to be the ones of the middle of the canvas
    :return: A tuple (center_x, center_y) representing the actual center x,y (0, 0)
    """
    width, height = get_canvas_width_height()
    center_x, center_y = width // 2, height // 2

    return center_x, center_y


def run_robotic_system():
    """
    The function to run step by step the given project tasks for robotic system
    """
    # 1st Task: Ask user for input data L1, L2, Direction, (x2, y2)
    l1, l2, direction, x2, y2 = get_user_input_data()

    # 2nd Task: Draw X,Y axes
    draw_axes()

    # 3rd Task: Draw the workspace internal and external circles
    draw_workspace_circles(l1, l2)

    # 4th Task: Calculate (x1a,y1a) & (x1b,y1b) pairs of solutions
    x1a, y1a, x1b, y1b = get_arm1_coords(l1, l2, x2, y2)

    # 5th Task: Pick proper arm1 coordinate solution according to picked arm direction
    # and print robotic arm in canvas
    x1, y1 = get_single_arm1_coords_from_direction(x2, y2, x1a, y1a, x1b, y1b, direction)
    arm1, arm2, oval1, oval2 = draw_robotic_arm(x1, y1, x2, y2)

    # 6th Task: Ask user for input data (xt, yt) for straight valid robotic arm move
    xt, yt = get_user_move_arm_data(l1, l2, x2, y2)

    # 7th Task: Animate robotic arm movement - Apply some initial delay in animation to give time to observe move path
    # At the same time clear some previous defined points as not needed in movement animation
    clear_from_canvas(oval1)
    clear_from_canvas(oval2)
    root.after(2000, lambda: animate_movement(direction, arm1, arm2, x1, y1, x2, y2, xt, yt, l1, l2, 300, 10))

    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Init create a root and canvas - This will be needed to base our calculations on it
    root, canvas = create_root_and_canvas()

    # Ready to run all given tasks for robotic system
    run_robotic_system()
