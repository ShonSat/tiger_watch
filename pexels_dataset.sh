#!/bin/bash

PEXELS_API_KEY="71w5cHv2F67qos1m3dwV3wDNh0mkX3p8Zf6aigIHt90AYF0f05IvOT47"
curl -H "Authorization: PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=tigers?page=2&per_page=40"
