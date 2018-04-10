# DMV Scheduler

DMV Script that checks for available appointments and books them when an earlier appointment time becomes available

## Getting Started

pip install -r requirements.txt

### How To Use

Set up cron tab to run script every 15 min until the day of your appointment

In terminal:
```
crontab -e
*/15 * * * *  <path-to:schedule_appt.py>
```
