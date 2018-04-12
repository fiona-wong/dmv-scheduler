# DMV Scheduler

DMV Script that checks for available appointments and books them when an earlier appointment time becomes available

## Getting Started

pip install -r requirements.txt

fill out constants with personal information

write the date of an appointment time in the same format that you currently have in appt.txt or leave as is


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
