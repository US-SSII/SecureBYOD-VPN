import glob
import os
from datetime import datetime


def process_logs():
    path = "../logs/"
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Calculate the month and year of the previous month
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    pattern = os.path.join(path, f"{previous_year:04d}-{previous_month:02d}-*.txt")
    logs_of_the_month = glob.glob(pattern)

    return logs_of_the_month


def get_integrity_faults(log_list):
    total_messages = 0
    successful_messages = 0

    for log in log_list:
        with open(log, 'r') as file:
            for line in file:
                if "info" in line.lower():
                    continue
                total_messages += 1
                if "success" in line.lower():
                    successful_messages += 1

    return total_messages, successful_messages


def calculate_successful_ratio(total_messages, successful_messages):
    return successful_messages / total_messages if total_messages > 0 else 0


def create_report():

    if not os.path.exists("../reports/"):
        os.makedirs("../reports/")

    log_list = process_logs()
    total_messages, successful_messages = get_integrity_faults(log_list)

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    report_name = f"Report-{previous_year:04d}_{previous_month:02d}.txt"
    report_file_path = os.path.join("../reports/", report_name)

    with open(report_file_path, 'w', encoding='utf-8') as report_file:
        report_file.write("=" * 50 + "\n")
        report_file.write(f"Monthly Report - {previous_month:02d}/{previous_year:04d}\n")
        report_file.write("=" * 50 + "\n\n")

        report_file.write("Total messages sent: {}\n".format(total_messages))
        report_file.write("Total complete messages: {}\n".format(successful_messages))
        report_file.write("Total non-comprehensive messages: {}\n\n".format(total_messages - successful_messages))

        report_file.write("Percentage of complete messages: {:.2%}\n\n".format(
            calculate_successful_ratio(total_messages, successful_messages)))

        report_file.write("=" * 50)
