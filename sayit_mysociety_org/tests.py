import re
import urlparse

from django.core import mail
from django.contrib.auth import get_user_model

from instances.tests import InstanceTestCase


class ShareInstanceTests(InstanceTestCase):
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
            'You have been invited to a SayIt',
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
            'You have been invited to a SayIt',
            invite_message.subject,
            )

        # Get the link out of the invitation email
        link = re.search(r'http://.*/\n', invite_message.body).group(0)
        parsed_link = urlparse.urlsplit(link)

        self.assertEqual(parsed_link.netloc, self.client.defaults['HTTP_HOST'])

        self.client.logout()
        resp = self.client.get(parsed_link.path)
        self.assertContains(resp, 'Accept invitation')

        resp = self.client.post(
            parsed_link.path,
            {'password1': 'password', 'password2': 'password'},
            )
        self.assertRedirects(resp, '/', status_code=302)

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
            'You have been invited to a SayIt',
            mail.outbox[0].subject,
            )
