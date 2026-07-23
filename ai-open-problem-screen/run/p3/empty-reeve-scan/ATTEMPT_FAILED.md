# Failed pre-panel attempt

The first direct-scan freeze attempt stopped before `panel.json` was written.
The deterministic panel validator compared an allocation map containing
zero-quota strata with an observed-entry counter that naturally omitted those
zero-count keys. The exact B1 support enumeration completed without an anchor
error; no geometry or stretched-polynomial query ran.

The attempt is preserved rather than overwritten. The bookkeeping validator was
fixed to compare over the complete allocated stratum set, and the identical
seed/selection algorithm was restarted in `run/p3/empty-reeve-scan-v2`.
