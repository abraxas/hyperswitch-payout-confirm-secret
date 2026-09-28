#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME=hyperswitch-payout-confirm-secret
BASE="${1:-http://127.0.0.1:18083}"
mkdir -p files
if [ ! -d hyperswitch-src/config ]; then
  echo "== clone Hyperswitch tag 2026.09.21.0 =="
  git clone --depth 1 --branch 2026.09.21.0 https://github.com/juspay/hyperswitch.git hyperswitch-src
fi
if [ -f poc.py ]; then
  POC=./poc.py
elif [ -f ../hyperswitch-payout-confirm-secret-Abraxas-Labs.py ]; then
  POC=../hyperswitch-payout-confirm-secret-Abraxas-Labs.py
else
  echo "FAIL no poc.py"
  exit 1
fi
chmod +x "$POC"

echo "== docker compose up (Hyperswitch router standalone, loopback) =="
docker compose up -d --build

echo "== wait for health =="
ok=0
for i in $(seq 1 90); do
  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 "$BASE/health" || true)"
  if [[ "$code" == "200" ]]; then
    echo "IOC hyperswitch-up http=$code"
    ok=1
    break
  fi
  echo "IOC wait i=$i http=$code"
  sleep 5
done
if [[ "$ok" != 1 ]]; then
  echo "FAIL Hyperswitch did not become ready on $BASE"
  docker compose logs --tail=80 hyperswitch-server
  exit 1
fi

echo "== poc.py =="
python3 "$POC" "$BASE"
