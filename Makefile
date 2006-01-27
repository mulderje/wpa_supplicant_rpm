# Makefile for source rpm: wpa_supplicant
# $Id$
NAME := wpa_supplicant
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
