diff -up wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h.atoi wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h
--- wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h.atoi	2008-02-22 11:46:35.000000000 -0500
+++ wpa_supplicant-0.5.7/wpa_gui/networkconfig.ui.h	2008-02-22 11:49:38.000000000 -0500
@@ -10,6 +10,7 @@
 ** destructor.
 *****************************************************************************/
 
+#include <stdlib.h>
 
 enum {
     AUTH_NONE = 0,
