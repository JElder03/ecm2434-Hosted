"""
Author: Victor Smith
"""

import qrcode

def genQrCode(group_name):
    """
    Generate a QR code for a given group which links to a group joining page

    # parameters
    group_name (str): The name of the group

    # return
    myqr (any): The QR code linking to the group joining page
    """
    
    qr_content = "http://127.0.0.1:8000/join_group/" + group_name
    myqr = qrcode.make(qr_content)
    return myqr
