from pyteal import *
import base64

def approval_program():
    
    on_initialize = Seq([
        Approve()
    ])

    return on_initialize

def clear_program():
    return Approve()