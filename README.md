# Swampert Reloaded
> Non è finita finchè non è finita


## Prologue
Swampert Reloaded is a project born from the original [Swampert](https://github.com/DanieleDifra/Swampert), a home project made to remotely water balcony plants during the hot Milanese summers. It consists in a RaspberryPi used to control a pump and electrovalves driven by a handy Telegram Bot.


## Usage
SSH can be used to access the Raspberry

```
ssh -Y swampi@192.168.1.230
```

Nothing should be actually done, the functioning of the telegramBot is granted by its starting script `runScript.sh`

Logs and graphs about the system can be found [here](https://thingspeak.com/channels/1806671)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Already planned improvements:
* Docker/Kubernetes for scalability and resilience of the Telegram Bot instance

## Authors
* **Daniele Di Francesco** - *Main author* - [Github](https://github.com/DanieleDifra)
* **Luca Franceschini** - *Mention of honor* - [Github](https://github.com/biboluke)