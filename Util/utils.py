"""Utils that we use throughout the application. The most relevant details:

* we keep the storage ID of the current user in session.
* If we need the actual user, we read the current data for that user from
  storage.
* Route handling functions decorated with @require_login can depend on a user
  object being defined on the flask g object.
* The user object is also automatically defined as a top-level variable in the
  context for any template rendered with our template function.
"""

import os.path as pth
import logging

from flask import g, render_template


def app_logger():
    """Centralize a name for the application logger and save other modules the
    trouble of importing logger"""
    return logging.getLogger("gluten")


def user_audit_record(transcript, msg):
    """Write a user log record. Note that we assume that we are currently in a
    Flash request context."""

    user = getattr(g, 'user', None)

    base_msg = "%s: {usr:%s,name:%s,state:%s,scriptid:%s,orig_scriptid:%s}" % (
        msg,
        user.email if user else '[NOUSER]',
        user.name if user else '[NOUSER]',
        transcript.state,
        transcript.id,
        transcript.source_transcript
    )

    def tag_count(fld):
        if not fld or fld.lower() == 'unspecified':
            return 0
        else:
            return 1

    utts = transcript.utterance_list if transcript else []
    act, subact, mode, totitems = 0, 0, 0, 0

    for utt in utts:
        totitems += 1
        act += tag_count(utt['act'])
        subact += tag_count(utt['subact'])
        mode += tag_count(utt['mode'])

    app_logger().info("[[AUDIT]] %s {totitems:%d,act:%d,subact:%d,mode:%d}" % (
        base_msg,
        totitems,
        act,
        subact,
        mode
    ))


def project_file(relpath):
    """Given the path to a file relative to the project root, return the
    absolute file name."""
    # Kinda janky - we know this file is one directory up from the project
    # root, so we can work from there
    base = pth.abspath(pth.join(pth.dirname(__file__), '..'))
    return pth.join(base, relpath)


def template(template_name, **context_kwrds):
    """Helper that provides any default, base data for our templates. Note that
    if g.user is defined (which routes decorated with .auth.require_login will
    have), the user will be added to the context"""
    ctx = {
        'user': getattr(g, 'user', None)
    }
    ctx.update(context_kwrds)
    return render_template(template_name, **ctx)


def first(lst):
    """Return the first element of the given list - otherwise return None"""
    return lst[0] if lst else None
