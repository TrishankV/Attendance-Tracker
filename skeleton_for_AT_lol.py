import calendar

def create_timetable(day, subjects_by_day):
    if day in subjects_by_day:
        timetable = subjects_by_day[day]
    else:
        timetable = []
    return timetable

def count_subjects_lectures(subjects_by_day, weeks):
    subject_lecture_count = {}

    for day, subjects in subjects_by_day.items():
        for subject in subjects:
            if subject in subject_lecture_count:
                subject_lecture_count[subject] += weeks if day != "Saturday" and day != "Sunday" else 0
            else:
                subject_lecture_count[subject] = weeks if day != "Saturday" and day != "Sunday" else 0

    return subject_lecture_count

def select_date_range_with_timetable(start_year, start_month, start_day, end_year, end_month, end_day, subjects_by_day, holidays):
    subject_lecture_count = {}
    attendance = {}
    total_lectures = 0
    total_attendance = 0
    day_names = list(calendar.day_name)
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if (year == start_year and month < start_month) or (year == end_year and month > end_month):
                continue
            month_range = calendar.monthrange(year, month)
            for day in range(1, month_range[1] + 1):
                if (year == start_year and month == start_month and day < start_day) or (year == end_year and month == end_month and day > end_day):
                    continue
                date = f"{year}-{month:02d}-{day:02d}"
                if date in holidays:
                    continue
                day_of_week = calendar.weekday(year, month, day)
                day_name = day_names[day_of_week]
                if day_name == "Saturday" or day_name == "Sunday":
                    continue
                if day_name in subjects_by_day:
                    print(f"\n{date} - {day_name}")
                    attendance_input = input("Enter 'all present', 'all absent', 'bunk lectures' or 'done': ")
                    if attendance_input.lower() == "all present":
                        total_attendance += len(subjects_by_day[day_name])
                        total_lectures += len(subjects_by_day[day_name])
                        for subject in subjects_by_day[day_name]:
                            if subject in subject_lecture_count:
                                subject_lecture_count[subject] += 1
                                attendance[subject] = attendance.get(subject, 0) + 1
                            else:
                                subject_lecture_count[subject] = 1
                                attendance[subject] = 1
                    elif attendance_input.lower() == "all absent":
                        total_lectures += len(subjects_by_day[day_name])
                        for subject in subjects_by_day[day_name]:
                            if subject in subject_lecture_count:
                                subject_lecture_count[subject] += 1
                            else:
                                subject_lecture_count[subject] = 1
                    elif attendance_input.lower() == "bunk lectures":
                        bunked_subjects_input = input("Enter the bunked lectures separated by commas (e.g. Math,Science): ")
                        bunked_subjects = [subject.strip() for subject in bunked_subjects_input.split(",")]
                        total_attendance += len(subjects_by_day[day_name]) - len(bunked_subjects)
                        total_lectures += len(subjects_by_day[day_name])
                        for subject in subjects_by_day[day_name]:
                            if subject in subject_lecture_count:
                                subject_lecture_count[subject] += 1
                                if subject not in bunked_subjects:
                                    attendance[subject] = attendance.get(subject, 0) + 1
                            else:
                                subject_lecture_count[subject] = 1
                                if subject not in bunked_subjects:
                                    attendance[subject] = 1
                    elif attendance_input.lower() == "done":
                        break

    attendance_percentage = {}
    for subject, count in attendance.items():
        total_subject_lectures = subject_lecture_count.get(subject, 0)
        percentage = (count / total_subject_lectures) * 100
        attendance_percentage[subject] = percentage

    total_attendance_percentage = (total_attendance / total_lectures) * 100

    return attendance_percentage, total_attendance_percentage

start_year = int(input("Enter the start year: "))
start_month = int(input("Enter the start month: "))
start_day = int(input("Enter the start day: "))
end_year = int(input("Enter the end year: "))
end_month = int(input("Enter the end month: "))
end_day = int(input("Enter the end day: "))

subjects_by_day = {}
day_names = list(calendar.day_name)
for day_name in day_names:
    subjects_input = input(f"Enter the subjects for {day_name} separated by commas (e.g. Math,Science): ")
    if subjects_input.strip() != "":
        subjects_by_day[day_name] = [subject.strip() for subject in subjects_input.split(",")]
    else:
        subjects_by_day[day_name] = []

holidays_input = input("Do you want to add any holidays? (yes/no): ")
holidays = []
if holidays_input.lower() == "yes" or "YES" or "Yes":
    while True:
        holiday_input = input("Enter a holiday date in YYYY-MM-DD format (or 'done' to finish): ")
        if holiday_input.lower() == "done" or "DONE" or "Done":
            break
        holidays.append(holiday_input)

attendance_percentage, total_attendance_percentage = select_date_range_with_timetable(start_year, start_month, start_day, end_year, end_month, end_day, subjects_by_day, holidays)

for subject, percentage in attendance_percentage.items():
    print(f"{subject}: {percentage:.2f}% attendance") 

print(f"\nTotal attendance: {total_attendance_percentage:.2f}%")
