#!/usr/bin/env bash
set -euo pipefail
python clip_esa_worldcover.py --aoi AOI_Naposta_Grande_shp.zip --out outputs "$@"
