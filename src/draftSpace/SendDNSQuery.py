import dns.resolver


domain = 'google.com'
domain = 'www.cpsc.ucalgary.ca'
answers = dns.resolver.query(domain,'A')
print(answers)
for server in answers:
    print(server)