grep -E "(192)(\.[0-9]{1,3}){3}" test.txt > z.txt
timeout /t 1
grep -E "(169)(\.[0-9]{1,3}){3}" test.txt >> z.txt
timeout /t 1
grep -E "(172)(\.[0-9]{1,3}){3}" test.txt >> z.txt
timeout /t 1
grep -E "(10)(\.[0-9]{1,3}){3}" test.txt >> z.txt
timeout /t 1
grep -E "(198)(\.[0-9]{1,3}){3}" test.txt >> z.txt
timeout /t 1
grep -E "(224)(\.[0-9]{1,3}){3}" test.txt >> z.txt
timeout /t 1
grep -E "(239)(\.[0-9]{1,3}){3}" test.txt >> z.txt
timeout /t 1
grep -E -o "[^^][0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}" z.txt > final.txt