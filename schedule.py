"""Server for the technologist take home question.

Server for the technologist take home question that offers a fake backend for
a temperature scheduling service.

Author: Plenty United
License: Closed Source
"""


import copy
import json

import flask
app = flask.Flask(__name__)
app.debug = True


DEFAULT_SCHEDULE = {
    'Room1': {'commands': [
        {'time': '09:00:00Z', 'target': 70},
        {'time': '13:00:00Z', 'target': 75},
        {'time': '17:00:00Z', 'target': 70},
        {'time': '18:00:00Z', 'target': 65},
        {'time': '01:00:00Z', 'target': 60},
        {'time': '08:00:00Z', 'target': 65}
    ]},
    'Room2': {'commands': [
        {'time': '17:00:00Z', 'target': 70},
        {'time': '08:00:00Z', 'target': 65}
    ]}
}


class Calendar:
    """Set of schedules indexed by room name."""

    def __init__(self, schedules):
        """Create a new calendar.

        Args:
            schedules (list of dict): The list of schedules to include in this
                calendar.
        """
        self.__schedules = copy.deepcopy(schedules)

    def get_schedules(self):
        """Get all of the schedules on the calendar.

        Returns:
            list of dict: The schedules registered on this calendar.
        """
        return self.__schedules

    def get_schedule(self, name):
        """Get a schedule given that schedule's name.

        Args:
            name (str): The name of the location (like Room1) whose schedule
                should be returned.
        """
        return self.__schedules.get(name, None)

    def put_schedule(self, name, scheudle):
        """Put a schedule.

        Put a schedule, overwritting a prior schedule if one already exists at
        that name.

        Args:
            name (str): The name of the scheudle to be put. This should be the
                location of the schedule.
            schedule (dict): Dictionary describing the schedule.
        """
        self.__schedules[name] = scheudle


def build_app(target_app, calendar):
    """Build a flask application.

    Args:
        target_app (flask.Flask): The application on which endpoints should be
            registered.
        calendar (Calendar): The starting calendar to be serviced by this app.
    """

    @target_app.route('/', methods=['GET'])
    def render_scheudle_view():
        """Render the schedule view."""
        return flask.render_template('schedule.html')

    @target_app.route('/schedules.json', methods=['GET'])
    def get_schedules():
        """Get a listing of all schedules.

        Returns:
            Response: Response containing a JSON object with JSON objects per
                location for which a schedule is registered. Those objects have
                a JSON array called "commands" whose elements contain the target
                temperature in Fahrenheit and the time as an ISO 8601 time.
        """
        return json.dumps(calendar.get_schedules())

    @target_app.route('/schedule/<schedule_name>.json', methods=['GET'])
    def get_schedule(schedule_name):
        """Get a schedules given the name of the location for that schedule.

        Get a schedules given the name of the location for that schedule where
        that name is given by the URL itself.

        Returns:
            Response: Response containing a JSON object with a JSON array called
                "commands" whose elements contain the target temperature in
                Fahrenheit and the time as an ISO 8601 time.
        """
        schedule = calendar.get_schedule(schedule_name)
        if schedule:
            return json.dumps(schedule)
        else:
            return 'Scheudle not found.', 404

    @target_app.route('/schedule/<schedule_name>.json', methods=['POST'])
    def update_schedule(schedule_name):
        """Update a schedule given the name of the location for that schedule.

        Update a schedule given the name of the location for that schedule,
        using the schedule name from the URL and the body of the request as the
        JSON description of that schedule.

        Returns:
            Response: Respnse indicating if the action was successful.
        """
        data = flask.request.data

        new_schedule = None
        try:
            new_schedule = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            return 'Could not parse request', 400

        if not 'commands' in new_schedule:
            return 'Expecting schedule to provide commands.', 400

        for item in new_schedule['commands']:
            if not 'time' in item:
                return 'All commands must provide a time.', 400

            if not 'target' in item:
                return 'All commands must provide a target.', 400

        calendar.put_schedule(schedule_name, new_schedule)

        return 'Updated schedule.', 200

    return target_app


app = build_app(app, Calendar(DEFAULT_SCHEDULE))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
