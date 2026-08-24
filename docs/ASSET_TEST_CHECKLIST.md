# Asset test checklist

After building `drugwars_ti_nspire_cx2_graphical_v2.py` with the prepared BMP resources, verify these screens on the calculator:

- title screen shows the skyline banner
- Trenchcoat screen shows the coat image
- Travel screen shows the subway background
- mugging event shows the mugger artwork
- found-drugs event shows the dead-body artwork
- police events show the police-car artwork
- gun offers show the matching Beretta, snub, or .44 artwork
- doctor event shows the doctor artwork

If an event says `[art unavailable]`, the Python resource loader could not resolve that image name. Check the resource filename/order in the generated TNS and update `ASSET_SPECS` if necessary.
