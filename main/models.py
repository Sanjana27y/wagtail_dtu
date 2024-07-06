from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.blocks import StructBlock, CharBlock, TextBlock, RichTextBlock
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtailmedia.edit_handlers import MediaChooserPanel

class HomePage(Page):
    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    intro = RichTextField(blank=True)
    big_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('logo'),
        FieldPanel('intro', classname="full"),
        FieldPanel('big_image'),
        InlinePanel('homepage_announcements', label="Announcements"),
        InlinePanel('important_links', label="Important Links"),
        InlinePanel('facilities', label="Facilities"),
        # MultiFieldPanel(
        #     [
        #         InlinePanel('facilities', label="Facilities"),
        #     ],
        #     heading="Facilities",
        # ),        
        InlinePanel('web_resources', label="Web Resources"),
        # InlinePanel('contact_us', label="Contact Us"),
    ]

class HomePageAnnouncement(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='homepage_announcements')
    title = models.CharField(max_length=250)
    link = models.URLField()

    panels = [
        FieldPanel('title'),
        FieldPanel('link'),
    ]

class ImportantLink(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='important_links')
    title = models.CharField(max_length=250)
    link = models.URLField()

    panels = [
        FieldPanel('title'),
        FieldPanel('link'),
    ]

class Facility(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='facilities')
    title = models.CharField(max_length=250)
    video = models.ForeignKey(
        'wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )


    panels = [
        FieldPanel('title'),
        MediaChooserPanel('video'),
    ]

class WebResource(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='web_resources')
    title = models.CharField(max_length=250)
    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    link = models.URLField()

    panels = [
        FieldPanel('title'),
        FieldPanel('logo'),
        FieldPanel('link'),
    ]

# class ContactUs(Orderable):
#     page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='contact_us')
#     text = models.CharField(max_length=250)
#     link = models.URLField()

#     panels = [
#         FieldPanel('text'),
#         FieldPanel('link'),
#     ]





class AboutUsPage(Page):
    intro = RichTextField(blank=True)
    vision_mission = StreamField(
        [('paragraph', blocks.RichTextBlock())], null=True, blank=True)
    history = StreamField(
        [('paragraph', blocks.RichTextBlock())], null=True, blank=True)
    core_values = StreamField(
        [('paragraph', blocks.RichTextBlock())], null=True, blank=True)
    research = StreamField(
        [('paragraph', blocks.RichTextBlock())], null=True, blank=True)
    campus_map = StreamField(
        [('image', ImageChooserBlock())], null=True, blank=True)
  
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('vision_mission'),
        FieldPanel('history'),
        FieldPanel('core_values'),
        FieldPanel('research'),
        FieldPanel('campus_map'),
    ]

class CoursesPage(Page):
    intro = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('courses', label="Courses"),
    ]

class Course(Orderable):
    page = ParentalKey('main.CoursesPage', on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',null=True, blank= True,  on_delete=models.SET_NULL, related_name='+'
    )
    pdf = models.ForeignKey(
        'wagtaildocs.Document',null=True, blank= True,  on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels +[
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image'),
        FieldPanel('pdf'),
    ]

class FacultyPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('branches', label="Branches"),
    ]

class Branch(Orderable):
    page = ParentalKey('main.FacultyPage', on_delete=models.CASCADE, related_name='branches')
    title = models.CharField(max_length=250)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    branch_faculty_page = models.ForeignKey('FacultyBranchPage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('title'),
        FieldPanel('image'),
        PageChooserPanel('branch_faculty_page'),
    ]

class FacultyBranchPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('faculties', label="Faculties"),
    ]

class Faculty(Orderable):
    page = ParentalKey(FacultyBranchPage, on_delete=models.CASCADE, related_name='faculties')
    name = models.CharField(max_length=250)
    designation = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    panels = [
        FieldPanel('name'),
        FieldPanel('designation'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('image'),
    ]



class GalleryPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('headings', label="Gallery Headings"),
    ]

class GalleryHeading(ClusterableModel):
    page = ParentalKey('main.GalleryPage', on_delete=models.CASCADE, related_name='headings')
    title = models.CharField(max_length=250)

    panels = [
        FieldPanel('title'),
        InlinePanel('images', label="Images"),
    ]

class GalleryImage(Orderable):
    heading = ParentalKey('main.GalleryHeading', on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    caption = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

class PublicationsPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('years', label="Years"),
    ]

class PublicationYear(ClusterableModel):
    page = ParentalKey('main.PublicationsPage', on_delete=models.CASCADE, related_name='years')
    year = models.CharField(max_length=4)

    panels = [
        FieldPanel('year'),
        InlinePanel('publications', label="Publications"),
    ]

class Publication(Orderable):
    year = ParentalKey('main.PublicationYear', on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=250)
    authors = models.CharField(max_length=500)
    link = models.URLField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('authors'),
        FieldPanel('link'),
    ]
class AdmissionPage(Page):
    intro_heading = models.CharField(max_length=250, blank=True)
    intro_text = RichTextField(blank=True)
    allotment_notice = models.CharField(max_length=250, blank=True)
    allotment_link = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('announcements', label="Announcements"),
        FieldPanel('intro_heading'),
        FieldPanel('intro_text'),
        FieldPanel('allotment_notice'),
        FieldPanel('allotment_link'),
    ]

class Announcement(Orderable):
    page = ParentalKey('main.AdmissionPage', on_delete=models.CASCADE, related_name='announcements')
    text = models.CharField(max_length=250)
    link = models.URLField()

    panels = [
        FieldPanel('text'),
        FieldPanel('link'),
    ]

class ContactPage(Page):
    emergency_helpline = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    address_link = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('emergency_helpline', classname="full"),
        FieldPanel('contact_info', classname="full"),
        FieldPanel('email', classname="full"),
        FieldPanel('phone', classname="full"),
        FieldPanel('fax', classname="full"),
        FieldPanel('address', classname="full"),
        FieldPanel('address_link', classname="full"),
    ]