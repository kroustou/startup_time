# Startup time script
This script will parse a given log file for a given service and output the time it took for it to start, based on the given logs.

## Usage
Below is the usage, defaults are:

- service: nxsengine
- logs_file: ../../Quiz data/Question1/engine.log
- time_format: the format of the engine.log file

``` sh
usage: startup_time.py [-h] [--service SERVICE] [--logs_file LOGS_FILE] [--time_format TIME_FORMAT]

Get startup time for the given service.

optional arguments:
  -h, --help            show this help message and exit
  --service SERVICE     the name of the service
  --logs_file LOGS_FILE
                        the path of the logs file
  --time_format TIME_FORMAT
                        the format of the time on each line
```

Practically for the quiz, no arguments should be given, but the script was designed this way in order to be robust and not limited to the specific service or file or format.

## Sample output

``` sh
Start Cycle: 1 Duration: 00:00:02
Start Cycle: 2 Duration: 01:40:50
```


## Tests
One can run the tests using:

``` sh
./test_startup_time.py
```
