CS Takehome - Schedule UI
================================================================================
Plenty take home question for technologists.

<br>

Introduction
--------------------------------------------------------------------------------
Thank you for taking the time to complete this exercise which will give you an
opportunity to work on a real-ish world problem on your time and at your own
pace. For this exercise, you will be reading the summary of user research below
and using the included test server to build a front-end that allows users to
modify 24 hour temperature schedules for different rooms.

You may use any open source libraries / code you would like to complete this
exercise which should take about 1 - 2 hours. You may also use any front-end
patterns or architectures you see fit. After you are done, please send your
interviewer an email.

While you may consult online resources, please do not share this problem or
directly collaborate with others.

Thanks again for your time and have fun!

<br>

Getting Started
--------------------------------------------------------------------------------
You will need Python 3 and Flask to complete this exercise. To get Python, [checkout this guide](http://docs.python-guide.org/en/latest/starting/installation/). To get Flask, use pip!

```
pip install -r requirements.txt
```

<br>

User Research / Problem Introduction
--------------------------------------------------------------------------------
Plants are growing in various "grow rooms" at a facility where each room has its
own environment and crop isolated from the other rooms. Plant scientists would
like to control the room temperatures on a per-room basis.

Specifically, Plant Science has daily temperature schedules it would like to
run in each room and has come to you for a tool that can:

 - Lookup a room in a UI to see the temperature schedule for that room.
 - Specify that temperature schedule for each room from the same UI at the
   hourly level.

Note that:

 - More detailed control beyond the hourly level is not necessary.
 - The same 24 hour temperature schedule is used every day.

One room may have more temperature changes scheduled than another
so some rooms might have a temperature that changes only twice daily while
others may have many temperature changes. Finally, the software will maintain
the last set temperature for a room until a new temperature target is provided.

For this exercise, the schedules only need to be shown and modified for Room1
and Room2 but assume that more rooms may be added in the future. That said,
the tool does not need to support adding / deleting rooms.

<br>

Your Task
--------------------------------------------------------------------------------
Your task (if you choose to accept it - and we hope you will!), is to extend the
provided web-based tool, designing and building a front-end that allows the user
to see and modify room schedules. You can use the existing backend, you only
need to work on the front-end.

<br>

Project Structure
--------------------------------------------------------------------------------
The HTML templates (rendered in [Jija2](http://jinja.pocoo.org/docs/2.9/)) are
in the templates folder. Static assets (including CSS and JS) are in the static
folder. You should not need to modify the backend during this exercise.

<br>

Endpoints Supported
--------------------------------------------------------------------------------
The following endpoints are provided for you:

 - "GET /" which will render the schedule.html template.
 - "GET /schedules.json" will return all rooms and their schedules in a JSON
   document.
 - "GET /schedule/<room name>.json" will return the schedule for the given room
   or a 404 if there is no known room by that name.
 - "POST /schedule/<room name>.json" will update the schedule for the given room
   where the body of the request should be a JSON schedule as described below.

<br>

Example Schedule
--------------------------------------------------------------------------------
Here is an example of what a schedule looks like:

```
{'commands': [
    {'time': '09:00:00Z', 'target': 70},
    {'time': '18:00:00Z', 'target': 65}
]}
```

In this schedule, the temperature is set to 70 F at 9am UTC and stays at 70 F
until 6pm UTC at which point the temperature drops to 65 F. The temperature will
stay 65F until 9am the following morning.

<br>

Running the Web Service
--------------------------------------------------------------------------------
Within Codenvy, use the run button at the top of the IDE and select "run". This
will start the server. In the console at the bottom of the IDE, a preview URL
will be provided. Click on that link to open your browser to the test server.
# Plenty
