# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _

from django.contrib.auth.models import User, Permission

from idios.models import ProfileBase, create_profile

from geonode.layers.enumerations import COUNTRIES
from geonode.people.enumerations import ROLE_VALUES, CONTACT_FIELDS


class Contact(ProfileBase):
    name = models.CharField(_('Individual Name'), max_length=255, blank=True, null=True, help_text=_('name of the responsible personsurname, given name, title separated by a delimiter'))
    organization = models.CharField(_('Organization Name'), max_length=255, blank=True, null=True, help_text=_('name of the responsible organization'))
    profile = models.TextField(_('Profile'), null=True, blank=True)
    position = models.CharField(_('Position Name'), max_length=255, blank=True, null=True, help_text=_('role or position of the responsible person'))
    voice = models.CharField(_('Voice'), max_length=255, blank=True, null=True, help_text=_('telephone number by which individuals can speak to the responsible organization or individual'))
    fax = models.CharField(_('Facsimile'),  max_length=255, blank=True, null=True, help_text=_('telephone number of a facsimile machine for the responsible organization or individual'))
    delivery = models.CharField(_('Delivery Point'), max_length=255, blank=True, null=True, help_text=_('physical and email address at which the organization or individual may be contacted'))
    city = models.CharField(_('City'), max_length=255, blank=True, null=True, help_text=_('city of the location'))
    area = models.CharField(_('Administrative Area'), max_length=255, blank=True, null=True, help_text=_('state, province of the location'))
    zipcode = models.CharField(_('Postal Code'), max_length=255, blank=True, null=True, help_text=_('ZIP or other postal code'))
    country = models.CharField(choices=COUNTRIES, max_length=3, blank=True, null=True, help_text=_('country of the physical address'))
    email = models.EmailField(blank=True, null=True, help_text=_('address of the electronic mailbox of the responsible organization or individual'))

    # MBDC extensions
    website_url = models.URLField(default="http://", blank=True, null=True)
    mapc_newsletter = models.BooleanField(default=True)
    mbdc_newsletter = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-last_modified']

    def clean(self):
        # the specification says that either name or organization should be provided
        valid_name = (self.name != None and self.name != '')
        valid_organization = (self.organization != None and self.organization !='')
        if not (valid_name or valid_organization):
            raise ValidationError('Either name or organization should be provided')

    def get_absolute_url(self):
        return ('profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.organization)


class Role(models.Model):
    """
    Roles are a generic way to create groups of permissions.
    """
    value = models.CharField('Role', choices=ROLE_VALUES, max_length=255, unique=True, help_text=_('function performed by the responsible party'))
    permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)

    def __unicode__(self):
        return self.get_value_display()


def create_user_profile(instance, sender, created, **kwargs):
    try:
        profile = Contact.objects.get(user=instance)
    except Contact.DoesNotExist:
        profile = Contact(user=instance)
        profile.name = instance.username
        profile.save()

# Remove the idios create_profile handler, which interferes with ours.
signals.post_save.disconnect(create_profile, sender=User)
signals.post_save.connect(create_user_profile, sender=User)
