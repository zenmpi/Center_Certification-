# Center certification 

This certification center is based on bot telegrams. 
This bot issues certificates for encrypting letters in Outlook.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```
And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

* Python
* The pyopenssl library.
* pip install -r requirements.txt
### Usage
* First generate the CA file
* python ssl_gen.py --ca --cert-org example --cert-ou example
* This will dump the ca keys in a folder aptly named keys
* Generate the client certificate
* python ssl_gen.py --client --cert-name cert_name
* Generate a pfx certificate
* python ssl_gen.py --pfx --cert-name cert_name



## Built With

* [OpenSSL](https://www.pyopenssl.org/en/stable/api.html) - The library encryption
* [Telebot](https://pypi.org/project/pyTelegramBotAPI/0.3.0/) - The library for create bot in telegram

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Karlinsky Yaroslav** - [Telegram contact](https://telegram.me/Karlinsky_Yaroslav)


## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
