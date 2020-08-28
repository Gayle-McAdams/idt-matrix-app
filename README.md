# idt-matrix-app
Dash app to compute 3x3 Input Device Transform matrix.

This Dash app takes in a .csv file of a camera's spectral sensitivities and computes a 3x3 IDT Matrix based off of ACES procedure document P-2013-001. 

KNOWN ISSUES:
'Upload' Dash component does not allow access to path to user uploaded files which is required for colour science IDT matrix code. In this commit, the path is hard-coded in for proof of concept. 
