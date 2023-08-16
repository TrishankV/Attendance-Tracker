import csv
import calendar

class Timetable:
    def __init__(self, subjects_by_day=None):
        if subjects_by_day is None:
            self.subjects_by_day = {}
        else:
            self.subjects_by_day = subjects_by_day

    def create_timetable(self, day):
        if day in self.subjects_by_day:
            timetable = self.subjects_by_day[day]
        else:
            timetable = []
        return timetable

    def count_subjects_lectures(self, weeks):
        subject_lecture_count = {}

        for day, subjects in self.subjects_by_day.items():
            for subject in subjects:
                if subject in subject_lecture_count:
                    subject_lecture_count[subject] += weeks if day != "Saturday" and day != "Sunday" else 0
                else:
                    subject_lecture_count[subject] = weeks if day != "Saturday" and day != "Sunday" else 0

        return subject_lecture_count

    def read_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                day = row[0]
                subjects = row[1:]
                self.subjects_by_day[day] = subjects

    def update_timetable(self, day, subjects):
        self.subjects_by_day[day] = subjects

class AttendanceTracker:
    def __init__(self, start_year, start_month, start_day, end_year, end_month, end_day, timetable_filename, holidays):
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.timetable_filename = timetable_filename
        self.holidays = holidays

    def select_date_range_with_timetable(self):
        timetable = Timetable()
        timetable.read_from_csv(self.timetable_filename)

        subject_lecture_count = {}
        attendance = {}
        total_lectures = 0
        total_attendance = 0
        day_names = list(calendar.day_name)
        
        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13):
                if (year == self.start_year and month < self.start_month) or (year == self.end_year and month > self.end_month):
                    continue
                month_range = calendar.monthrange(year, month)
                for day in range(1, month_range[1] + 1):
                    if (year == self.start_year and month == self.start_month and day < self.start_day) or (year == self.end_year and month == self.end_month and day > self.end_day):
                        continue
                    date = f"{year}-{month:02d}-{day:02d}"
                    if date in self.holidays:
                        continue
                    day_of_week = calendar.weekday(year, month, day)
                    day_name = day_names[day_of_week]
                    if day_name == "Saturday" or day_name == "Sunday":
                        continue
                    if day_name in timetable.subjects_by_day:
                        print(f"\n{date} - {day_name}")
                        attendance_input = input("Enter 'all present', 'all absent', 'bunk lectures' or 'done': ")
                        if attendance_input.lower() == "all present":
                            total_attendance += len(timetable.subjects_by_day[day_name])
                            total_lectures += len(timetable.subjects_by_day[day_name])
                            for subject in timetable.subjects_by_day[day_name]:
                                if subject in subject_lecture_count:
                                    subject_lecture_count[subject] += 1
                                    attendance[subject] = attendance.get(subject, 0) + 1
                                else:
                                    subject_lecture_count[subject] = 1
                                    attendance[subject] = 1
                        elif attendance_input.lower() == "all absent":
                            total_lectures += len(timetable.subjects_by_day[day_name])
                            for subject in timetable.subjects_by_day[day_name]:
                                if subject in subject_lecture_count:
                                    subject_lecture_count[subject] += 1
                                else:
                                    subject_lecture_count[subject] = 1
                        elif attendance_input.lower() == "bunk lectures":
                            bunked_subjects_input = input("Enter the bunked lectures separated by commas (e.g. Math,Science): ")
                            bunked_subjects = [subject.strip() for subject in bunked_subjects_input.split(",")]
                            total_attendance += len(timetable.subjects_by_day[day_name]) - len(bunked_subjects)
                            total_lectures += len(timetable.subjects_by_day[day_name])
                            for subject in timetable.subjects_by_day[day_name]:
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

start_date_input = input("Enter the start date in YYYY-MM-DD format: ")
start_year, start_month, start_day = map(int, start_date_input.split("-"))
end_date_input = input("Enter the end date in YYYY-MM-DD format: ")
end_year, end_month, end_day = map(int, end_date_input.split("-"))

timetable_filename = input("Enter the filename of the CSV file containing the timetable: ")

holidays_input = input("Do you want to add any holidays? (yes/no): ")
holidays = []
if holidays_input.lower() == "yes":
    while True:
        holiday_input = input("Enter a holiday date in YYYY-MM-DD format (or 'done' to finish): ")
        if holiday_input.lower() == "done":
            break
        holidays.append(holiday_input)

attendance_tracker = AttendanceTracker(start_year, start_month, start_day, end_year, end_month, end_day, timetable_filename, holidays)
attendance_percentage, total_attendance_percentage = attendance_tracker.select_date_range_with_timetable()

for subject, percentage in attendance_percentage.items():
    print(f"{subject}: {percentage:.2f}% attendance")

print(f"\nTotal attendance: {total_attendance_percentage:.2f}%")
