# US Money Supply API

Real-time US money supply data including M1, M2, monetary base, and velocity. Powered by FRED (Federal Reserve Economic Data).

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All money supply indicators snapshot |
| `GET /m1` | M1 money stock (M1SL) |
| `GET /m2` | M2 money stock (M2SL) |
| `GET /monetary-base` | Monetary base total (BOGMBASE) |
| `GET /velocity-m1` | Velocity of M1 money stock (M1V) |
| `GET /velocity-m2` | Velocity of M2 money stock (M2V) |

## Data Source

FRED - Federal Reserve Bank of St. Louis
https://fred.stlouisfed.org/

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
