DEFINES+=PROJECT_CONF_H=\"project-conf.h\"
CONTIKI_PROJECT = broadcast

all: $(CONTIKI_PROJECT)

CONTIKI_WITH_IPV6 = 1

CONTIKI = ../..
include $(CONTIKI)/Makefile.include
