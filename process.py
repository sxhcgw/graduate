import re

str="手机很不错，很喜欢！质量也不错是正品,2015-11-19 17:08:43,,0,0,5,玫瑰金,公开版,jd_7811txl,61,四川,2015-10-29 08:44:18,0"
model = "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*$"
pattern = re.compile(model)
match = pattern.search(str)
pos = match.start()
print(str[0 : pos])
