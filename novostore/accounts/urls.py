from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('accounts.views',
    (r'login/' , 'login'),
    (r'register/' , 'register'),
    (r'logout/' , 'logout'),
    (r'profile/' , 'profile'),
#    (r'auvk/' , 'vkauth'),
#    (r'vkemailconfcomplete/$' , 'vkemailconfirm_complete'),
#    (r'vkemailconfirm/' , 'vkemailconfirm'),
#    (r'channelfb/','fbchannel'),
#    (r'aufb/','fbauth'),
#    (r'apifb/','fbauthapi'),
    (r'restorepasswd/','email_for_restorepassword'),
    (r'change_password/','change_password'),
    (r'combinecarts/','combinecarts'),
    (r'new-users-redirect-url/','change_password_by_new_social_user'),
    (r'saveprofileajax/','saveprofileajax')
)