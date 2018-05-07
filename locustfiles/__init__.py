# from locustfiles.locustfile_example import WebsiteUser
from locustfiles.search_httplocust import SearchUser
from locustfiles.upload_dsslocust import UploadUser
from locustfiles.download_dsslocust import DownloadUser
from locustfiles.checkout_dsslocust import CheckoutUser
from locustfiles.notify_dsslocust import NotifiedUser

locustTest_1 = {SearchUser: 2, UploadUser: 5, DownloadUser: 3, CheckoutUser: 4, NotifiedUser: 4}