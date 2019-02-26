import sys
import time
import dns.resolver


# domain = 'google.com'
domain = 'auroralimaging.ca'
for _ in range(0, 100):
    answers = dns.resolver.query(domain,'NS')
    # print(answers)
    for server in answers:
        print(server)
    time.sleep(1)