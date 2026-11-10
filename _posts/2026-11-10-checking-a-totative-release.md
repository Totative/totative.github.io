---
title: Checking a Totative release
description: What we sign, what each release carries, and the commands that check it without taking our word for it.
---

A security shop asking you to trust its downloads is a bit rich. So every release from [github.com/Totative](https://github.com/Totative) can be checked without trusting us; here's how.

## What we sign

Every commit and tag in our public repositories is signed. Ours carry SSH signatures from keys registered on GitHub, and squash merges are signed by GitHub itself (so either way, GitHub shows them as Verified.)

Nothing reaches `main` by a direct push. A change goes through a pull request and a merge queue, and lands only once its CI and CodeQL checks pass on the merged result. Force-pushes and deleting `main` are refused.

## What a release carries

A release starts with a signed tag. Pushing it runs the repository's `release.yml` on GitHub's own runners, which builds the source tarball and an SPDX SBOM, then attaches two attestations to the tarball: build provenance (which repository, workflow and commit produced the file) and the SBOM (what went into it).

Both are signed through Sigstore and recorded in its public transparency log, Rekor. If we ever swapped a file after the fact, the log would still say what was built.

## Checking one

You'll need the [GitHub CLI](https://cli.github.com). Using go-avscan v0.3.0 as the example:

```sh
gh release download v0.3.0 --repo Totative/go-avscan --pattern '*.tar.gz'
gh attestation verify go-avscan-v0.3.0.tar.gz --owner Totative
gh attestation verify go-avscan-v0.3.0.tar.gz --owner Totative \
  --predicate-type https://spdx.dev/Document/v2.3
```

The first check passes only if GitHub Actions built that exact file from a Totative repository's workflow. The second confirms the SBOM was made for that same file.

A pass means the file you hold came from source you can read, built where we say it was; it says nothing about bugs in that source (that part is still on us.)

The attestations cover the tarball, not the `sbom.spdx.json` beside it, so point the check at the tarball. If you use one of our Go libraries through `go get`, the Go checksum database already pins each module version for you; that's a separate check from this one.

## If a check fails

Tell us. A failed verification, or a release with no attestation, counts as a vulnerability report, so send it the way our [security policy](https://github.com/Totative/.github/blob/main/SECURITY.md) describes rather than in a public issue.
