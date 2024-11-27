Install qcad:

```bash
brew install qcad
```

Convert dwg to dxf:

```bash
/Applications/QCAD.app/Contents/Resources/qcad -export-dxf sc23-exhibitors.dwg
```

Process dxf:

```bash
./dxf2exhibitors.py sc24-exhibitors.dxf --output_file sc24-exhibitors.csv
```