# OGN Receiver Database

A parser for <http://wiki.glidernet.org/list-of-receivers>,
returns the list-of-receivers in a machine-readable [format](#data-format).

## Requirements

These scripts are written in python3 and need the python3-requests package.
If [pip](https://pip.pypa.io/en/stable/quickstart/) for python3 is availabe,
this dependency could be installed by

```
pip install -r requirements.txt
```

### Debian

On Debian the dependencies could be installed by

```
sudo apt-get install python3 python3-requests
```

## Usage

- mkreceiverjson.py

  Fetch the list-of-receivers from wiki.glidernet.org and output it
  into a (machine-readable) file `receivers.json`.

  ```
  mkreceiverjson.py --out receivers.json --obfuscate
  ```

- mkstatistics.py

  Generate some statistics from `receivers.json`.

  ```
  mkstatistics.py --in receivers.json
  ```

## Data format

### receivers.json

Specification: [receiverlist-schema-0.2.1](receiverlist-schema-0.2.1.json)

Example:
```json
{ "receivers":
  [
    {
      "callsign": "N0CALL",
      "description": "An OGN receiver located on planet earth. Raspberry Pi 3, colinear antenna",
      "photos": [
        "https://example.com/img/receiver.jpg",
        "https://example.com/img/antenna.jpg",
        "https://example.com/img/runway.jpg",
      ],
      "contact": "John Doe",
      "email": "john@example.com",
      "country": "None",
      "links": [
        {"href": "https://example.com/blog/installed-ogn-receiver-on-earth", "rel": "Blog"},
        {"href": "https://example.com/video.jpeg", "rel": "Webcam"}
      ]
    },
  ],
  "timestamp": "2016-02-04T11:11:11",
  "version": "0.2.1"
}
```

## Data analysis ([jq](https://stedolan.github.io/jq/) required)

Show all receiver callsigns, grouped by country:
```
cat receivers.json | jq ".receivers | group_by(.country) | map({(.[0].country): [.[].callsign]}) | add"
```

## License

Licensed under the [AGPLv3](LICENSE) or later.
