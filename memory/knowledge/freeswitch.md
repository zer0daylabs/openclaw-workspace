# FreeSWITCH — CB Knowledge Summary

Last updated: 2026-03-17
Proficiency: basic
Source: SignalWire Documentation, EventVikings implementation info

## What It Is
FreeSWITCH is an open source communications platform written in C from the ground up. It's a **telephony construction kit** for building everything from softphones to full Class 5 switches. FreeSWITCH is modular ("Don't glue the Lego pieces together"), licensed under MPL.

## Architecture
- **Core:** libfreeswitch (back-to-back user agent/B2BUA)
- **Embedded:** Can be embedded into softphones, OpenWRT routers, or used as standalone PBX
- **Modular:** Optional modules extend functionality without inter-module dependency
- **Platforms:** Linux, Windows, Mac OS X, *BSD, Debian, Ubuntu, CentOS/Fedora/RHEL
- **Version:** Current public release 1.10 (Aug 2019), recommended for production

## Our Use Case
**EventVikings predictive dialer** — We're building a predictive dialer that analyzes call patterns, agent availability, and other factors to predict the optimal time to place calls. FreeSWITCH provides the telephony foundation for this.

## Key Commands / API
- **ESL (Event Socket Library):** Listens on port **8021** by default, password **'ClueCon'**
- **Dialplan:** XML-based dialplan configuration
- **CLI:** `fs_cli` for command-line interface
- **Web API:** REST API for programmatic control

## Configuration
- **Default config directory:** `/etc/freeswitch/`
- **Main config file:** `freeswitch.xml`
- **ESL port:** 8021
- **ESL password:** ClueCon (default)
- **Installation:** See SignalWire docs for build instructions

## Integration Points
- **Predictive dialing algorithms:** Analyze call patterns + agent availability
- **FusionPBX:** Can be built on FusionPBX with own GUI using PostgreSQL DB info for auto dial
- **SIP Protocol:** Core telephony protocol for call setup
- **Hardware interfaces:** Sangoma A100 series for PRI circuits (FreeTDM)

## Gotchas
- **Version checking:** Check Release Notes before upgrading — breaking changes between minor/major releases
- **EOL:** Version 1.8 is End Of Life, must upgrade to 1.10
- **Bugs:** Test in Development release before filing bug reports on GitHub
- **Module dependencies:** Modular architecture means one module doesn't require loading another
- **Predictive dialer implementation:** Usually don't signal events outside the dialer in predictive scenarios

## Resources
- **Documentation:** https://developer.signalwire.com/freeswitch/
- **GitHub:** https://github.com/signalwire/freeswitch
- **Community docs:** https://wiki.freeswitch.org/
- **Installation:** https://developer.signalwire.com/freeswitch/FreeSWITCH-Explained/Installation/
- **Introduction:** https://developer.signalwire.com/freeswitch/FreeSWITCH-Explained/Introduction/

## Current Proficiency Assessment
- **Status:** Research complete (2026-03-17)
- **Gap identified:** Need deeper understanding of predictive dialing algorithm implementation
- **Action:** Study ESL integration for predictive dialer logic, understand call pattern analysis
- **Next steps:** Research predictive dialing algorithm patterns, implement call state monitoring
