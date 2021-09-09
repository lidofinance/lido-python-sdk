# CHANGELOG

All notable changes to this project are documented in this file.

This changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/lidofinance/lido-python-sdk)

## [2.1.2](https://github.com/lidofinance/lido-python-sdk) - 2021-09-09
### Changed
- Cache eth_chain_id value [#0037](https://github.com/lidofinance/lido-python-sdk/pull/37)

## [2.1.1](https://github.com/lidofinance/lido-python-sdk) - 2021-09-03
### Changed
- Update web3 from 5.23.0 to 5.23.1. Now "used" key is optional for verification [#0035](https://github.com/lidofinance/lido-python-sdk/pull/35)

## [2.1.0](https://github.com/lidofinance/lido-python-sdk) - 2021-09-03
### Added
- Add new params that could be provided to multicall [#0032](https://github.com/lidofinance/lido-python-sdk/pull/32)

## [2.0.1](https://github.com/lidofinance/lido-python-sdk) - 2021-09-01
### Changed
- Renamed library root package to `lido_sdk`, added more tests, fixed ABIs packaging [#0029](https://github.com/lidofinance/lido-python-sdk/pull/29)

## [1.0.1](https://github.com/lidofinance/lido-python-sdk) - 2021-08-31
### Added
- Lido public class [#0020](https://github.com/lidofinance/lido-python-sdk/pull/20)
- Added fast BLS verification [#0019](https://github.com/lidofinance/lido-python-sdk/pull/19)

### Changed
- If strict is false, for validation we will try possible WC only for already used keys [#0024](https://github.com/lidofinance/lido-python-sdk/pull/24)

## [0.3.0](https://github.com/lidofinance/lido-python-sdk) - 2021-08-26
### Fixed
- Move eth2deposit code to repository

## [0.2.0](https://github.com/lidofinance/lido-python-sdk) - 2021-08-26
### Added
- Github actions ([#0005](https://github.com/lidofinance/lido-python-sdk/pull/5))
- Contract interact and contract's multicall support ([#0006](https://github.com/lidofinance/lido-python-sdk/pull/6))
- Base operator's methods ([#0008](https://github.com/lidofinance/lido-python-sdk/pull/8))
- Key validation method ([#0011](https://github.com/lidofinance/lido-python-sdk/pull/11))
- Stats method ([#0013](https://github.com/lidofinance/lido-python-sdk/pull/11))

### Fixed
- Code coverage ([#0014](https://github.com/lidofinance/lido-python-sdk/pull/14))

## [0.1.0](https://github.com/lidofinance/lido-python-sdk) - 2021-08-20
### Added
- Initial release
- Setup configuration ([#0002](https://github.com/lidofinance/lido-python-sdk/pull/2))
