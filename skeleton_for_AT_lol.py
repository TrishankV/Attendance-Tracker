import calendar

class AttendanceTracker:
    def __init__(self):
        self.subjects_by_day = {}
        self.holidays = []
        self.subject_lecture_count = {}
        self.attendance = {}
        self.total_lectures = 0
        self.total_attendance = 0

    def create_timetable(self, day):
        if day in self.subjects_by_day:
            timetable = self.subjects_by_day[day]
        else:
            timetable = []
        return timetable

    def count_subjects_lectures(self, weeks):
        for day, subjects in self.subjects_by_day.items():
            for subject in subjects:
                if subject in self.subject_lecture_count:
                    self.subject_lecture_count[subject] += weeks if day != "Saturday" and day != "Sunday" else 0
                else:
                    self.subject_lecture_count[subject] = weeks if day != "Saturday" and day != "Sunday" else 0

    def select_date_range_with_timetable(self, start_date, end_date):
        try:
            start_year, start_month, start_day = map(int, start_date.split('-'))
            end_year, end_month, end_day = map(int, end_date.split('-'))
        except ValueError:
            print("Error: Invalid date format. Please enter dates in YYYY-MM-DD format.")
            return

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if (year == start_year and month < start_month) or (year == end_year and month > end_month):
                    continue
                month_range = calendar.monthrange(year, month)
                for day in range(1, month_range[1] + 1):
                    if (year == start_year and month == start_month and day < start_day) or (year == end_year and month == end_month and day > end_day):
                        continue
                    date = f"{year}-{month:02d}-{day:02d}"
                    if date in self.holidays:
                        continue
                    day_of_week = calendar.weekday(year, month, day)
                    day_name = calendar.day_name[day_of_week]
                    if day_name == "Saturday" or day_name == "Sunday":
                        continue
                    if day_name in self.subjects_by_day:
                        attendance_input = input(f"\n{date} - {day_name}\nEnter 'all present', 'all absent', 'bunk lectures' or 'done': ")
                        if attendance_input.lower() == "all present":
                            self.total_attendance += len(self.subjects_by_day[day_name])
                            self.total_lectures += len(self.subjects_by_day[day_name])
                            for subject in self.subjects_by_day[day_name]:
                                if subject in self.subject_lecture_count:
                                    self.subject_lecture_count[subject] += 1
                                    self.attendance[subject] = self.attendance.get(subject, 0) + 1
                                else:
                                    self.subject_lecture_count[subject] = 1
                                    self.attendance[subject] = 1
                        elif attendance_input.lower() == "all absent":
                            self.total_lectures += len(self.subjects_by_day[day_name])
                            for subject in self.subjects_by_day[day_name]:
                                if subject in self.subject_lecture_count:
                                    self.subject_lecture_count[subject] += 1
                                else:
                                    self.subject_lecture_count[subject] = 1
                        elif attendance_input.lower() == "bunk lectures":
                            bunked_subjects_input = input("Enter the bunked lectures separated by commas (e.g. Math,Science): ")
                            bunked_subjects = [subject.strip() for subject in bunked_subjects_input.split(",")]
                            self.total_attendance += len(self.subjects_by_day[day_name]) - len(bunked_subjects)
                            self.total_lectures += len(self.subjects_by_day[day_name])
                            for subject in self.subjects_by_day[day_name]:
                                if subject in bunked_subjects:
                                    continue
                                if subject in self.subject_lecture_count:
                                    self.subject_lecture_count[subject] += 1
                                    self.attendance[subject] = self.attendance.get(subject, 0) + 1
                                else:
                                    self.subject_lecture_count[subject] = 1
                                    self.attendance[subject] = 1
                        elif attendance_input.lower() == "done":
                            break

    def calculate_attendance_percentage(self):
        attendance_percentage = {}
        for subject, count in self.attendance.items():
            total_subject_lectures = self.subject_lecture_count.get(subject, 0)
            percentage = (count / total_subject_lectures) * 100
            attendance_percentage[subject] = percentage

        total_attendance_percentage = (self.total_attendance / self.total_lectures) * 100

        return attendance_percentage, total_attendance_percentage


# Example usage
tracker = AttendanceTracker()
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
for day_name in day_names:
    subjects_input = input(f"Enter the subjects for {day_name} separated by commas (e.g. Math,Science): ")
    if subjects_input.strip() != "":
        tracker.subjects_by_day[day_name] = [subject.strip() for subject in subjects_input.split(",")]
    else:
        tracker.subjects_by_day[day_name] = []

holidays_input = input("Do you want to add any holidays? (yes/no): ")
if holidays_input.lower() == "yes":
    while True:
        holiday_input = input("Enter a holiday date in YYYY-MM-DD format (or 'done' to finish): ")
        if holiday_input.lower() == "done":
            break
        tracker.holidays.append(holiday_input)

tracker.select_date_range_with_timetable(start_date, end_date)
attendance_percentage, total_attendance_percentage = tracker.calculate_attendance_percentage()

for subject, percentage in attendance_percentage.items():
    print(f"{subject}: {percentage:.2f}% attendance")

print(f"\nTotal attendance: {total_attendance_percentage:.2f}%")
