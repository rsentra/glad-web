activate_this = 'D:/myproject/genv/Scripts/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, 'D:/myproject/genv/glad-web')

from run import app as application