import smtplib as smtp


def send_mail(dest_email, email_text):

    email = "kbondar17@yandex.ru"
    password = "ouemkrnnfkbgwboo"
    subject = "registration"

    message = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(
        email, dest_email, subject, email_text
    )

    server = smtp.SMTP("smtp.yandex.com", port=587)
    server.starttls()
    server.login(email, password)

    server.sendmail(email, dest_email, message)
    server.quit()
