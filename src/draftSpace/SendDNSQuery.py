import sys
import time
import dns.resolver


# domain = 'www.google.com'
domain = 'auroralimaging.com'
# domain = 'cpsc.ucalgary.ca'
domain = "madrigal.phys.ucalgary.ca"
my_resolver = dns.resolver.Resolver(configure=False)
my_resolver.nameservers = ["136.159.142.5"]
for _ in range(0, 1):
    try:
        answers = my_resolver.query(domain,'A')
        # print(answers)
        # for server in answers:
            # print(server.to_text(origin=True))
        print(answers.response)
    except:
        print("Error Info")
    finally:
        time.sleep(1)
        # dns.resolver.reset_default_resolver()