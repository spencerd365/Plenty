import json
import unittest

import schedule


class CalendarTest(unittest.TestCase):

    def setUp(self):
        self.__calendar = schedule.Calendar(schedule.DEFAULT_SCHEDULE)

    def test_get_all(self):
        schedules = self.__calendar.get_schedules()
        self.assertEqual(len(schedules.keys()), 2)
        self.assertTrue('Room1' in schedules)
        self.assertTrue('Room2' in schedules)

    def test_get_known(self):
        schedule = self.__calendar.get_schedule('Room1')
        self.assertEqual(6, len(schedule['commands']))
        self.assertEqual('09:00:00Z', schedule['commands'][0]['time'])
        self.assertEqual(70, schedule['commands'][0]['target'])

    def test_get_unknown(self):
        schedule = self.__calendar.get_schedule('Room3')
        self.assertIsNone(schedule)

    def test_put(self):
        self.assertIsNone(self.__calendar.get_schedule('Room3'))

        self.__calendar.put_schedule('Room3', {
            'commands': [
                {'time': '10:00:00Z', 'target': 50}
            ]
        })

        schedule = self.__calendar.get_schedule('Room3')
        self.assertEqual(1, len(schedule['commands']))
        self.assertEqual(50, schedule['commands'][0]['target'])


class ServerTest(unittest.TestCase):

    def setUp(self):
        schedule.app.testing = True
        self.client = schedule.app.test_client()

    def test_get_all(self):
        response = self.client.get('/schedules.json')
        self.assertEqual(200, response.status_code)
        schedules = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(schedules.keys()), 2)
        self.assertTrue('Room1' in schedules)
        self.assertTrue('Room2' in schedules)

    def test_get_known(self):
        response = self.client.get('/schedule/Room1.json')
        self.assertEqual(response.status_code, 200)
        schedule = json.loads(response.data.decode('utf-8'))
        self.assertEqual(6, len(schedule['commands']))
        self.assertEqual('09:00:00Z', schedule['commands'][0]['time'])
        self.assertEqual(70, schedule['commands'][0]['target'])

    def test_get_unknown(self):
        response = self.client.get('/schedule/Room3.json')
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post('/schedule/Room2.json', data=json.dumps(
            {
                'commands': [
                    {'time': '10:00:00Z', 'target': 50}
                ]
            }
        ))

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/schedule/Room2.json')
        self.assertEqual(response.status_code, 200)
        schedule = json.loads(response.data.decode('utf-8'))
        self.assertEqual(1, len(schedule['commands']))

    def test_post_no_command(self):
        response = self.client.post('/schedule/Room2.json', data=json.dumps(
            {}
        ))

        self.assertEqual(response.status_code, 400)

    def test_post_no_time(self):
        response = self.client.post('/schedule/Room2.json', data=json.dumps(
            {
                'commands': [
                    {'target': 50}
                ]
            }
        ))

        self.assertEqual(response.status_code, 400)

    def test_post_no_target(self):
        response = self.client.post('/schedule/Room2.json', data=json.dumps(
            {
                'commands': [
                    {'time': '10:00:00Z'}
                ]
            }
        ))

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
