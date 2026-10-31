# Official macro calendar verification

Use this workflow for scheduled market events, central-bank speeches, and
event-aware analysis. It is agent guidance, not an implemented calendar fetcher
or a requirement to query every calendar during ordinary stock analysis.

## Scope and evidence

Company disclosures and stock news in `15_events` do not establish complete
macro-calendar coverage. Keep company events and macro events separate.
Select official calendars for the requested market and date range; the US
sources below are not a complete global calendar.

Search tools may help discover an event, but verify material dates, times,
speakers, and status against the issuing institution's page or public feed.
Link the source and record when it was checked. Do not require a particular
search provider.

## US official sources

| Source | Coverage and access |
|---|---|
| [BEA release dates JSON](https://apps.bea.gov/API/signup/release_dates.json) | GDP, Personal Income and Outlays / PCE, and other BEA releases. Public machine-readable schedule; do not assume a stable API contract or complete future coverage. |
| [BEA release schedule](https://www.bea.gov/news/schedule) | Official page for checking schedule coverage and changes when the JSON is incomplete or unavailable. |
| [Federal Reserve Board calendar](https://www.federalreserve.gov/newsevents/calendar.htm) | Board events, scheduled speeches, and releases; follow the relevant month and event links. |
| [FOMC calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) | Meeting dates and associated official materials; distinguish the meeting window from statement and press-conference times. |
| [BLS release schedule](https://www.bls.gov/schedule/) | Employment, CPI, PPI, JOLTS, and other BLS releases; select the requested month or year. |
| [Kansas City Fed symposium](https://www.kansascityfed.org/research/jackson-hole-economic-symposium/) | During the Jackson Hole window, check the relevant year's official agenda rather than assuming a speaker or time from a previous year. |

These sources include both JSON and web pages, not interchangeable JSON APIs.
Validate the returned date coverage and structure; deduplicate repeated feed
entries. An HTTP success alone does not establish usable or current coverage.

## Time and publication status

- Preserve the source's date, time, and timezone. For US events, show ET and
  the user's requested timezone, with calendar dates when conversion crosses
  midnight. Use IANA zones such as `America/New_York` for daylight-saving
  conversion, not a fixed UTC offset. If the user's timezone is unknown, label
  ET and UTC instead of guessing their location.
- Keep scheduled, verified released/delivered, postponed, cancelled, and
  unverified status distinct. A passed scheduled time does not prove that a
  release or speech occurred; verify the official release, transcript, or
  other official evidence before reporting its contents.
- If no exact time is published, say so. Do not invent a timestamp or reuse an
  earlier year's agenda.

## Missing data and reporting

Check cached data's retrieval time, covered dates, and completeness before
reuse. When a source fails, is stale, or does not cover the requested period,
try an available official alternative and disclose any unresolved gap. Do not
turn timeouts, parsing errors, empty company-news results, or missing calendar
coverage into "no events today."

Even after successful checks, qualify negative findings: "No relevant events
found in the checked sources for this date range," naming those sources and
any coverage limits. Keep verified events separate from unverified candidates.

For each material event, report its category, title, scheduled time and status,
official source, and verification time. Separate confirmed facts from inferred
market implications. This workflow does not authorize new recurring alerts or
trades, and a scheduled catalyst alone is not a buy/sell signal.
