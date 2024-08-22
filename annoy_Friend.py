
#Sample code for message spammer

import smtplib
import time

FROM_EMAIL = "EMAIL"
TO_EMAIL = "EMAIL" #Phone numers are abled to be used as emails. Varies for each provider
PASSWORD = "PASSWORD"
message = "MESAGE"
# Create the SMTP session
server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server with port 587
server.starttls()  

try:
    # Login to the email account
    server.login(FROM_EMAIL, PASSWORD)
    print("Login successful")

    # Send the email every second for 30 seconds
    for i in range(30):
        server.sendmail(FROM_EMAIL, TO_EMAIL, message)
        print(f"Email {i+1} sent successfully")
        time.sleep(1)

except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    # Terminate the SMTP session
    server.quit()