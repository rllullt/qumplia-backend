from django.db import models
from django.conf import settings

class Campaign(models.Model):
    """
    Model representing a marketing campaign.
    """
    name = models.CharField(max_length=255, verbose_name='Campaign Name')
    description = models.TextField(verbose_name='Campaign Description')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Update Date')
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    reject_reason = models.TextField(
        blank=True,
        verbose_name='Reason for Rejection'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_campaigns',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Created By'
    )
    last_time_checked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reviewed_campaigns',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Last Time Checked By'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        ordering = ['-creation_date'] # Default order by descending creation date


class CampaignImage(models.Model):
    """
    Model representing an image associated with a marketing campaign.
    """
    campaign = models.ForeignKey(Campaign, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='campaign_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{campaign_name} - {image_name}".format(campaign_name=self.campaign.name, image_name=self.image.name)
