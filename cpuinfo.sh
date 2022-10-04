#!/bin/sh -e

if (grep -q -e '^flags.*\badx\b' /proc/cpuinfo) 2>/dev/null; then
    echo "[present] adx"
else
    echo "[absent] adx"
fi
if (grep -q -e '^flags.*\bavx\b' /proc/cpuinfo) 2>/dev/null; then
    echo "[present] avx"
else
    echo "[absent] avx"
fi
if (grep -q -e '^flags.*\bavx2\b' /proc/cpuinfo) 2>/dev/null; then
    echo "[present] avx2"
else
    echo "[absent] avx2"
fi
