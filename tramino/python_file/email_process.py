# coding: utf-8

from email.mime.text import MIMEText
import smtplib
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from ..models import TeamInformations, User, EventPostPool


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

def send_mail_when_event_applied(request):# message_roomで発火
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
    subject_to_guest = render_to_string('tramino/mail_template/event_apply/subject_to_guest.txt', context)
    message_to_guest = render_to_string('tramino/mail_template/event_apply/message_to_guest.txt', context)
    user.email_user(subject_to_guest, message_to_guest)

    event_id = request.POST['matchid']
    event = EventPostPool.objects.get(id=event_id)
    host_user = event.event_host_team.user
    context = {
        'protocol': request.scheme,
        'domain': domain,
        'token': dumps(host_user.pk),
        'user': host_user,
    }
    subject_to_host = render_to_string('tramino/mail_template/event_apply/subject_to_host.txt', context)
    message_to_host = render_to_string('tramino/mail_template/event_apply/message_to_host.txt', context)
    host_user.email_user(subject_to_host, message_to_host)
    return



