from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), help_text=_('for direct access on the website of an author'))
    email = models.EmailField(_('email adress'))
    url = models.URLField(_('personal website'), null=True, blank=True, verify_exists=False)
    bio = models.TextField(_('bio'), help_text=_('HTML please, optional'), null=True, blank=True)

    class Meta:
        verbose_name = _('Author')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/authors/#%s' % (self.slug)
