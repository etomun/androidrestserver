#cd visitmarthapura

# Pull the latest changes from the GitHub
git pull origin master

# Set deploy.sh executable
chmod +x deploy.sh

# Set domain name using dnsmasq
dnsmasq -C ~/visitmarthapura/.local-dns.conf


