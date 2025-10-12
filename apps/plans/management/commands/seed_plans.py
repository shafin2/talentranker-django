from django.core.management.base import BaseCommand
from apps.plans.models import Plan


class Command(BaseCommand):
    help = 'Seed plans matching Node.js backend exactly'

    def handle(self, *args, **options):
        # Clear existing plans
        Plan.objects.all().delete()
        self.stdout.write('Cleared existing plans')

        plans_data = [
            # Freemium Global Plan
            {
                'name': 'Freemium',
                'region': 'Global',
                'billing_cycle': None,
                'price': 0,
                'currency': 'USD',
                'jd_limit': 1,
                'cv_limit': 10,
                'description': 'Perfect for trying out TalentRanker',
                'features': ['1 Job Description', '10 CV Reviews', 'Basic Matching', 'Email Support'],
                'sort_order': 1
            },

            # Pakistan Plans - Starter
            {
                'name': 'Starter',
                'region': 'Pakistan',
                'billing_cycle': 'Monthly',
                'price': 5000,
                'currency': 'PKR',
                'jd_limit': 10,
                'cv_limit': 500,
                'description': 'Great for small teams and startups',
                'features': ['10 Job Descriptions', '500 CV Reviews', 'Advanced Matching', 'Priority Support'],
                'sort_order': 2
            },
            {
                'name': 'Starter',
                'region': 'Pakistan',
                'billing_cycle': 'SixMonth',
                'price': 25000,
                'currency': 'PKR',
                'jd_limit': 10,
                'cv_limit': 500,
                'description': 'Great for small teams and startups (6 months)',
                'features': ['10 Job Descriptions', '500 CV Reviews', 'Advanced Matching', 'Priority Support'],
                'sort_order': 3
            },
            {
                'name': 'Starter',
                'region': 'Pakistan',
                'billing_cycle': 'Annual',
                'price': 50000,
                'currency': 'PKR',
                'jd_limit': 10,
                'cv_limit': 500,
                'description': 'Great for small teams and startups (Annual)',
                'features': ['10 Job Descriptions', '500 CV Reviews', 'Advanced Matching', 'Priority Support'],
                'sort_order': 4
            },

            # Pakistan Plans - Growth
            {
                'name': 'Growth',
                'region': 'Pakistan',
                'billing_cycle': 'Monthly',
                'price': 12000,
                'currency': 'PKR',
                'jd_limit': 25,
                'cv_limit': 1500,
                'description': 'Perfect for growing companies',
                'features': ['25 Job Descriptions', '1500 CV Reviews', 'AI-Powered Matching', 'Phone Support', 'Custom Reports'],
                'sort_order': 5
            },
            {
                'name': 'Growth',
                'region': 'Pakistan',
                'billing_cycle': 'SixMonth',
                'price': 60000,
                'currency': 'PKR',
                'jd_limit': 25,
                'cv_limit': 1500,
                'description': 'Perfect for growing companies (6 months)',
                'features': ['25 Job Descriptions', '1500 CV Reviews', 'AI-Powered Matching', 'Phone Support', 'Custom Reports'],
                'sort_order': 6
            },
            {
                'name': 'Growth',
                'region': 'Pakistan',
                'billing_cycle': 'Annual',
                'price': 120000,
                'currency': 'PKR',
                'jd_limit': 25,
                'cv_limit': 1500,
                'description': 'Perfect for growing companies (Annual)',
                'features': ['25 Job Descriptions', '1500 CV Reviews', 'AI-Powered Matching', 'Phone Support', 'Custom Reports'],
                'sort_order': 7
            },

            # Pakistan Plans - Pro
            {
                'name': 'Pro',
                'region': 'Pakistan',
                'billing_cycle': 'Monthly',
                'price': 25000,
                'currency': 'PKR',
                'jd_limit': 50,
                'cv_limit': 3000,
                'description': 'For established businesses with high volume',
                'features': ['50 Job Descriptions', '3000 CV Reviews', 'Advanced Analytics', 'Dedicated Support', 'API Access'],
                'sort_order': 8
            },
            {
                'name': 'Pro',
                'region': 'Pakistan',
                'billing_cycle': 'SixMonth',
                'price': 130000,
                'currency': 'PKR',
                'jd_limit': 50,
                'cv_limit': 3000,
                'description': 'For established businesses with high volume (6 months)',
                'features': ['50 Job Descriptions', '3000 CV Reviews', 'Advanced Analytics', 'Dedicated Support', 'API Access'],
                'sort_order': 9
            },
            {
                'name': 'Pro',
                'region': 'Pakistan',
                'billing_cycle': 'Annual',
                'price': 260000,
                'currency': 'PKR',
                'jd_limit': 50,
                'cv_limit': 3000,
                'description': 'For established businesses with high volume (Annual)',
                'features': ['50 Job Descriptions', '3000 CV Reviews', 'Advanced Analytics', 'Dedicated Support', 'API Access'],
                'sort_order': 10
            },

            # Pakistan Plans - Enterprise
            {
                'name': 'Enterprise',
                'region': 'Pakistan',
                'billing_cycle': None,
                'price': None,
                'currency': 'PKR',
                'jd_limit': None,
                'cv_limit': None,
                'description': 'Custom solution for large enterprises',
                'features': ['Unlimited Job Descriptions', 'Unlimited CV Reviews', 'White-label Solution', '24/7 Support', 'Custom Integrations', 'Dedicated Account Manager'],
                'sort_order': 11
            },

            # International Plans - Starter
            {
                'name': 'Starter',
                'region': 'International',
                'billing_cycle': 'Monthly',
                'price': 50,
                'currency': 'USD',
                'jd_limit': 10,
                'cv_limit': 1000,
                'description': 'Great for small teams and startups',
                'features': ['10 Job Descriptions', '1000 CV Reviews', 'Advanced Matching', 'Priority Support'],
                'sort_order': 12
            },
            {
                'name': 'Starter',
                'region': 'International',
                'billing_cycle': 'SixMonth',
                'price': 250,
                'currency': 'USD',
                'jd_limit': 10,
                'cv_limit': 1000,
                'description': 'Great for small teams and startups (6 months)',
                'features': ['10 Job Descriptions', '1000 CV Reviews', 'Advanced Matching', 'Priority Support'],
                'sort_order': 13
            },
            {
                'name': 'Starter',
                'region': 'International',
                'billing_cycle': 'Annual',
                'price': 500,
                'currency': 'USD',
                'jd_limit': 10,
                'cv_limit': 1000,
                'description': 'Great for small teams and startups (Annual)',
                'features': ['10 Job Descriptions', '1000 CV Reviews', 'Advanced Matching', 'Priority Support'],
                'sort_order': 14
            },

            # International Plans - Growth
            {
                'name': 'Growth',
                'region': 'International',
                'billing_cycle': 'Monthly',
                'price': 120,
                'currency': 'USD',
                'jd_limit': 25,
                'cv_limit': 3000,
                'description': 'Perfect for growing companies',
                'features': ['25 Job Descriptions', '3000 CV Reviews', 'AI-Powered Matching', 'Phone Support', 'Custom Reports'],
                'sort_order': 15
            },
            {
                'name': 'Growth',
                'region': 'International',
                'billing_cycle': 'SixMonth',
                'price': 600,
                'currency': 'USD',
                'jd_limit': 25,
                'cv_limit': 3000,
                'description': 'Perfect for growing companies (6 months)',
                'features': ['25 Job Descriptions', '3000 CV Reviews', 'AI-Powered Matching', 'Phone Support', 'Custom Reports'],
                'sort_order': 16
            },
            {
                'name': 'Growth',
                'region': 'International',
                'billing_cycle': 'Annual',
                'price': 1200,
                'currency': 'USD',
                'jd_limit': 25,
                'cv_limit': 3000,
                'description': 'Perfect for growing companies (Annual)',
                'features': ['25 Job Descriptions', '3000 CV Reviews', 'AI-Powered Matching', 'Phone Support', 'Custom Reports'],
                'sort_order': 17
            },

            # International Plans - Pro
            {
                'name': 'Pro',
                'region': 'International',
                'billing_cycle': 'Monthly',
                'price': 250,
                'currency': 'USD',
                'jd_limit': 50,
                'cv_limit': 5000,
                'description': 'For established businesses with high volume',
                'features': ['50 Job Descriptions', '5000 CV Reviews', 'Advanced Analytics', 'Dedicated Support', 'API Access'],
                'sort_order': 18
            },
            {
                'name': 'Pro',
                'region': 'International',
                'billing_cycle': 'SixMonth',
                'price': 1300,
                'currency': 'USD',
                'jd_limit': 50,
                'cv_limit': 5000,
                'description': 'For established businesses with high volume (6 months)',
                'features': ['50 Job Descriptions', '5000 CV Reviews', 'Advanced Analytics', 'Dedicated Support', 'API Access'],
                'sort_order': 19
            },
            {
                'name': 'Pro',
                'region': 'International',
                'billing_cycle': 'Annual',
                'price': 2600,
                'currency': 'USD',
                'jd_limit': 50,
                'cv_limit': 5000,
                'description': 'For established businesses with high volume (Annual)',
                'features': ['50 Job Descriptions', '5000 CV Reviews', 'Advanced Analytics', 'Dedicated Support', 'API Access'],
                'sort_order': 20
            },

            # International Plans - Enterprise
            {
                'name': 'Enterprise',
                'region': 'International',
                'billing_cycle': None,
                'price': None,
                'currency': 'USD',
                'jd_limit': None,
                'cv_limit': None,
                'description': 'Custom solution for large enterprises',
                'features': ['Unlimited Job Descriptions', 'Unlimited CV Reviews', 'White-label Solution', '24/7 Support', 'Custom Integrations', 'Dedicated Account Manager'],
                'sort_order': 21
            },
        ]

        created = 0
        updated = 0

        for plan_data in plans_data:
            plan, created_flag = Plan.objects.update_or_create(
                name=plan_data['name'],
                region=plan_data['region'],
                billing_cycle=plan_data['billing_cycle'],
                defaults={
                    'price': plan_data['price'],
                    'currency': plan_data['currency'],
                    'jd_limit': plan_data['jd_limit'],
                    'cv_limit': plan_data['cv_limit'],
                    'description': plan_data['description'],
                    'features': plan_data['features'],
                    'sort_order': plan_data['sort_order'],
                    'is_active': True
                }
            )

            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created: {plan}'))
            else:
                updated += 1
                self.stdout.write(self.style.WARNING(f'🔄 Updated: {plan}'))

        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(f'   Created: {created} plans')
        self.stdout.write(f'   Updated: {updated} plans')
        self.stdout.write(f'   Total: {Plan.objects.count()} plans')
