# -*- coding: utf-8 -*-

import os
from . import email_utils


class Staff(object):
    """ Represent an supported staff.

    Attributes:
        name (:obj:`str`): Staff name.

        addr (:obj:`str`): Email address.
    """

    def __init__(self, name, addr):
        self.name = name
        self.addr = addr


class SimpleEmail(object):
    """ Sending email notifications in an easy way.

    Attributes:
        attachement_root (:obj:`str`): Attachment path on the server, e.g. http://www.domain.com/result/attachment.

        from_addr (:obj:`str array`): Sender address.

        from_name (:obj:`str`): Send name alias to the sender email address.

        subject_prefix (:obj:`str`): Prefix of subject.

        support_staffs (:obj:`str`): Supported staffs.
    """

    def __init__(self, attachment_root,
                 from_addr='autotest@ruijie.com.cn',
                 from_name=u'自动化测试系统',
                 subject_prefix=u'自动化测试系统',
                 support_staffs=None):
        self.subject_prefix = subject_prefix
        self.from_name = from_name
        self.attachment_root = attachment_root
        self.support_staffs = support_staffs
        self.from_addr = from_addr

    def __is_attachment_ok(self, path):
        size = os.path.getsize(path)
        if size > 20 * 1024 * 1024:
            return False
        return True

    def send(self, to_addrs,
             subject,
             message,
             attachments=None):
        """ Send email notification.

        Args:

            to_addrs (:obj:`str array`): Receivers' email address.

            subject (:obj:`str`): Email title.

            message (:obj:`str`): notification message.

            attachments (:obj:`str`): Attachements.

        Example::

            SimpleEmail(attachment_root='http://192.168.1.1/result/attachement',
                support_staffs=[
                    Staff(name=u'Tom', addr='tom@landicorp.com'),
                    Staff(name=u'Jerry', addr='jerry@landicorp.com'),
                ]
            ).send(to_addrs=['linw@landicorp.com'], 
                    subject=u'A8 UI testing result',
                    message=u'All tests pass!',
                    attachments=[
                        Attachment(path='result.txt'),
                        Attachment(path='result-2.zip'),
                    ]
            )
        """

        title = u"""[{}]{}'""".format(self.subject_prefix, subject)

        valid_attachments = []
        invalid_attachments = []
        for atta in attachments:
            if not self.__is_attachment_ok(atta.path):
                invalid_attachments.append(atta)
                continue
            valid_attachments.append(atta)

        body = u"""
        <p>{message}</p>
        """.format(message=message)

        if invalid_attachments:
            body = u"""
            {body}
            <p>以下附件由于超过邮件服务器附件大小限制无法发送，点击链接获取原始文件：</p>
            """.format(body=body)
            for atta in invalid_attachments:
                body = u"""
                {body}
                <p><a href="{atta_root}/{atta_path}">{atta_name}</a></p>
                """.format(body=body, atta_root=self.attachment_root, atta_path=atta.path, atta_name=atta.name)

        if self.support_staffs is not None:
            body = u"""
            {body}
            <p>如有任何疑问，请联系以下支持人员：</p>
            <ul>
            """.format(body=body)
            for staff in self.support_staffs:
                body = u"""
                {body}
                <li><a href="mailto:{staff_email}">{staff_name}</a></li>
                """.format(body=body, staff_email=staff.addr, staff_name=staff.name)
            body = u"""
            {body}
            </ul>
            """.format(body=body)

        body = email_utils.Email.create_message(subject=title, body=body,
                                                from_name=self.from_name, body_type='html',
                                                attachments=valid_attachments)
        email_utils.Email(from_addr=self.from_addr,
                          to_addrs=to_addrs, message=body).notify()
