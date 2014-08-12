# -*- coding: utf-8 -*-

import re
import urlparse

from django.core import mail
from django.contrib.auth import get_user_model

from instances.tests import InstanceTestCase

from speeches.models import Speaker, Section
from instances.models import Instance

class SmokeTests(InstanceTestCase):
    """Very basic tests to make sure we can see anything at all."""
    def test_homepage(self):
        """Check that the home page for an empty instance returns OK."""
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)


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
            'You have been invited to a SayIt',
            mail.outbox[0].subject,
            )

class SlugTests(InstanceTestCase):

    def test_all_latin_speaker_slug(self):
        latin_speaker = Speaker.objects.create(
            name='Foo Bar',
            instance=self.instance
        )
        try:
            self.assertEqual(
                latin_speaker.slug,
                'foo-bar'
            )
        finally:
            latin_speaker.delete()

    def test_all_cjk_speaker_slug(self):
        cjk_speaker = Speaker.objects.create(
            name=u'張家祝',
            instance=self.instance
        )
        cjk_speaker_duplicate = Speaker.objects.create(
            name=u'張家祝',
            instance=self.instance
        )
        try:
            self.assertEqual(
                cjk_speaker.slug,
                'zhang-jia-zhu'
            )
            self.assertEqual(
                cjk_speaker_duplicate.slug,
                'zhang-jia-zhu-2'
            )
        finally:
            cjk_speaker.delete()
            cjk_speaker_duplicate.delete()

    def test_cyrillic_speaker_slug(self):
        cyrillic_speaker = Speaker.objects.create(
            name=u'борщ',
            instance=self.instance
        )
        try:
            self.assertEqual(
                cyrillic_speaker.slug,
                'borshch'
            )
        finally:
            cyrillic_speaker.delete()

    def test_all_cjk_section_slug(self):
        cjk_section = Section.objects.create(
            heading=u'經貿國是會議全國大會總結',
            instance=self.instance
        )
        try:
            self.assertEqual(
                cjk_section.slug,
                'jing-mao-guo-shi-hui-yi-quan-guo-da-hui-zong-jie'
            )
        finally:
            cjk_section.delete()
