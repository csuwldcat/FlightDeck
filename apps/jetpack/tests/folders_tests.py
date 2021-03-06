from test_utils import TestCase

from django.contrib.auth.models import User
from nose import SkipTest

from jetpack.models import Package, PackageRevision, Module, EmptyDir, \
        Attachment


class FolderTest(TestCase):
    fixtures = ['mozilla_user', 'users', 'packages']

    def setUp(self):
        self.author = User.objects.get(username='john')
        self.path = 'util';

    def test_folder_removed_when_modules_added(self):
        " EmptyDir's shouldn't exist if there are modules inside the 'dir' "
        addon = Package(author=self.author, type='a')
        addon.save()
        revision = PackageRevision.objects.filter(package__name=addon.name)[0]

        folder = EmptyDir(name=self.path, author=self.author, root_dir='l')
        folder.save()
        revision.folder_add(folder)
        self.assertEqual(1, revision.folders.count())

        mod = Module(
            filename='/'.join([self.path, 'helpers']),
            author=self.author,
            code='//test code'
        )
        mod.save()
        revision.module_add(mod)
        self.assertEqual(0, revision.folders.count())

        mod = Module(
            filename='model',
            author=self.author,
            code='//test code'
        )
        mod.save()
        revision.module_add(mod)
        self.assertEqual(0, revision.folders.count())

    def test_folder_added_when_modules_removed(self):
        " EmptyDir's should be added if all modules in a 'dir' are removed "
        addon = Package(author=self.author, type='a')
        addon.save()
        revision = PackageRevision.objects.filter(package__name=addon.name)[0]

        mod = Module(
            filename='/'.join([self.path, 'helpers']),
            author=self.author,
            code='//test code'
        )
        mod.save()
        revision.module_add(mod)
        self.assertEqual(0, revision.folders.count())

        revision.module_remove(mod)
        self.assertEqual(1, revision.folders.count())
        self.assertEqual(self.path, revision.folders.all()[0].name)

    def test_folder_removed_when_attachments_added(self):
        " EmptyDir's shouldn't exist if there are attachments inside the 'dir' "
        addon = Package(author=self.author, type='a')
        addon.save()
        revision = PackageRevision.objects.filter(package__name=addon.name)[0]

        folder = EmptyDir(name=self.path, author=self.author, root_dir='d')
        folder.save()
        revision.folder_add(folder)
        self.assertEqual(1, revision.folders.count())

        att = Attachment(
            filename='/'.join([self.path, 'helpers']),
            author=self.author,
            ext='js'
        )
        att.save()
        revision.attachment_add(att)
        self.assertEqual(0, revision.folders.count())

        att = Attachment(
            filename='model',
            author=self.author,
            ext='html'
        )
        att.save()
        revision.attachment_add(att)
        self.assertEqual(0, revision.folders.count())

    def test_folder_added_when_attachments_removed(self):
        " EmptyDir's should be added if all attachments in a 'dir' are removed "
        addon = Package(author=self.author, type='a')
        addon.save()
        revision = PackageRevision.objects.filter(package__name=addon.name)[0]

        att = Attachment(
            filename='/'.join([self.path, 'helpers']),
            author=self.author,
            ext='js'
        )
        att.save()
        revision.attachment_add(att)
        self.assertEqual(0, revision.folders.count())

        revision.attachment_remove(att)
        self.assertEqual(1, revision.folders.count())
        self.assertEqual(self.path, revision.folders.all()[0].name)
