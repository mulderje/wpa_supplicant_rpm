diff -up wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h.atoi wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h
--- wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h.atoi	2006-12-09 19:38:48.000000000 -0500
+++ wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h	2008-02-22 11:51:28.000000000 -0500
@@ -10,6 +10,7 @@
 ** destructor.
 *****************************************************************************/
 
+#include <stdlib.h>
 
 enum {
     AUTH_NONE = 0,
diff -up wpa_supplicant-0.5.7/wpa_gui/wpagui.ui.h.atoi wpa_supplicant-0.5.7/wpa_gui/wpagui.ui.h
--- wpa_supplicant-0.5.7/wpa_gui/wpagui.ui.h.atoi	2008-02-22 14:39:19.000000000 -0500
+++ wpa_supplicant-0.5.7/wpa_gui/wpagui.ui.h	2008-02-22 14:39:31.000000000 -0500
@@ -16,6 +16,7 @@
 #include <unistd.h>
 #endif
 
+#include <stdlib.h>
 
 void WpaGui::init()
 {
diff -up wpa_supplicant-0.5.7/wpa_gui/userdatarequest.ui.h.atoi wpa_supplicant-0.5.7/wpa_gui/userdatarequest.ui.h
--- wpa_supplicant-0.5.7/wpa_gui/userdatarequest.ui.h.atoi	2008-02-22 14:38:32.000000000 -0500
+++ wpa_supplicant-0.5.7/wpa_gui/userdatarequest.ui.h	2008-02-22 14:38:56.000000000 -0500
@@ -10,6 +10,8 @@
 ** destructor.
 *****************************************************************************/
 
+#include <stdlib.h>
+
 int UserDataRequest::setParams(WpaGui *_wpagui, const char *reqMsg)
 {
     char *tmp, *pos, *pos2;
