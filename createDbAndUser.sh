#!/usr/bin/env bash
set -e

psql -U postgres -c "CREATE ROLE zeroecks LOGIN  PASSWORD 'zeroecks'"
psql -U postgres -d postgres -c "CREATE DATABASE zeroecks OWNER zeroecks"
