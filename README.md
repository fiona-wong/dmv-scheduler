# DMV Scheduler

DMV Script that checks for available appointments and books them when an earlier appointment time becomes available

## Getting Started

pip install -r requirements.txt
fill out constants with personal information
make sure that you write a date of your current appt in appt.txt with the same format as currently in the myfile

Note: This script is for OFFICE VISIT APPT ONLY

### How To Use

Set up cron tab to run script every 15 min until the day of your appointment

In terminal:
```
crontab -e
*/15 * * * *  <path-to:schedule_appt.py>
```
Or to run manually just:
```
python schedule_appt.py
```
