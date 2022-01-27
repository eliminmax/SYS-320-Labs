from syslog_check import parse as syslog_parse


def get_klogind_auth_failures():

    failure_ip_matches = syslog_parse(
        '../../logs/Linux_2k.log',
        ['klogind\[[0-9]+\]: Authentication failed from .*(\(.*\))']
    )
    # returns a list of lists of pattern matches per line
    # uses a regex capture group to just get the IP address in a 1-long list

    matched_ips = dict()
    # if the list is not 1 long, something's wrong, print warning.
    for ip_list in failure_ip_matches:
        if len(ip_list) != 1:
            print("Warning: unexpected list size!",
                  len(ip_list), line_matches)
        else:
            # get the only item in the list
            ip = ip_list[0]
            # if it's already been seen, increase the counter
            if ip in matched_ips.keys():
                matched_ips[ip] += 1
            # if it's new, create a counter and set it to 1
            else:
                matched_ips[ip] = 1

    # print out results
    for ip in matched_ips.keys():
        print(
            f'ip address {ip} failed to authenticate {matched_ips[ip]} times.'
        )


if __name__ == '__main__':
    get_klogind_auth_failures()
