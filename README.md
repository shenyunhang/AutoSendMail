# AutoSendMail
A tool that automatically sends logs to your mails to notify you when your program is accomplished.


## Usage:
```bash
sendmail.py -c your-command
```

We can also specify the log file:
```bash
sendmail.py -c your-command -l your-log
```

If the command requires current shell environment to execute, we can do this by:
```bash
your-command | tee your-log ; sendmail.py -l your-log
```


## Configure

We need create a simple file named 'email.yml' to configure the email.

The email.yml.example provides the template.
```bash
cp email.yml.example email.yml
```
And then fill the content in email.yml.
