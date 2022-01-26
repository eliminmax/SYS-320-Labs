from syslog_check import parse as syslog_parse

def get_klogind_auth_failures():
    
    failure_ip_matches = syslog_parse(
        '../../logs/Linux_2k.log',
    ['klogind\[[0-9]+\]: Authentication failed from .*(\(.*\))']
    )
    # return a list of lists of pattern matches per line
    # uses a regex capture group to just get the IP address in a 1-long list
    
    # if the list is not 1 long, something's wrong, print warning.
    
    matched_ips = dict()
    for ip_list in failure_ip_matches:
        if len(ip_list) != 1:
            print("Warning: unexpected list size!", 
                len(ip_list), line_matches)
        else:
            ip = ip_list[0] # it's in a list
            if ip in matched_ips.keys():
                matched_ips[ip] += 1
            else:
                matched_ips[ip] = 1
    
    # print out results
    for ip in matched_ips.keys():
        print(
            f'ip address {ip} failed to authenticate {matched_ips[ip]} times.'
        )