import datetime as dt
from flask import Flask, redirect, render_template,request,flash
import smtplib,ssl,requests,os
from dotenv import load_dotenv
from post import Post
load_dotenv()
# # API_ENDPOINT = "https://api.npoint.io/1e7bda221a2e79e444fa"

# # GMAIL DEV ACCOUNT #
# GMAIL_ACCOUNT = os.getenv('MY_USERNAME')
# GMAIL_PASSWORD = os.getenv('MY_PASSWORD') # Stored as env variable
# # SMTP SERVER INFORMATION
OWN_EMAIL = os.getenv('MY_USERNAME')
OWN_PASSWORD = os.getenv('MY_PASSWORD')

# s = smtplib.SMTP(host="smtp.gmail.com", port=587)
# s.starttls()
# s.login(OWN_EMAIL,OWN_PASSWORD )

# message = f"""\
# Subject:SOMEONE wants to contact you.."""
GMAIL_SMTP_SERVER = "smtp.gmail.com"
PORT = 465
context = ssl.create_default_context() # CREATES A SECURE SSL CONTEXT

LOCAL_DATA=os.getenv('LOCAL_DATA')
JSON_URL = f"https://api.npoint.io/{LOCAL_DATA}"
posts=requests.get(JSON_URL)


app =Flask(__name__)

response=requests.get(JSON_URL)
response.raise_for_status()
blog_posts=response.json()
all_posts=[]


def getting_current_year():
    """A dummy docstring."""
    return dt.datetime.now().year
@app.route("/")
def home():
    """A dummy docstring."""
    return render_template("index.html", posts=all_posts, year=getting_current_year())

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/about")
def about():
    """A dummy docstring."""
    return render_template("about.html", year=getting_current_year())

@app.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == "POST":
        name_entry = request.form['name']
        email_entry = request.form['email']
        phone_entry = request.form['phone']
        message_entry = request.form['message']
        # MESSAGE TEMPLATE TO EMAIL #
        message = f'''Subject: Contact Inquiry\n
            Name: {name_entry}\n
            Email: {email_entry}\n
            Phone: {phone_entry}\n
            \n
            Message: {message_entry} 
            '''
        # CREATES SMTP SESSION #
        with smtplib.SMTP_SSL(GMAIL_SMTP_SERVER, PORT, context=context) as server:
            server.login(OWN_EMAIL, OWN_PASSWORD)
            server.sendmail(from_addr=GMAIL_SMTP_SERVER, to_addrs=OWN_EMAIL, msg=message)

        return render_template('contact.html', h1_entry="We have received your email!")

    return render_template('contact.html')
# def contact():
#     """A dummy docstring."""
#     return render_template("contact.html", year=getting_current_year())
# def send_email(name, email, phone, message):
#     email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(OWN_EMAIL, OWN_PASSWORD)
#         connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)
#         flash("Form Submitted Successfully...Will get back to you soon!!!")


# @app.route("/form-entry", methods=["POST"])
# def receive_data():
#     data = request.form
#     print(data["name"])
#     print(data["email"])
#     print(data["phone"])
#     print(data["message"])

#     return  render_template("contact.html")
 
        
@app.route("/contribute")
def contribute():
    """A dummy docstring."""
    return render_template("contribute.html", year=getting_current_year())


if __name__=="__main__":
    app.run(debug=True)
 
