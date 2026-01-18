# BRLYT editing

First, see [tablets-brlan.md](tablets-brlan.md) for the general approach and the purpose
of this kind of document.

* WARNING: The linked Benzin doesn't round-trip userdata correctly, which breaks brlyt files.
  You need to get <https://github.com/HACKERCHANNEL/benzin/pull/2> running somehow. I'm sorry.

* Open `DATA/files/US/Layout/MenuPause.arc` with BrawlCrate
* Extract `blyt/pause_00.brlyt` in BrawlCrate
* Run `.\BENZIN.exe r pause_00.brlyt pause_00.xmlyt`

Apply the following changes:

```xml
diff --git a/./pause_00.xmlyt.orig b/./pause_00.xmlyt
index b556a7d..e465703 100644
--- a/./pause_00.xmlyt.orig
+++ b/./pause_00.xmlyt
@@ -43705,6 +43705,8 @@
                        <tag type="grp1" name="G_mogura_00">
                                <subs>
                                        <sub>N_mogura_00</sub>
+                                       <sub>N_icon_06</sub>
+                                       <sub>N_icon_05</sub>
                                        <sub>P_shadow_08</sub>
                                        <sub>P_shadow_05</sub>
                                </subs>
```

* Run `.\BENZIN.exe w pause_00.xmlyt pause_00.brlyt`

You now have a pause menu that will correctly display the icon for Mogma Mitts if you have them.