SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = 'mysql://glad:glad9@localhost/glad'
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER='D:/myproject/genv/glad-web/uploads/'
BLOG_IMG_FOLDER='D:/myproject/genv/glad-web/uploads/blogs/'
UPLOAD_ANAL_FOLDER='D:/myproject/genv/glad-web/uploads/anal'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
CARS_PER_PAGE=15
POSTS_PER_PAGE=15
CONT_PER_PAGE=50

#markup blog용
BLOGGING_URL_PREFIX = "/blog"
BLOGGING_DISQUS_SITENAME = "test"
BLOGGING_SITEURL = "http://localhost:5000"
BLOGGING_SITENAME = "My Site"
BLOGGING_KEYWORDS = ["blog", "meta", "keywords"]
FILEUPLOAD_IMG_FOLDER = "fileupload"
FILEUPLOAD_PREFIX = "/fileupload"
FILEUPLOAD_ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
