from datetime import datetime
from time import sleep
from os import getlogin
from sys import stdout


def converting_datetime(from_date, to_date, from_time='0.0', to_time='0.0') -> tuple:
    """ To datetime object from format DD.MM HH:MM """
    try:
        from_datetime = datetime.strptime(from_date + from_time, '%d.%m%H.%M')
        to_datetime = datetime.strptime(to_date + to_time, '%d.%m%H.%M')
        return from_datetime, to_datetime
    except ValueError:
        stdout.write('[!] Wrong month [!]')


def filter_dates(from_date, to_date, from_email, to_email, line) -> bool:
    """ Filtering by date and e-mails"""
    date_filter = from_date <= datetime.strptime(line[:15], '%b %d %H:%M:%S') <= to_date
    from_email_filter = True if from_email == '' else any([f'from=<{from_email}' in line[27:].lower(),
                                                           f'from <{from_email}' in line[27:].lower()])
    to_email_filter = True if to_email == '' else any([f'to=<{to_email}' in line[27:].lower(),
                                                       f'to <{to_email}' in line[27:].lower()])
    return all([date_filter, from_email_filter, to_email_filter])


def main(date_1, date_2, sent_to, received_from) -> None:
    """Analyzing mail.log and printing"""
    from_date, to_date = converting_datetime(date_1, date_2)
    sender, receiver = sent_to.lower(), received_from.lower()

    try:
        with open(f'C:/Users/{getlogin()}/Downloads/mail.log', 'r', encoding='ANSI') as logfile:
            stdout.write('|   Date  |   Time   | Log record')
            data = (line for line in logfile)
            for line in data:
                if filter_dates(from_date, to_date, sender, receiver, line):
                    stdout.write(f'| {line[:4]}{line[4:6]}  | {line[7:15]} | {line[25:]}')
            stdout.write('\n')
    except FileNotFoundError or FileExistsError:
        stdout.write('Check your downloads. Maillog should be at path: C:/Users/***yourlogin***/Downloads\n')

    # запись в отдельный файл result.txt
    # with open(f'C:/Users/{getlogin()}/Downloads/mail.log', 'r', encoding='ANSI') as logfile, \
    #         open(f'C:/Users/{getlogin()}/Downloads/result.txt', 'w', encoding='UTF-8') as result:
    #         result.write('|   Date  |   Time   | Log record\n')
    #         generator = (line for line in logfile)
    #         for line in generator:
    #             if filter_dates(from_date, to_date, sender, receiver, line):
    #                 result.writelines(f'| {line[:4]}{line[4:6]}  | {line[7:15]} | {line[25:]}')


if __name__ == '__main__':
    stdout.write(f"[!] Hello, {getlogin()}! I'm Kaspersky Log Analyzer! [!]\n"
                 f"[!] Please, note that date/time should be at Day.Month format [!]\n\n")

    while True:
        main(input('Searching date from\nDate (Dd.Mm): '), input('Searching date to\nDate (Dd.Mm): '),
             input('Sender (optional): '), input('Receiver (optional): '))
        if input('[!] Another one (y/n)?: ') == 'y':
            continue
        else:
            stdout.write('Have a nice day!\nClosing...')
            sleep(1)
            break




