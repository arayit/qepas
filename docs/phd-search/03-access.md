# Tooling: why group web pages cannot be read from this session

**1 September 2026.**

## What was tested

Direct fetches were attempted against institutional and reference domains, both through
the WebFetch tool and through `curl` on the command line:

`physik.hu-berlin.de`, `tu.berlin`, `mbi-berlin.de`, `fbh-berlin.de`, `fhi.mpg.de`,
`pc.fhi-berlin.mpg.de`, `amolf.nl`, `icfo.eu`, `arxiv.org`, `export.arxiv.org`,
`en.wikipedia.org`, `scholar.google.com`, `researchgate.net`, `journals.aps.org`,
`opg.optica.org`, `nature.com`, `orcid.org`, `euraxess.ec.europa.eu`,
`cordis.europa.eu`, `erc.europa.eu`, `api.openalex.org`, `api.crossref.org`,
`api.semanticscholar.org`, `api.openaire.eu`.

**All of them fail.** `curl -v` shows the cause precisely:

```
> CONNECT www.physik.hu-berlin.de:443 HTTP/1.1
< HTTP/1.1 403 Forbidden
* CONNECT tunnel failed, response 403
```

and the proxy's own status endpoint logs it as
`connect_rejected — gateway answered 403 to CONNECT (policy denial)`.

## What this means

A 403 on CONNECT is an **organization egress-policy denial**, not a broken proxy, not a
TLS problem, and not something a different tool or user-agent gets around. The session's
own documentation is explicit that policy denials must be reported rather than routed
around, so no mirror, cache or third-party proxy was tried.

**The only working channel is WebSearch**, which runs outside the container. That is
enough to identify people, read abstracts, confirm grants and prizes, and catch
retirements and moves. It is *not* enough to open a group's members page, read a
current vacancy list, or enumerate a department's staff — which is exactly the gap.

## The fix

In rough order of reliability:

1. **Run Claude Code locally.** The CLI on your own machine has no egress proxy at all.
   Every group page, every job list, arXiv, Scholar — all directly readable. For a
   search that is fundamentally about reading a few hundred university pages, this is
   the right tool.
2. **Change this environment's network policy.** Remote environments have a network
   policy chosen when the environment is created. In claude.ai: profile icon →
   Settings → **Capabilities** → *Code execution and file creation* → **Domain
   allowlist** → set to **All domains** (or add specific domains). Enterprise/admin
   equivalent: Organization settings → Capabilities → Code execution → *Allow network
   egress*. Note there are open bug reports about the allowlist not always propagating
   to the session proxy, so verify after changing it by asking for any page to be
   fetched.
3. **Paste pages in.** For a handful of specific groups, copying the page text into the
   conversation works fine and needs no configuration.

Until one of those happens, treat every group-structure and vacancy claim in these
documents as indirect, and check it before writing to anyone.
