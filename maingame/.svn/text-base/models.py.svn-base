from django.db import models
class Story(models.Model):
    storyId = models.IntegerField()
    topic = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)
    memberNum = models.IntegerField()
    startItem = models.IntegerField()
    def __unicode__(self):
        return u'%i-%s' % (self.storyId, self.topic)
#    def __unicode__(self):
#        return self.storyId
        
class Items(models.Model):
    storyId = models.ForeignKey(Story)
    itemId  = models.IntegerField()
    topic   = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)
    op1     = models.CharField(max_length=1000,blank=True,null = True)
    op1_next= models.IntegerField(blank=True,null = True)
    op2     = models.CharField(max_length=1000,blank=True,null = True)
    op2_next= models.IntegerField(blank=True,null = True)
    op3     = models.CharField(max_length=1000,blank=True,null = True)
    op3_next= models.IntegerField(blank=True,null = True)
    op4     = models.CharField(max_length=1000,blank=True,null = True)
    op4_next= models.IntegerField(blank=True,null = True)
    op5     = models.CharField(max_length=1000,blank=True,null = True)
    op5_next= models.IntegerField(blank=True,null = True)
    op6     = models.CharField(max_length=1000,blank=True,null = True)
    op6_next= models.IntegerField(blank=True,null = True)
    isend     = models.IntegerField()
    isStart = models.IntegerField()
    def __unicode__(self):
        return u'%i-%s' % (self.itemId, self.topic)
#    def __unicode__(self):
#        return u'%i %s' % (self.storyId, self.topic)

class Users(models.Model):
    usrname = models.CharField(max_length=1000)
    storyId = models.ForeignKey(Story)
    current = models.IntegerField()
    currentId = models.IntegerField()
    history = models.CharField(max_length=1000)
    isover  = models.IntegerField()
    def __unicode__(self):
        return u'%s-%i' % (self.usrname, self.current)
#    def __unicode__(self):
#        return u'%i %i' % (self.current, self.storyId)

class Users_Current(models.Model):
    usrname = models.CharField(max_length=1000)
    storyId = models.ForeignKey(Story)
    current = models.IntegerField()
    currentId = models.IntegerField()
    isover  = models.IntegerField()
    location= models.IntegerField()
    finished_story=models.CharField(max_length=1000,blank=True,null = True)
    def __unicode__(self):
        return u'%s-%i' % (self.usrname, self.location)
