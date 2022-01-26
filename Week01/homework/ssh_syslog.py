from syslog_check import parse as syslog_parse


def get_sshd_login_counts():
    ssh_session_log = syslog_parse(
        '../../logs/Linux_2k.log',
        # this is a single string, split between lines for PEP8 compliance.
        [('(sshd\(pam_unix\)\[[0-9]{1,8}\]: session opened for user [a-z_]'
          '(?:[a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$) by \(uid=[0-9]+\))')]
        # username regex adapted from https://unix.stackexchange.com/a/435120
         )
    
    # syslog_parse returns a list of all pattern matches on a line
    # but this program will only ever have at most 1 match unless
    # someone is trying to break it
    
    pattern_matches = list()
    for match_list in ssh_session_log:
        if len(match_list) != 1:
            print("Warning: unexpected list size!", 
                  len(match_list), match_list)
        else:
            pattern_matches += match_list
            
    ssh_logins = [line.split(' ')[5] for line in pattern_matches]

    for user in set(ssh_logins):
        print(f'User {user} logged in {ssh_logins.count(user)} times.')
        

if __name__ == '__main__':
    get_sshd_login_counts()