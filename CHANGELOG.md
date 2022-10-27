# CHANGELOG

All notable changes to this project are documented in this file.

This changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[comment]: <> (## [Unreleased]&#40;https://github.com/lidofinance/lido-python-sdk&#41; - 2021-09-15)

## [2.6.0](https://github.com/lidofinance/lido-python-sdk) - 2022-10-27
### Added
- Support to ARM for linux. Move build blst to separate wf.

## [2.5.4](https://github.com/lidofinance/lido-python-sdk) - 2022-10-04
### Added
- Support to ARM, Update blst lib ([#0069](https://github.com/lidofinance/lido-python-sdk/pull/69))
- Fix for [2.5.2] release.

## [2.5.3](https://github.com/lidofinance/lido-python-sdk) - 2022-07-22
### Removed
- Removed PoA check for Goerli nerwork ([#0068](https://github.com/lidofinance/lido-python-sdk/pull/68))

## [2.5.2](https://github.com/lidofinance/lido-python-sdk) - 2022-04-01
### Fix
- Set upper bound to `multicall` version

## [2.5.1](https://github.com/lidofinance/lido-python-sdk) - 2022-04-01
### Changed
- Added Kiln network ([#0067](https://github.com/lidofinance/lido-python-sdk/pull/67))

## [2.5.0](https://github.com/lidofinance/lido-python-sdk) - 2021-02-15
### Changed
- Now python processes validates a bunch of keys (1000) instead of 1. ([#0065](https://github.com/lidofinance/lido-python-sdk/pull/65))

### Fix
- Fix typo in multicall decode code inputs.

## [2.4.7](https://github.com/lidofinance/lido-python-sdk) - 2021-12-28
### Changed
- Added Kintsugi network ([#0060](https://github.com/lidofinance/lido-python-sdk/pull/60))

## [2.4.6](https://github.com/lidofinance/lido-python-sdk) - 2021-12-28
### Fixed
- Library works correctly without typing_extensions when python >= 3.8 ([#0060](https://github.com/lidofinance/lido-python-sdk/pull/60))

## [2.4.5](https://github.com/lidofinance/lido-python-sdk) - 2021-12-22
### Changed
- Change library dependency ([#0059](https://github.com/lidofinance/lido-python-sdk/pull/59))

## [2.4.3](https://github.com/lidofinance/lido-python-sdk) - 2021-11-18
### Changed
- Fixes for configurable timeouts ([#0058](https://github.com/lidofinance/lido-python-sdk/pull/58))

## [2.4.2](https://github.com/lidofinance/lido-python-sdk) - 2021-11-17
### Added
- Added configurable timeouts for Pool and Thread Executors ([#0056](https://github.com/lidofinance/lido-python-sdk/pull/56))

## [2.4.1](https://github.com/lidofinance/lido-python-sdk) - 2021-11-09
### Added
- Fixed empty call_args when operators have zero unused keys while updating keys (`lido.update_keys`) ([#0054](https://github.com/lidofinance/lido-python-sdk/pull/54))

## [2.4.0](https://github.com/lidofinance/lido-python-sdk) - 2021-10-01
### Added
- Add ability to update keys in optimal way (`lido.update_keys`) ([#0050](https://github.com/lidofinance/lido-python-sdk/pull/50))

## [2.3.1](https://github.com/lidofinance/lido-python-sdk) - 2021-09-22
### Changed
- Move from req.txt to poetry ([#0048](https://github.com/lidofinance/lido-python-sdk/pull/48))

## [2.2.2](https://github.com/lidofinance/lido-python-sdk) - 2021-09-22
### Added
- Add Rinkeby support ([#0047](https://github.com/lidofinance/lido-python-sdk/pull/47))

## [2.2.0](https://github.com/lidofinance/lido-python-sdk) - 2021-09-14
### Changed
- Remove strict param from validate_keys method ([#0042](https://github.com/lidofinance/lido-python-sdk/pull/42))
- Fixed behavior when input is an empty array in lido methods ([#0043](https://github.com/lidofinance/lido-python-sdk/pull/43))

## [2.1.2](https://github.com/lidofinance/lido-python-sdk) - 2021-09-09
### Changed
- Cache eth_chain_id value ([#0037](https://github.com/lidofinance/lido-python-sdk/pull/37))

## [2.1.1](https://github.com/lidofinance/lido-python-sdk) - 2021-09-03
### Changed
- Update web3 from 5.23.0 to 5.23.1. Now "used" key is optional for verification ([#0035](https://github.com/lidofinance/lido-python-sdk/pull/35))

## [2.1.0](https://github.com/lidofinance/lido-python-sdk) - 2021-09-03
### Added
- Add new params that could be provided to multicall ([#0032](https://github.com/lidofinance/lido-python-sdk/pull/32))

## [2.0.1](https://github.com/lidofinance/lido-python-sdk) - 2021-09-01
### Changed
- Renamed library root package to `lido_sdk`, added more tests, fixed ABIs packaging ([#0029](https://github.com/lidofinance/lido-python-sdk/pull/29))

## [1.0.1](https://github.com/lidofinance/lido-python-sdk) - 2021-08-31
### Added
- Lido public class ([#0020](https://github.com/lidofinance/lido-python-sdk/pull/20))
- Added fast BLS verification ([#0019](https://github.com/lidofinance/lido-python-sdk/pull/19))

### Changed
- If strict is false, for validation we will try possible WC only for already used keys ([#0024](https://github.com/lidofinance/lido-python-sdk/pull/24))

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
