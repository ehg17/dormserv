from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	ALSPLAUGH = 'ALS'
	BASSETT = 'BAS'
	BROWN = 'BRO'
	PEGRAM = 'PEG'
	AYCOCK = 'AYC'
	EPWORTH = 'EPW'
	GILES = 'GIL'
	JARVIS = 'JAR'
	WILSON = 'WIL'
	GILBERT_ADDOMS = 'GAD'
	SOUTHGATE = 'SOU'
	BELL_TOWER = 'BTW'
	BLACKWELL = 'BLA'
	RANDOLPH = 'RAN'
	CRAVEN = 'CRA'
	CROWELL = 'CRO'
	WANNAMAKER = 'WAN'
	EDENS = 'EDE'
	FEW = 'FEW'
	KEOHANE = 'KEO'
	KILGO = 'KIL'
	EAST = 'EAS'
	CENTRAL = 'CEN'
	BLANK = '   '
	QUAD_CHOICES = (
		(BLANK, 'Choose a quad...'),
		(CENTRAL, 'Central Campus'),
		(ALSPLAUGH, 'Alsplaugh'),
		(AYCOCK, 'Aycock'),
		(BASSETT, 'Bassett'),
		(BELL_TOWER, 'Bell Tower'),
		(BLACKWELL, 'Blackwell'),
		(BROWN, 'Brown'),
		(CRAVEN, 'Craven'),
		(CROWELL, 'Crowell'),
		(EDENS, 'Edens'),
		(EPWORTH, 'Epworth'),
		(FEW, 'Few'),
		(GILBERT_ADDOMS, 'Gilbert-Addoms'),
		(GILES, 'Giles'),
		(JARVIS, 'Jarvis'),
		(KEOHANE, 'Keohane'),
		(KILGO, 'Kilgo'),
		(PEGRAM, 'Pegram'),
		(RANDOLPH, 'Randolph'),
		(SOUTHGATE, 'Southgate'),
		(WANNAMAKER, 'Wannamaker'),
		(WILSON, 'Wilson'),
	)
	user = models.OneToOneField(User)
	dorm = models.CharField(max_length=3, choices=QUAD_CHOICES, default=BLANK)
	section = models.CharField(max_length=2)
	room = models.CharField(max_length=7)
	phone = models.CharField(max_length=20)



	def __unicode__(self):
		return self.user.username