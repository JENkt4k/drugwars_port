# Embedded graphical assets

The graphical v2 game loads the BMP resources that Luna packs into the `.tns` file.

## Build order

The asset build must pass the prepared BMP files to Luna in this order:

1. `header_skyline.bmp`
2. `police_car.bmp`
3. `mugger.bmp`
4. `dead_body.bmp`
5. `trenchcoat.bmp`
6. `doctor.bmp`
7. `gun.bmp`
8. `gun_snub.bmp`
9. `gun_44.bmp`
10. `subwaybg.bmp`

`src/drugwars_ti_nspire_cx2_graphical_v2.py` attempts to load each resource by:

1. full BMP filename,
2. basename without extension,
3. insertion-order number.

That gives the game a fallback across the different ways TI-Nspire documents may expose embedded image names.

## Build

Using the existing WSL/Luna asset build pipeline, select the v2 source and produce a new `.tns` file. The resulting TNS should contain the ten BMP resource names above.

The v2 UI uses the images for:

- title skyline
- trenchcoat inventory
- subway travel
- mugging event
- dead-body/find event
- police market/chase/combat events
- three gun-offer variants
- doctor/healing event

If an asset cannot be loaded, the title retains its procedural skyline fallback and event screens remain usable rather than crashing.
