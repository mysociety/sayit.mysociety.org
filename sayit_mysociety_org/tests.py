# -*- coding: utf-8 -*-

import re
import urlparse

from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings

from instances.tests import InstanceTestCase
from instances.models import Instance


@override_settings(BASE_HOST='example.org')
class SmokeTestsNoInstance(TestCase):
    """Very basic tests for non-instance pages"""
    def test_homepage(self):
        """Check that the home page returns OK."""
        resp = self.client.get('/')
        self.assertContains(resp, 'Bringing transcripts into the Internet age')

    def test_add_page(self):
        resp = self.client.get('/instances/add')
        self.assertContains(resp, '<span class="postfix">.example.org</span>')


class NoInstanceLoginRedirect(TestCase):
    def test_login_redirects_to_your_instances(self):
        get_user_model().objects.create_user(
            'alice', email='alice@example.com', password='foo')

        resp = self.client.post(
            '/accounts/login/',
            {'login': 'alice', 'password': 'foo'},
            )

        self.assertRedirects(resp, '/accounts/profile/')


class InstanceLoginRedirect(InstanceTestCase):
    def test_login_redirects_to_instance_home(self):
        get_user_model().objects.create_user(
            'alice', email='alice@example.com', password='foo')

        resp = self.client.post(
            '/accounts/login/',
            {'login': 'alice', 'password': 'foo'},
            follow=True,
            )

        self.assertRedirects(resp, '/')


class YourInstancesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.alice = get_user_model().objects.create_user(
            'alice', email='alice@example.com', password='foo')

        cls.bob = get_user_model().objects.create_user(
            'bob', email='bob@example.com', password='foo')

        return super(YourInstancesTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.alice.delete()
        cls.bob.delete()
        return super(YourInstancesTests, cls).tearDownClass()

    def test_not_logged_in(self):
        self.client.logout()
        resp = self.client.get('/accounts/profile/')
        self.assertRedirects(resp, '/accounts/login/?next=/accounts/profile/')

    def test_no_instances(self):
        self.client.login(username='alice', password='foo')
        resp = self.client.get('/accounts/profile/')
        self.assertContains(
            resp,
            "You have don't yet have any instances",
            status_code=200,
            )
        self.assertContains(resp, "<a href='/instances/add'>create one")

    def test_instance_no_description(self):
        instance_no_description = Instance.objects.create(
            label='bob-no-description',
            title="Bob's Mystery Instance",
            created_by=self.bob,
            )
        instance_no_description.users.add(self.bob)

        self.client.login(username='bob', password='foo')
        resp = self.client.get('/accounts/profile/')

        self.assertContains(resp, "Bob&#39;s Mystery Instance", status_code=200)
        self.assertContains(resp, "(created by you)")
        self.assertContains(resp, "(no description)")

        self.assertNotContains(
            resp,
            "You have don't yet have any instances",
            )
        self.assertNotContains(resp, "<a href='/instances/add'>create one")

        instance_no_description.delete()
        self.client.logout()

    def test_instance_with_description(self):
        instance_with_description = Instance.objects.create(
            label='bob-with-description',
            title="Bob's Quotes",
            description="Quotes go here.",
            created_by=self.bob,
            )
        instance_with_description.users.add(self.bob)

        self.client.login(username='bob', password='foo')
        resp = self.client.get('/accounts/profile/')

        self.assertContains(resp, "Bob&#39;s Quotes", status_code=200)
        self.assertContains(resp, "(created by you)")
        self.assertNotContains(resp, "(no description)")
        self.assertContains(resp, "Quotes go here.")

        instance_with_description.delete()
        self.client.logout()

    def test_instance_long_description(self):
        instance_long_description = Instance.objects.create(
            label='bob-with-long-description',
            # http://www.gutenberg.org/cache/epub/1064/pg1064.txt
            title="The Masque of the Red Death",
            description="""
The "Red Death" had long devastated the country.  No pestilence had
ever been so fatal, or so hideous.  Blood was its Avatar and its
seal--the redness and the horror of blood.  There were sharp pains, and
sudden dizziness, and then profuse bleeding at the pores, with
dissolution.  The scarlet stains upon the body and especially upon the
face of the victim, were the pest ban which shut him out from the aid
and from the sympathy of his fellow-men. And the whole seizure,
progress and termination of the disease, were the incidents of half an
hour.

But the Prince Prospero was happy and dauntless and sagacious. When his
dominions were half depopulated, he summoned to his presence a thousand
hale and light-hearted friends from among the knights and dames of his
court, and with these retired to the deep seclusion of one of his
castellated abbeys.  This was an extensive and magnificent structure,
the creation of the prince's own eccentric yet august taste.  A strong
and lofty wall girdled it in. This wall had gates of iron.  The
courtiers, having entered, brought furnaces and massy hammers and
welded the bolts.  They resolved to leave means neither of ingress nor
egress to the sudden impulses of despair or of frenzy from within.  The
abbey was amply provisioned.  With such precautions the courtiers might
bid defiance to contagion.  The external world could take care of
itself.  In the meantime it was folly to grieve, or to think.  The
prince had provided all the appliances of pleasure.  There were
buffoons, there were improvisatori, there were ballet-dancers, there
were musicians, there was Beauty, there was wine.  All these and
security were within.  Without was the "Red Death".

It was towards the close of the fifth or sixth month of his seclusion,
and while the pestilence raged most furiously abroad, that the Prince
Prospero entertained his thousand friends at a masked ball of the most
unusual magnificence.
""",
            created_by=self.bob,
            )
        instance_long_description.users.add(self.bob)

        self.client.login(username='bob', password='foo')
        resp = self.client.get('/accounts/profile/')

        self.assertContains(resp, "The Masque of the Red Death", status_code=200)
        self.assertContains(
            resp,
            """The &quot;Red Death&quot; had long devastated the country.  No pestilence had
ever been so fatal, or so hi...""")

        instance_long_description.delete()
        self.client.logout()

    def test_someone_elses_instance(self):
        instance = Instance.objects.create(
            label='bobs-instance',
            title="Bob's Instance",
            created_by=self.bob,
            )
        instance.users.add(self.alice)

        self.client.login(username='alice', password='foo')
        resp = self.client.get('/accounts/profile/')

        self.assertContains(
            resp,
            "Bob&#39;s Instance",
            status_code=200,
            )
        self.assertNotContains(resp, '(created by you)')

        instance.delete()
        self.client.logout()


class SmokeTests(InstanceTestCase):
    """Very basic tests to make sure we can see anything at all."""
    def test_homepage(self):
        """Check that the home page for an empty instance returns OK."""
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)


class ShareInstanceTests(InstanceTestCase):
    def test_share_form_only_logged_in(self):
        self.client.logout()
        resp = self.client.get('/instance/share')
        self.assertRedirects(resp, '/accounts/login/?next=/instance/share')

    def test_share_form_exists(self):
        resp = self.client.get('/instance/share')
        self.assertContains(resp, 'Share your SayIt', status_code=200)

    def test_share_with_existing_user(self):
        sharee = get_user_model().objects.create_user(
            'sharee', email='sharee@example.com')
        resp = self.client.post('/instance/share',
                                {'email': 'sharee@example.com'},
                                follow=True)

        self.instance.users.get(pk=sharee.id)
        self.assertRedirects(resp, '/instance/share', status_code=302)

        self.assertContains(resp, 'invitation has been sent')

        # Verify that the subject of the first message is correct.
        self.assertIn(
            'You\'ve been invited to help edit "Test Instance"',
            mail.outbox[0].subject,
            )

    def test_share_with_unknown_user(self):
        resp = self.client.post('/instance/share',
                                {'email': 'newsharee@example.com'})

        sharee = get_user_model().objects.get(email='newsharee@example.com')
        self.instance.users.get(pk=sharee.id)
        self.assertRedirects(resp, '/instance/share', status_code=302)

        invite_message = mail.outbox[0]

        # Verify that the subject of the first message is correct.
        self.assertIn(
            'You\'ve been invited to help edit "Test Instance"',
            invite_message.subject,
            )

        # Get the link out of the invitation email
        link = re.search(r'http://[^ ]*', invite_message.body).group(0)
        parsed_link = urlparse.urlsplit(link)

        self.assertEqual(parsed_link.netloc, self.client.defaults['HTTP_HOST'])

        self.client.logout()
        resp = self.client.get(parsed_link.path)
        self.assertContains(resp, 'Welcome to SayIt')

        resp = self.client.post(
            parsed_link.path,
            {'password1': 'password', 'password2': 'password'},
            follow=True,
            )
        self.assertRedirects(resp, '/', status_code=302)

        self.assertContains(
            resp,
            'You can now create and edit speeches and sections',
            )

        # Check that sharee is now logged in, following
        # http://stackoverflow.com/a/6013115/517418
        self.assertEqual(self.client.session['_auth_user_id'], sharee.pk)

        # Check we can log out and in again with the new credentials
        self.client.logout()
        self.assertTrue(
            self.client.login(
                email='newsharee@example.com', password='password')
            )

    def test_share_with_unknown_user_long_email(self):
        resp = self.client.post(
            '/instance/share',
            {'email': 'what_a_long_email_address@example.com'},
            )

        sharee = get_user_model().objects.get(
            email='what_a_long_email_address@example.com')
        self.instance.users.get(pk=sharee.id)
        self.assertRedirects(resp, '/instance/share', status_code=302)

        # Verify that the subject of the first message is correct.
        self.assertIn(
            'You\'ve been invited to help edit "Test Instance"!',
            mail.outbox[0].subject,
            )
