#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

def add_email_to_list(email):
    """Appends an email to the subscribers.txt file."""
    try:
        with open('subscribers.txt', 'a') as f:
            f.write(email + '\n')
        return True
    except Exception as e:
        return False

form = cgi.FieldStorage()
email = form.getvalue('email')

print("Content-Type: text/html")
print()

if email:
    if add_email_to_list(email):
        print("<html>")
        print("<head><title>Success</title></head>")
        print("<body>")
        print("<h2>Thank you for subscribing!</h2>")
        print(f"<p>The email address {email} has been added to our mailing list.</p>")
        print("</body>")
        print("</html>")
    else:
        print("<html>")
        print("<head><title>Error</title></head>")
        print("<body>")
        print("<h2>Error</h2>")
        print("<p>There was an error subscribing your email. Please try again later.</p>")
        print("</body>")
        print("</html>")
else:
    print("<html>")
    print("<head><title>Error</title></head>")
    print("<body>")
    print("<h2>Error</h2>")
    print("<p>No email address was provided.</p>")
    print("</body>")
    print("</html>")
