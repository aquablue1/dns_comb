import sys
import time
import dns.resolver


# domain = 'google.com'
domain = 'ns1.auroralimaging.ca'
for _ in range(0, 60):
    answers = dns.resolver.query(domain,'A')
    # print(answers)
    for server in answers:
        print(server)
    time.sleep(1)