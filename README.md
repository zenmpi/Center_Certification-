#Requirements
1.Python
2.The pyopenssl library.
pip install -r requirements.txt
#Usage
First generate the CA file
python CA.py --ca --cert-org example --cert-ou example
This will dump the ca keys in a folder aptly named keys
Generate the client certificate
python CA.py --client --cert-name cert_name
Generate a pfx certificate
python CA.py --pfx --cert-name cert_name

