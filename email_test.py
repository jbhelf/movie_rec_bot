import smtplib
import ssl
from email.mime.text import MIMEText
import imaplib
import email
from email.header import decode_header
import time
import collections

#Verizon (to send texts):  XXX@vtext.com
#Verizon (to recieve): XXX@vzwpix.com

def send_email(subject, content): 
    #Content has to be in triple quotes

    port = 465

    context =  ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        email, password = "SOME EMAIL ADDRESS", "SOME PASSWORD"
        server.login(email, password)

        rec_email = ["A LIST OF RECIPIENTS"]

        msg = MIMEText(content)

        msg['Subject'] = subject
        msg['From'] = email
        msg['To'] = ", ".join(rec_email)

        server.sendmail(email, rec_email, msg.as_string())

def read_votes():
    #Set connection
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    #Log into instance
    mail.login("AN EMAIL ADDRESS", "A PASSWORD")

    #Select inbox
    status, messages = mail.select("INBOX")

    #Select specific sender (and get indices of what they sent)
    people = ['(FROM "RECIPIENT")']

    list_of_votes = []
    vote_options = ["1", "2", "3", "4"] #4 being 'random'

    for voters in people:
        #Get the mail indices recieved from them
        _, selected_mails = mail.search(None, voters)

        #Get latest email (index)
        latest_index = selected_mails[0].split()
        latest_index = (latest_index[len(latest_index) - 1])

        #Retrieve data
        _, data = mail.fetch(latest_index, '(RFC822)')
        _, bytes_data = data[0]

        #Convert to a message
        email_content = email.message_from_bytes(bytes_data)

        date_num = int(email_content["date"][5:7])
        current_day = int(time.ctime()[8:10])

        #Check if the response was from today
        if(date_num == current_day):
            for part in email_content.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                        message = part.get_payload(decode=True)
                        vote = message.decode()
                        if vote in vote_options:
                            list_of_votes.append(int(vote))

    #Tie/vote checking
    if len(list_of_votes):
        # print(list_of_votes)
        frequencies = collections.Counter(list_of_votes)
        if(len(frequencies) == 4): #1 vote per item
            winning_vote = 4
        elif(len(frequencies) == 2):
            two_case = -2
            for i in frequencies:
                if(frequencies[i] == 2):
                    two_case += 1
            if two_case == 0:
                winning_vote = 4
            else:
                winning_vote = max(frequencies, key= lambda x: frequencies[x])
        else:
            winning_vote = max(frequencies, key= lambda x: frequencies[x])
    else:
        winning_vote = 4
    mail.close()
    mail.logout()

    return winning_vote

def check_for_movie_approval():
    #Set connection
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    #Log into instance
    mail.login("AN EMAIL ADDRESS", "A PASSWORD")

    #Select inbox
    status, messages = mail.select("INBOX")

    #Select specific sender (and get indices of what they sent)
    people = ['(FROM "RECIPIENT")']

    for voters in people:
        #Get the mail indices recieved from them
        _, selected_mails = mail.search(None, voters)

        #Get latest email (index)
        latest_index = selected_mails[0].split()
        latest_index = (latest_index[len(latest_index) - 1])

        #Retrieve data
        _, data = mail.fetch(latest_index, '(RFC822)')
        _, bytes_data = data[0]

        #Convert to a message
        email_content = email.message_from_bytes(bytes_data)

        date_num = int(email_content["date"][5:7])
        current_day = int(time.ctime()[8:10])

        for part in email_content.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    message = part.get_payload(decode=True)
                    text = message.decode()
                    if text == "movie please":
                        return True

    return False

if __name__ == "__main__":

    # send_email("", "")
    # read_votes()
    # print(check_for_movie_approval())
    exit(0)
