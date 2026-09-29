# Riveted-Joint Mendeley Metadata Structure Audit v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN METADATA-ONLY FOLLOW-UP
**Parent:** RIVET_MENDELEY_SOURCE_DISCOVERY_v0.1.md
**Evidence class:** PUBLIC DATASET INTAKE / NO NUMERIC FRF ACCESS

## Trigger

The parent discovery established that the public Mendeley JSON endpoint is reachable for both datasets but did not extract a direct file route.

## Purpose

Recursively inspect only the public JSON metadata structure to recover file descriptors, names, identifiers, and URL/download fields without requesting any file body.

## Allowed fields

Record:
- top-level JSON keys;
- recursive key paths whose key names include file, name, id, url, href, download, content, mime, size, checksum, hash, or uuid;
- scalar values associated with those paths;
- any string value containing data.h5 or Structure_images.

Long free-text descriptions are excluded.

## Prohibited operations

- no file-body GET;
- no HDF5 open;
- no FRF values;
- no signal-derived design decisions.

## Dispositions

- FILE_DESCRIPTOR_DISCOVERED if a public data.h5 filename plus stable file identifier or URL/download field is recovered.
- FILE_NAME_ONLY if data.h5 is named but no stable route/identifier is present.
- METADATA_STRUCTURE_INSUFFICIENT otherwise.

A discovered file descriptor permits a separately frozen HEAD/layout intake.
