# smoothie-wifi-manager

smoothie-wifi-manager is a bluetooth serial application that allows someone to connect to smoothie to configure wifi.

This allows the smoothie's wifi to be configured headlessly.

Do have a look at [smoothie](https://github.com/ackerleytng/smoothie-prototype)!

## Setup

Create a virtualenv to house python requirements

```
cd /home/pi
python3 -m venv venv
```

Install requirements

```
source venv/bin/activate
cd /home/pi/smoothie-bluetooth-serial-wifi
pip install -r requirements.txt
```

Setup services for starting on boot. See [config](https://github.com/ackerleytng/smoothie-bluetooth-serial-wifi/tree/master/config).

Install `xdotool`

```
sudo apt install xdotool
```
