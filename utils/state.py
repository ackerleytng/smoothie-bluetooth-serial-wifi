import os
import pwd
import subprocess


def refresh_chromium():
    script_path = os.path.dirname(os.path.realpath(__file__))

    subprocess.Popen(
        [script_path + "/../refresh-chromium.sh"],
        preexec_fn=_run_as_pi,
        env={"DISPLAY": ":0"}
    )


def _run_as_pi():
    pw_record = pwd.getpwnam("pi")
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    os.setgid(user_gid)
    os.setuid(user_uid)
