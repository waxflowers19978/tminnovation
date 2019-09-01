# coding: utf-8

from email.mime.text import MIMEText
import smtplib
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string


def send_email(request):
    user = request.user
    # アクティベーションURLの送付
    current_site = get_current_site(request)
    domain = current_site.domain
    context = {
        'protocol': request.scheme,
        'domain': domain,
        'token': dumps(user.pk),
        'user': user,
    }

    subject = render_to_string('tramino/register/mail_template/create/subject.txt', context)
    message = render_to_string('tramino/register/mail_template/create/message.txt', context)

    user.email_user(subject, message)
    return



