# AutoSendMail
A tool that automatically sends logs to your mails to notify you when your program ends.


###Usage:
```bash
sendmail.py -c your-command


Or you can specify the log file:
```bash
sendmail.py -c your-command -l your-log


If the command requires current shell environment to execute, we can do this by:
```bash
your-command | tee your-log ; sendmail.py -l your-log
	


###configure

We need create a simple file named 'email.conf' to configure the email.
The email.conf.example provide a template.
