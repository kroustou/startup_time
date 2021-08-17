#!/usr/bin/env python3
import argparse
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def startup_time(service="nxengine", logs_file=None, time_format="%b  %d %H:%M:%S"):
    """
    Parse logs and find the startup time of the given service
    """
    if logs_file is None:
        msg = "No logfile given"
        logging.error(msg)
        raise Exception(msg)
    events = {"starting": [], "running": []}
    logging.info("Starting the script with arguments: %s %s", service, logs_file)
    try:
        with open(os.path.abspath(logs_file)) as logs:
            for log in logs.readlines():
                # do we care about this line?
                if f"starting {service}" in log or f"{service} is running" in log:
                    # yes we do
                    logging.debug("Line %s matches", log)
                    time = datetime.strptime(log.split(service)[0].strip(), time_format)
                    for event in events.keys():
                        if event in log:
                            # in case we get a running event before starting
                            if event == "running" and not events["starting"]:
                                continue
                            events[event].append(time)
                            continue
    except Exception as e:
        logging.error("Could not read log file %s: %s", logs_file, e)
    result = [
        done - start for start, done in zip(events["starting"], events["running"])
    ]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get startup time for the given service."
    )
    parser.add_argument(
        "--service", type=str, help="the name of the service", default="nxengine"
    )
    parser.add_argument(
        "--logs_file",
        type=str,
        help="the path of the logs file",
        default="../../Quiz data/Question1/engine.log",
    )
    parser.add_argument(
        "--time_format",
        type=str,
        help="the format of the time on each line",
        default="%b  %d %H:%M:%S",
    )
    # TODO add argument for verbosity
    args = parser.parse_args()
    result = startup_time(args.service, args.logs_file, args.time_format)
    for cycle, duration in enumerate(result, 1):
        seconds = duration.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        print(f"Start Cycle: {cycle} Duration: {hours:02}:{minutes:02}:{seconds:02}")
