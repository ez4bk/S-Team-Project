# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

ruijie_mail_url = "casfz.ruijie.com.cn"


class Attachment(object):
    """ Represent an email attachment.

    Attributes:
        name (:obj:`str`): Attachment name to show in the email, default set to file name.

        path (:obj:`str`): Path to the attachment.
    """

    def __init__(self, path, name=''):
        self.name = name
        self.path = path
        if self.name == '':
            self.name = os.path.basename(os.path.normpath(path))


class Image(object):
    """ Represent an image of the email body.

    Attributes:
        name (:obj:`str`): Image ID used to reference to the image in html body.
        
        path (:obj:`str`): Image path.
    """

    def __init__(self, path, name=''):
        self.name = name
        self.path = path
        if self.name == '':
            self.name = os.path.basename(os.path.normpath(path))


class Email(object):
    """ Sending email notifications.

    Attributes:
        from_addr (:obj:`str`): Sender address.

        to_addrs (:obj:`str array`): Receiver address.

        message (:obj:`str`): notification message.
    """

    def __init__(self, from_addr, to_addrs, message):
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.message = message

    '''
    Create a message with given 
    '''

    @staticmethod
    def create_message(subject,
                       body,
                       from_name='',
                       body_type='plain',
                       images=None,
                       attachments=None):
        """ Create email message.

        Args:

            subject (:obj:`str`): Message subject.

            body (:obj:`str`): Message body.

            body_type (:obj:`str`): MIME type of body, ``plain`` for plain text or ``html`` for html content.

            from_name (:obj:`str`, optional): Aliases of the address of email sender.

            images (:obj:`Image` array): Images to show in html body.

            attachments (:obj:`Attachment` array): Attachments.

        Returns:

            :obj:`MIMEMultipart` instance.

        Example:

            1. To create a email message with:

                - default sender address as from name
                - plain text body
                - two text attachment::
        
                    Email.create_message(subject='This is a demo email notification',
                                        body='This email notification is just a test demo!',
                                        body_type='plain',
                                        attachments=[
                                            Attachment(path='result.txt'),
                                            Attachment(path='result-2.txt'),
                                        ])

            2. To create a email message with:

                - aliases from name
                - html body with image
                - two text attachment::

                    Email.create_message(subject='Email notification demo',
                                        body_type='html',
                                        body=\"\"\"
                                            <p><a href="https://www.google.com"> This is an email notification!</a></p>
                                            <img src="cid:logo" alt="python logo" />
                                            \"\"\",
                                        images=[
                                            Image(name='logo', path='python-logo.png'),
                                        ],
                                        attachments=[
                                            Attachment(path='result.txt'),
                                            Attachment(path='result-2.txt'),
                                        ])
        """

        if images is None:
            images = []
        if attachments is None:
            attachments = []
        message = MIMEMultipart()
        if from_name != '':
            message['From'] = Header(from_name, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(body, body_type, 'utf-8'))

        for atta in attachments:
            mt = MIMEText(open(atta.path, 'rb').read(), 'base64', 'utf-8')
            mt["Content-Type"] = 'application/octet-stream'
            mt["Content-Disposition"] = 'attachment; filename="{}"'.format(atta.name)
            message.attach(mt)

        for img in images:
            fp = open(img.path, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            msgImage.add_header('Content-ID', '<{}>'.format(img.name))
            message.attach(msgImage)

        return message

    def notify(self):
        """ Send email notification.
        """
        smtp = smtplib.SMTP(host=ruijie_mail_url)
        smtp.sendmail(self.from_addr, self.to_addrs, self.message.as_string())
        print('send email successfully!')
