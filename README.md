# A Simple HTTP/3 Server

This is a simple HTTP/3 server using
[hypercorn](https://pgjones.gitlab.io/hypercorn/)
and [bareASGI](https://github.com/rob-blackbourn/bareASGI).

I ran this on Ubuntu 20.04 LTS with Python 3.8 on 2020-12-05.

You will need a signed certificate and private key. There are instructions
for this [here](https://github.com/rob-blackbourn/ssl-certs).

## Usage

First create a virtual environment with Python 3.8 and activate it.

```bash
$ python3.8 -m venv .venv
$ . .venv/bin/activate
(.venv) $
```

Next install hypercorn (with http/3 support) and bareASGI.

```bash
(.venv) $ pip install hypercorn[h3] bareASGI
```

Now run the server. This must be done as root as we are using the privileged ports 80 and 443.
As quic requires TLS style encryption we must provide a certificate and a key.

Change the certificate and key path to wherever they are on your machine.

```bash
(.venv) $ sudo .venv/bin/python http3_server.py $HOME/.keys/server.crt $HOME/.keys/server.key
```

Now browse to https://<host>/index.html and the page will display the version of http
that is being served, or you can check in the network tab of the devtools in your browser.
The "protocol" column in the network tab is not visible by default. If you right click over
the columns you can select it.

The only browser I've found that works on Ubuntu 20.04 LTS at the time
of writing (2020-12-05) is the FireFox nightly build. I needed to refresh the page before
it switched to http/3.

