# Wormhole paper scripts

Run these utilities from the project root so their existing relative output
paths continue to place generated figures beside the TeX manuscripts:

```powershell
python scripts/make_observer_charge_channels_v7.py
```

The scripts share a few local modules in this directory. Invoking a script by
path, as above, keeps those imports working without installing a package.

