from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')

        # Delete in proper order to respect foreign keys
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write('Creating users (superheroes)...')

        # Marvel heroes
        iron_man = User.objects.create(
            username='ironman',
            email='tony.stark@avengers.com',
            password='pbkdf2_pepper3000suit'
        )
        spider_man = User.objects.create(
            username='spiderman',
            email='peter.parker@avengers.com',
            password='pbkdf2_greatpower'
        )
        captain_america = User.objects.create(
            username='captainamerica',
            email='steve.rogers@avengers.com',
            password='pbkdf2_supersoldier'
        )

        # DC heroes
        batman = User.objects.create(
            username='batman',
            email='bruce.wayne@jla.com',
            password='pbkdf2_darkknightrise'
        )
        wonder_woman = User.objects.create(
            username='wonderwoman',
            email='diana.prince@jla.com',
            password='pbkdf2_amazonwarrior'
        )
        superman = User.objects.create(
            username='superman',
            email='clark.kent@jla.com',
            password='pbkdf2_manofsteel'
        )

        self.stdout.write('Creating teams...')

        team_marvel = Team.objects.create(name='Team Marvel')
        team_marvel.members.set([iron_man, spider_man, captain_america])

        team_dc = Team.objects.create(name='Team DC')
        team_dc.members.set([batman, wonder_woman, superman])

        self.stdout.write('Creating activities...')

        Activity.objects.create(
            user=iron_man,
            activity_type='Strength Training',
            duration=60.0,
            date=date(2025, 2, 20)
        )
        Activity.objects.create(
            user=spider_man,
            activity_type='Web Swinging Cardio',
            duration=45.0,
            date=date(2025, 2, 21)
        )
        Activity.objects.create(
            user=captain_america,
            activity_type='Shield Throwing',
            duration=30.0,
            date=date(2025, 2, 22)
        )
        Activity.objects.create(
            user=batman,
            activity_type='Martial Arts',
            duration=90.0,
            date=date(2025, 2, 20)
        )
        Activity.objects.create(
            user=wonder_woman,
            activity_type='Lasso Training',
            duration=50.0,
            date=date(2025, 2, 21)
        )
        Activity.objects.create(
            user=superman,
            activity_type='Flight Endurance',
            duration=120.0,
            date=date(2025, 2, 22)
        )

        self.stdout.write('Creating leaderboard entries...')

        Leaderboard.objects.create(user=iron_man, score=950)
        Leaderboard.objects.create(user=spider_man, score=870)
        Leaderboard.objects.create(user=captain_america, score=990)
        Leaderboard.objects.create(user=batman, score=1000)
        Leaderboard.objects.create(user=wonder_woman, score=980)
        Leaderboard.objects.create(user=superman, score=1050)

        self.stdout.write('Creating workouts...')

        Workout.objects.create(
            name='Avengers Assemble Workout',
            description='High-intensity workout inspired by Marvel heroes',
            exercises=[
                {'name': 'Arc Reactor Push-ups', 'sets': 4, 'reps': 15},
                {'name': 'Spider Crawl Planks', 'sets': 3, 'reps': 10},
                {'name': 'Shield Lateral Raises', 'sets': 3, 'reps': 12},
            ]
        )
        Workout.objects.create(
            name='Justice League Training',
            description='Strength and endurance workout inspired by DC heroes',
            exercises=[
                {'name': 'Batman Burpees', 'sets': 5, 'reps': 10},
                {'name': 'Wonder Woman Lunges', 'sets': 4, 'reps': 12},
                {'name': 'Superman Deadlifts', 'sets': 3, 'reps': 8},
            ]
        )
        Workout.objects.create(
            name='Hero Core Blast',
            description='Core workout for all heroes regardless of universe',
            exercises=[
                {'name': 'Superhero Sit-ups', 'sets': 4, 'reps': 20},
                {'name': 'Power Plank', 'seconds': 60, 'sets': 3},
                {'name': 'Villain-Crusher Crunches', 'sets': 3, 'reps': 15},
            ]
        )

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated octofit_db with superhero test data!\n'
            f'  Users: {User.objects.count()}\n'
            f'  Teams: {Team.objects.count()}\n'
            f'  Activities: {Activity.objects.count()}\n'
            f'  Leaderboard: {Leaderboard.objects.count()}\n'
            f'  Workouts: {Workout.objects.count()}'
        ))
