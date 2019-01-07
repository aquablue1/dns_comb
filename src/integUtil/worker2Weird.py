"""
" Get the hourly weird counting
" output: timestamp \t non-weird \t weird \n
" weird means the record has the corresponding weird log, dict["weird"] != "None"
" By Zhengping on 2019-01-06
"""

# Warning! This worker does not work, since weird type is not properly loaded by the outer input data structure.
# Update is needed.