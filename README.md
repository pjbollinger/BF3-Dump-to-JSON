BF3-Dump-to-JSON
================

This project was created to provide a means of converting BF3 text file dumps into usable JSON.

## Usage

Run `main.py` with a BF3 text dump in the same directory.

The program will prompt you for a file name.

### Example of successful usage

```
What file would you like to turn into JSON? (example.txt) Handcuff.txt
Handcuff.txt -----> Handcuff.json conversion complete.
```

### Example of input file

```
0000XXXX    BlahBlahData 2112156e454a5ea5454878
0000XXXX        $::BlahBlahData
0000XXXX            $::BlahBlahAsset
0000XXXX                $::BlahBlahContainer
0000XXXX                BlahBlah *nullString*
0000XXXX        BlahBlah::BlahBlah
0000XXXX            BlahBlah1 0.0
0000XXXX            BlahBlah2 0.0
0000XXXX            BlahBlah3 0.0
0000XXXX            BlahBlah4 0.0
0000XXXX        BlahBlah1 False
0000XXXX        BlahBlah2 True
0000XXXX        BlahBlah3 False
0000XXXX        BlahBlah4 False
0000XXXX        BlahBlah5 0.0
```

### Example of output JSON file

```json
{
    "BlahBlahData": {
        "$::BlahBlahData": {
            "$::BlahBlahAsset": {
                "$::BlahBlahContainer": null,
                "BlahBlah": "*nullString*",
                "properties": null,
                "value": null
            },
            "properties": null,
            "value": null
        },
        "BlahBlah1": "False",
        "BlahBlah2": "True",
        "BlahBlah3": "False",
        "BlahBlah4": "False",
        "BlahBlah5": "0.",
        "BlahBlah::BlahBlah": {
            "BlahBlah1": "0.0",
            "BlahBlah2": "0.0",
            "BlahBlah3": "0.0",
            "BlahBlah4": "0.0",
            "properties": null,
            "value": null
        },
        "properties": null,
        "value": null
    }
}
```
