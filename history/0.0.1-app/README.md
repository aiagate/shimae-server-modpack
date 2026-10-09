# 0.0.1 App migration evidence

These files preserve the original tracked App provenance, references, preparation
record, override review policy and release metadata byte-for-byte. They formerly
lived in `exports/` and the root `release.json`; recorded paths describe that
historical layout. They are audit evidence, not current build or upload inputs.
The current source is `pack/`; migration checks use `pack/migration.json`.
Published ZIPs, original user exports and acceptance receipts remain unchanged
in their existing Release/local locations. No historical upload code is needed
to read these records.
