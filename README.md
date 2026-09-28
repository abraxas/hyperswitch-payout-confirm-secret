<p align="center">
  <img src="header.png" alt="Abraxas Labs — hyperswitch-payout-confirm-secret" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/hyperswitch-payout-confirm-secret">hyperswitch-payout-confirm-secret</a>
</p>

# hyperswitch-payout-confirm-secret

**Hyperswitch** `2026.09.21.0` — Juspay

Unpublished Hyperswitch source finding: POST /payouts/{id}/confirm with a publishable pk_ key only requires client_secret present, not equal to the stored payout secret, so a dummy secret can raise the stored amount. Payments confirm still compares the secret (IR_09). Amount is persisted before connector routing.

| | |
|---|---|
| ID | Unpublished Hyperswitch source finding #2 (no CVE yet) |
| CWE | [CWE-863, CWE-345](https://cwe.mitre.org/data/definitions/345.html) |
| CVSS | **High: 7.5** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Product | [Hyperswitch](https://github.com/juspay/hyperswitch) |
| Affected | all versions **through 2026.09.21.0** (inclusive) |
| Patched | vendor patch — see references |
| Auth | unauthenticated (see source map) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## Advisory (from the source map)

routes/payouts.rs 160-173 confirm=true + check_sdk_auth_and_get_auth. authentication.rs 5907-5934 pk_ presence-only. helpers.rs 1465-1484 amount applied. core/payouts.rs 702 before 721. Payments authenticate_client_secret is the bound control.

---

## Entry

- **Method:** `POST`
- **Path:** `/payouts/{payout_id}/confirm`
- **Router:** payouts_confirm forces confirm=true. check_sdk_auth_and_get_auth for pk_ only check_value_present(client_secret). helpers.rs applies amount before payouts_core.
- **Notes:** Unauthenticated unpublished Hyperswitch #2 CWE-863 2026.09.21.0. Needs merchant publishable key (pk_ on checkout) and payout_id. Witness: GET /payouts/{id} amount=99900. Payments confirm dummy secret is the control (IR_09). Not eval. Not a reverse shell. Disclose security@juspay.in, not a public GitHub issue.

### Call chain

- `POST /accounts admin_api_key=test_admin`
- `POST /api_keys/{merchant_id}`
- `POST /account/{merchant_id}/connectors worldpayxml payout_processor`
- `POST /payouts/create confirm=false amount=1000 card PMD`
- `POST /payments/{id}/confirm dummy client_secret (control, must be IR_09)`
- `POST /payouts/{id}/confirm api-key=pk_ client_secret=dummy amount=99900`
- `GET /payouts/{id} amount=99900`

### Lab preconditions

- Hyperswitch v1 router, payouts enabled
- Merchant publishable key pk_
- Payout in RequiresConfirmation with payout_method_data
- Amount write is the oracle even if connector routing returns IR_39

### Witness

GET /payouts/{id} amount=99900 after dummy client_secret confirm (created at 1000). Payments confirm dummy secret returns IR_09.

### Not success

- eval/base64/system payload
- reverse shell
- 401 unless client_secret matches payouts.client_secret
- amount stays 1000

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **Hyperswitch**. See references.

**Verify after upgrade**

- Re-run `hyperswitch-payout-confirm-secret-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm the vendor advisory / changeset in the deployed tree (see references).
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Disable or isolate the affected component.
- Hunt for the witness condition on production (new privileged users, unexpected files, injected rows — whatever this CVE's map names).

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:18083` (or the loopback you bound). Do not point this script at the internet.

```bash
python3 hyperswitch-payout-confirm-secret-Abraxas-Labs.py
```

Success is the **witness** above in the response body. Generic 200 HTML is not it.

---

## Lab images

Loopback stack used to reproduce. Official images unless a `Dockerfile` in this folder builds from source.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/run.sh`](lab/run.sh)

`./run.sh` clones Hyperswitch tag **2026.09.21.0** into `lab/hyperswitch-src` and starts `hyperswitch-router:standalone` on loopback `:18083`. Then:

```bash
cd lab
./run.sh
```

Publish nothing except `127.0.0.1`.

---

## References

- [github.com/juspay/hyperswitch](https://github.com/juspay/hyperswitch) tag 2026.09.21.0
- Vendor intake: [security@juspay.in](mailto:security@juspay.in) ([VDP](https://github.com/juspay/hyperswitch/wiki/Vulnerability-Disclosure-Program)). Do **not** open a public GitHub issue.

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# Hyperswitch unpublished #2 — payout confirm unbound client_secret

CWE: CWE-863, CWE-345
Severity: High 7.5 (HTTP lab SUCCESS, 95%)

## Description

`POST /payouts/{id}/confirm` authenticates a publishable `pk_` key by requiring `client_secret` present, not equal to `payouts.client_secret`. The confirm body is a full `PayoutCreateRequest`, so `amount` is written in `update_payouts_and_payout_attempt` before connector routing. Payments confirm still binds the secret (`IR_09`).

## Product

Hyperswitch tag 2026.09.21.0 source; lab image `hyperswitch-router:standalone` v1.127.0. Oracle: retrieve amount 99900 after dummy `client_secret` (created at 1000). Confirm HTTP 400 `IR_39` (no eligible payout connector on this image) after the amount write.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
