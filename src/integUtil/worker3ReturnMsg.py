"""
" check if the return message is 0 or not.
" for inbound traffic, sender is outer host, the return message is sent by receiver, so we should count resp_byte.
" for outbound traffic, sender is inner host, the return message is sent by receiver, so we still count resp_byte.
" dict["conn"][2]
" By Zhengping
"""