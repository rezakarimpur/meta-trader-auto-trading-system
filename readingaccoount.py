import pandas as pd
 
file_path = "full_account_details.csv"

try:
    # باز کردن فایل با انکودینگ utf-16
    with open(file_path, encoding='utf-16') as f:
        contents = f.read()
        print("File read successfully!")
        print(contents)  # برای نمایش محتوا در کنسول
except UnicodeDecodeError as e:
    print("Failed to decode file with utf-16 encoding:")
    print(e)

# ادامه پردازش محتوا
else:
    print("Processing complete!")
# دیکشنری برای ذخیره داده‌ها
data_dict = {
    "Account": [],
    "Position": [],
    "History": []
}

# پردازش هر خط
lines = contents.split("\n")
for line in lines:
    line = line.strip()
    if line.startswith("Account"):
        _, key, value = line.split("\t")
        data_dict["Account"].append({"Key": key, "Value": value})
    elif line.startswith("Position"):
        _, position_data = line.split("\t", 1)
        data_dict["Position"].append(position_data)
    elif line.startswith("History"):
        _, history_data = line.split("\t", 1)
        details_parts = history_data.split(", ")
        history_entry = {}
        for part in details_parts:
            key, value = part.split(": ")
            history_entry[key.strip()] = value.strip()
        data_dict["History"].append(history_entry)

# نمایش داده‌ها
print("Account Data:")
print(data_dict["Account"])
print("\nPosition Data:")
print(data_dict["Position"])
print("\nHistory Data:")
print(data_dict["History"])
