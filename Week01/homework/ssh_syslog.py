from syslog_check import parse as syslog_parse


def get_sshd_login_counts():
    ssh_session_log = syslog_parse(
        '../../logs/Linux_2k.log',
        # this is a single string, split between lines for PEP8 compliance.
        [('sshd\(pam_unix\)\[[0-9]{1,8}\]: session opened for user ([a-z_]'
          '(?:[a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)) by \(uid=[0-9]+\)')]
        # username regex adapted from https://unix.stackexchange.com/a/435120
    )
    matched_users = dict()
    # if the list is not 1 long, something's wrong, print warning.
    for user_list in ssh_session_log:
        #
        if len(user_list) != 1:
            print("Warning: unexpected list size!",
                  len(user_list), user_list)
        else:
            # get the only item in the list
            user = user_list[0]
            # if it's already been seen, increase the counter
            if user in matched_users.keys():
                matched_users[user] += 1
            # if it's new, create a counter and set it to 1
            else:
                matched_users[user] = 1

    for user in matched_users.keys():
        print(f'User {user} logged in {matched_users[user]} times.')


if __name__ == '__main__':
    get_sshd_login_counts()
