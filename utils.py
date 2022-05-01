import numpy as np
import sympy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# Argument of the production theory of the polynomial bases of Lagrangian polynomial bases.
def arg_prod(i, j, x):
    # Symbolic variable
    x_sim = sympy.symbols('x')
    return (x_sim - x[i]) / (x[j] - x[i]) if i != j else 1


# Generate the polynomial with the points provided.
def polynomial_generator(n, s):
    x_sym = sympy.symbols('x')
    p = np.arange(n)

    # Constructing polynomial members randomly
    a = np.random.randint(10000, 99999, size=(n - 1))
    a = np.insert(a, 0, s)

    # Polynomial represented with symbolic variables with sympy library
    poly = sum(x_sym ** p * a)
    return poly


# With the polynomial we get m points for the people for x=1,x=2,...x=n
def get_points(poly, m):
    x_sym = sympy.symbols('x')
    points_poly = np.array([np.array([i, 0]) for i in range(m)])
    for i in range(m):
        # The subs function subs the symbolic variable by i + 1 and resolve the value
        points_poly[i] = [i + 1, poly.subs(x_sym, i + 1)]
    return points_poly


# Estimate the curve generated by the Lagrangian polynomial that interpolates the data points
# num_points_estimate (int): Number of points estimated from the polynomial
def interpolation_lagrage(points_poly, num_points_estimate=100):
    x_sim = sympy.symbols('x')

    # Separate the data
    x = points_poly[:, 0]
    y = points_poly[:, 1]

    # Number of points entered
    num_points = len(points_poly)

    # Polynomial bases lj = [l1, l2, ..., lk]
    lj = []
    for k in range(num_points):
        lk = np.prod([arg_prod(i, k, x) for i in range(num_points)])
        lj.append(lk)

    # Lagrange polynomial
    pol = sum(y * lj)

    return pol


def get_secret(poly):
    x_sym = sympy.symbols('x')
    return poly.subs(x_sym, 0)


def points_to_keys(points):
    return [str(point[0]) + "k" + str(point[1]) for point in points]


def keys_to_points(keys):
    points = np.array([np.array([i, 0]) for i in range(len(keys))])
    for i in range(len(points)):
        key = keys[i]
        points[i] = [key.split('k')[0], key.split('k')[1]]
    return points


def show_keys(keys, boolean_send_email, emails):
    if not boolean_send_email:
        for i in range(len(keys)):
            print(f"Person {i} your key is {keys[i]}.")
    else:
        for i in range(len(keys)):
            send_email_with_keys(keys[i], emails[i])


def send_email_with_keys(key, mail):
    # create message object instance
    msg = MIMEMultipart()
    username = mail.split("@gmail")[0]
    message = f"Hello {username}," \
              f"\n\nHere is your key for the sharing sharing_secret. Do not forget it.\n" \
              f"Key: {key}" \
              f"\n\nBest regards." \
              f"\n\nThe Sharing Secrets Company"

    # setup the parameters of the message
    password = "sharingsecrets#100"
    msg['From'] = "sharingsecretspython@gmail.com"
    msg['To'] = mail
    msg['Subject'] = "Key from Sharing Secret"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
