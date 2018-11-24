"""
Order Service Runner

Start the Order Service and initializes logging
"""

import os
from app import app, service

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "****************************************"
    print " O R D E R   S E R V I C E   R U N N I N G"
    print "****************************************"
    service.initialize_logging()
    service.init_db()  # make our sqlalchemy tables
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
