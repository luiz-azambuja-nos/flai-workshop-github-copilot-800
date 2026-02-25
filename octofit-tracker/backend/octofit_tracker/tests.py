from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='teamuser',
            email='teamuser@example.com',
            password='password123'
        )
        self.team = Team.objects.create(name='Alpha Team')
        self.team.members.add(self.user)

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Alpha Team')

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Alpha Team')

    def test_team_members(self):
        self.assertIn(self.user, self.team.members.all())


class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='actuser',
            email='actuser@example.com',
            password='password123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30.0,
            date=datetime.date.today()
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30.0)

    def test_activity_str(self):
        expected = f"actuser - Running on {datetime.date.today()}"
        self.assertEqual(str(self.activity), expected)


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='lbuser',
            email='lbuser@example.com',
            password='password123'
        )
        self.entry = Leaderboard.objects.create(user=self.user, score=500)

    def test_leaderboard_creation(self):
        self.assertEqual(self.entry.score, 500)

    def test_leaderboard_str(self):
        self.assertEqual(str(self.entry), 'lbuser: 500')


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Routine',
            description='A quick morning workout',
            exercises=['push-ups', 'sit-ups', 'jumping jacks']
        )

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, 'Morning Routine')

    def test_workout_str(self):
        self.assertEqual(str(self.workout), 'Morning Routine')


class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='apiuser',
            email='apiuser@example.com',
            password='password123'
        )

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_detail(self):
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Beta Team')

    def test_list_teams(self):
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        url = reverse('team-list')
        data = {'name': 'Gamma Team', 'members': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='actapiuser',
            email='actapiuser@example.com',
            password='password123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Cycling',
            duration=45.0,
            date=datetime.date.today()
        )

    def test_list_activities(self):
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_activity_detail(self):
        url = reverse('activity-detail', args=[self.activity.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='lbapiuser',
            email='lbapiuser@example.com',
            password='password123'
        )
        self.entry = Leaderboard.objects.create(user=self.user, score=750)

    def test_list_leaderboard(self):
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_leaderboard_detail(self):
        url = reverse('leaderboard-detail', args=[self.entry.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Evening Stretch',
            description='Relaxing evening stretches',
            exercises=['hamstring stretch', 'quad stretch', 'shoulder roll']
        )

    def test_list_workouts(self):
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workout(self):
        url = reverse('workout-list')
        data = {
            'name': 'Power Yoga',
            'description': 'Intense yoga session',
            'exercises': ['warrior pose', 'downward dog']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_workout_detail(self):
        url = reverse('workout-detail', args=[self.workout.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTest(APITestCase):
    def test_api_root(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
