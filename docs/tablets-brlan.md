# BRLAN editing

In order for the randomizer to display the correct tablets and gemstones
in the pause menu (instead of a fixed order - Emerald, Ruby, Amber),
the randomizer requires patches to the brlan file that contains UI animation
data in a binary format. This document describes what changes were made,
since the changed binary file cannot be inspected and I'd like the process
to be reproducible in case someone wants to touch that file again.

Required tools:

* [BrawlCrate](https://github.com/soopercool101/BrawlCrate)
* [Benzin](https://horizon.miraheze.org/wiki/Benzin)

* Open `DATA/files/US/Layout/MenuPause.arc` with BrawlCrate
* Extract `anim/pause_00_sekiban.brlan` in BrawlCrate
* Run `.\BENZIN.exe r pause_00_sekiban.brlan pause_00_sekiban.xmlan`

Apply the following changes:

```xml
diff --git a/./pause_00_sekiban.orig.xmlan b/./pause_00_sekiban.xmlan
index 68919e6..316c9a9 100644
--- a/./pause_00_sekiban.orig.xmlan
+++ b/./pause_00_sekiban.xmlan
@@ -11,7 +11,8 @@
           <string>G_sekiban_00</string>
         </seconds>
       </pat1>
-      <pai1 framesize="5" flags="00">
+      <!-- our frames go from 0 to 7 -> 8 frames -->
+      <pai1 framesize="8" flags="00">
         <timg name="hm_moleGloveA_00.tpl" />
         <timg name="hm_moleGloveB_00.tpl" />
         <timg name="hm_swordA_00.tpl" />
@@ -32,6 +33,11 @@
         <timg name="uk_purseC_00.tpl" />
         <timg name="uk_purseD_00.tpl" />
         <timg name="uk_purseE_00.tpl" />
+        <!-- add the additional textures as indices 0x14-0x17 -->
+        <timg name="tr_sekiban_03.tpl" />
+        <timg name="tr_sekiban_04.tpl" />
+        <timg name="tr_sekiban_05.tpl" />
+        <timg name="tr_sekiban_06.tpl" />
         <pane name="P_shadow_00" type="0">
           <tag type="RLVI">
             <entry type1="0" type2="Visibility">
@@ -195,7 +201,8 @@
                 <padding>0000</padding>
               </pair>
               <pair>
-                <data1>3.000000000000000</data1>
+                <!-- hide entire tablets UI at 7 -->
+                <data1>7.000000000000000</data1>
                 <data2>0000</data2>
                 <padding>0000</padding>
               </pair>
@@ -1257,6 +1264,12 @@
                 <data2>0001</data2>
                 <padding>0000</padding>
               </pair>
+              <!-- add additional keyframes to gemstone -->
+              <pair>
+                <data1>4.000000000000000</data1>
+                <data2>0000</data2>
+                <padding>0000</padding>
+              </pair>
             </entry>
           </tag>
         </pane>
@@ -1273,6 +1286,17 @@
                 <data2>0001</data2>
                 <padding>0000</padding>
               </pair>
+              <!-- add additional keyframes to gemstone -->
+              <pair>
+                <data1>3.000000000000000</data1>
+                <data2>0000</data2>
+                <padding>0000</padding>
+              </pair>
+              <pair>
+                <data1>5.000000000000000</data1>
+                <data2>0001</data2>
+                <padding>0000</padding>
+              </pair>
             </entry>
           </tag>
         </pane>
@@ -1289,6 +1313,12 @@
                 <data2>0001</data2>
                 <padding>0000</padding>
               </pair>
+              <!-- add additional keyframes to gemstone -->
+              <pair>
+                <data1>6.000000000000000</data1>
+                <data2>0000</data2>
+                <padding>0000</padding>
+              </pair>
             </entry>
           </tag>
         </pane>
@@ -1674,6 +1704,27 @@
                 <data2>000b</data2>
                 <padding>0000</padding>
               </pair>
+              <!-- add tablet texture keyframes -->
+              <pair>
+                <data1>3.000000000000000</data1>
+                <data2>0014</data2>
+                <padding>0000</padding>
+              </pair>
+              <pair>
+                <data1>4.000000000000000</data1>
+                <data2>0015</data2>
+                <padding>0000</padding>
+              </pair>
+              <pair>
+                <data1>5.000000000000000</data1>
+                <data2>0016</data2>
+                <padding>0000</padding>
+              </pair>
+              <pair>
+                <data1>6.000000000000000</data1>
+                <data2>0017</data2>
+                <padding>0000</padding>
+              </pair>
             </entry>
           </tag>
         </pane>
```

* Run `.\BENZIN.exe w pause_00_sekiban.xmlan pause_00_sekiban.brlan`

Now you have a brlan file that works with the rando patches (cf. get_tablet_keyframe_count)