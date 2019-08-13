import datetime
import glob
import os
from time import sleep

from loguru import logger
from playsound import playsound
import gui
from resources.sounds.sound_resources import no_plan_alarm, alarm


def main():
    shown_times = []

    logger.debug("Work plan started")

    while True:
        plan_file, error_message = find_plan_file(os.getcwd())

        if plan_file is None:
            logger.warning(f"No plan file found")
            playsound(no_plan_alarm)
            gui.alert("Error", error_message)

            sleep(20)
        else:
            time_with_activity = get_activities(plan_file)

            now = datetime.datetime.now()
            from_time, to_time = get_current_time_range(time_with_activity.keys(), now)


            if from_time is None:
                logger.warning("No defined activity")

                playsound(no_plan_alarm)
                gui.alert("Error", "No activity is planned")
                sleep(20)

            elif to_time is None:
                logger.warning("No defined activity end")

                playsound(no_plan_alarm)
                gui.alert("Error", f"Activity {time_with_activity[from_time]} starting at {from_time.strftime('%H:%M')}"
                               f" has no defined end")
                sleep(20)

            elif (to_time - from_time).total_seconds() > 60 * 60:
                logger.warning("Activity is too long (max duration is one hour)")

                playsound(no_plan_alarm)
                gui.alert("Error", "Activity is too long (maximally one hour is allowed)")
                sleep(20)

            elif from_time not in shown_times:
                logger.info(f"{from_time.strftime('%H:%M')} - {to_time.strftime('%H:%M')}: {time_with_activity[from_time]}")

                shown_times.append(from_time)
                playsound(alarm)
                gui.alert(f"{from_time.strftime('%H:%M')} - {to_time.strftime('%H:%M')}", time_with_activity[from_time],
                          timeout=None)
                sleep(5)

            else:
                sleep(5)


def get_current_time_range(activity_times, now):
    lesser_equal = None
    greater = None

    for time in activity_times:
        if time <= now and (lesser_equal is None or time > lesser_equal):
            lesser_equal = time
        elif now < time and (greater is None or greater > time):
            greater = time

    return lesser_equal, greater


def get_activities(plan_file):
    date = os.path.splitext(os.path.basename(plan_file))[0]

    activities = open(plan_file, 'r', encoding="utf8").readlines()
    time_with_activity_str = {line[0]: " - ".join(line[1:]) for line in
                          [line.strip().split(" - ") for line in activities if line.strip() != ""]
                          if len(line) >= 2}

    time_with_activity = {}
    for time_str, activity in time_with_activity_str.items():
        try:
            time = datetime.datetime.strptime(f"{date}T{time_str}", "%Y-%m-%dT%H:%M")
            time_with_activity[time] = activity
        except Exception as error:
            pass
            easygui.msgbox(str(error), title="Error")

    return time_with_activity


def find_plan_file(plan_directory):
    plan_files = glob.glob(f"{plan_directory}/**/*.txt", recursive=True)

    matching_files = [file for file in plan_files if
                     f"{datetime.datetime.now().date()}.txt" in file]

    result_plan_file = None
    error_message = None

    if len(matching_files) == 1:
        result_plan_file = matching_files[0]
    elif len(matching_files) > 1:
        error_message = f"Multiple plan files for today!\n{matching_files}"
    else:
        error_message = "No plan file for today"
    return result_plan_file, error_message


if __name__ == '__main__':
    main()
