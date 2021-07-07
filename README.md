# Verboscript
A Plain English Programming Language.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![GitHub](https://img.shields.io/github/license/Skiylia-Lang/Verboscript)
[![CodeFactor](https://www.codefactor.io/repository/github/skiylia-lang/Verboscript/badge)](https://www.codefactor.io/repository/github/skiylia-lang/Verboscript)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/Skiylia-Lang/Verboscript)
[![codecov](https://codecov.io/gh/Skiylia-Lang/Verboscript/branch/main/graph/badge.svg?token=DRJ67ZQA7M)](https://codecov.io/gh/Skiylia-Lang/Verboscript)
[![time tracker](https://wakatime.com/badge/github/Skiylia-Lang/Verboscript.svg)](https://wakatime.com/badge/github/Skiylia-Lang/Verboscript)

![GitHub language count](https://img.shields.io/github/languages/count/Skiylia-Lang/Verboscript)
![GitHub top language](https://img.shields.io/github/languages/top/Skiylia-Lang/Verboscript)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Skiylia-Lang/Verboscript)
![Lines of code](https://img.shields.io/tokei/lines/github.com/Skiylia-Lang/Verboscript) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Releases

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Skiylia-Lang/Verboscript?include_prereleases)
![GitHub commits since latest release (by date including pre-releases)](https://img.shields.io/github/commits-since/Skiylia-Lang/Verboscript/latest/develop?include_prereleases)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Skiylia-Lang/Verboscript)
![GitHub milestone](https://img.shields.io/github/milestones/progress/Skiylia-Lang/Verboscript/1)
![GitHub milestones](https://img.shields.io/github/milestones/open/Skiylia-Lang/Verboscript)
![GitHub issues](https://img.shields.io/github/issues-raw/Skiylia-Lang/Verboscript)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/Skiylia-Lang/Verboscript)
![GitHub last commit](https://img.shields.io/github/last-commit/Skiylia-Lang/Verboscript)

**Verboscript: [Latest release](../../releases)**

Open issues can be found here: [issues](../../issues)

To create an issue, be it a bug, question, feature request, or other, use this link here: [Open an issue](../../issues/new/choose)

# Verboscript

## Verbose, Verbose, Verbose

The entire concept for this language is plain english representation. Anyone, irrespective of programming experience, should be able to read and understand exactly what is happening. For an example of how this can be useful, consider the following:

This example in C:
```c
#include <stdio.h>
for(int x = 0; x < 5; x++)
{
    printf(x)
}
```

is equivalent to this example in Python:
```python
for x in range(0, 5):
    print(x)
```

Which could potentially be this, in Verboscript:
```
start a counter at zero, then repeat the following five times:
    show the counter
```

Each layer of abstraction becomes easier to understand in plain english, at the cost of requiring a more complicated program to execute it. Verboscript aims to be completely transparent to anyone, without requiring prior experince with programming languages.

The main directory housing the Verboscript software is [here](../../tree/main/Verboscript).

## Contributing

Any contributions made are absolutely welcome.

Checkout the issues area for any outstanding problems, or the discussions tab to discuss ideas and features.

Forking this repository is an excellent way to contribute to the code that makes this project tick. Open a pull request (preferably to the develop branch) if you have anything to add, and it'll be looked over.

## Tools

 - The project was written in [<Host Language>](<Host language Url>) <Host Language Version>, and can be ran on any machine with it installed.
 - [Mergify](https://mergify.io/) has been automatically managing all of the repository branches.
 - [All-contributors](https://allcontributors.org/) has been managing the contributors section.
 - [Snyk](https://snyk.io/) has been monitoring for security concerns.
 - [Release-drafter](https://github.com/release-drafter/release-drafter) has been compiling all pull requests into changelogs on each draft release, massively expediating the process.
 - And while we don't have an dependencies (yet?) [Dependabot](https://dependabot.com/) has been keeping in the shadows.

## Contributors

All the people who have contributed ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/SK1Y101"><img src="https://avatars.githubusercontent.com/u/8695579?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jack Lloyd-Walters</b></sub></a><br /><a href="https://github.com/Skiylia-Lang/Verboscript/commits?author=SK1Y101" title="Code">💻</a> <a href="https://github.com/Skiylia-Lang/Verboscript/pulls?q=is%3Apr+reviewed-by%3ASK1Y101" title="Reviewed Pull Requests">👀</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
