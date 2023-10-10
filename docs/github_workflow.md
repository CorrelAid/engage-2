# GitHub workflow guidelines

The intended GitHub workflow works with a `development` branch (the default
branch), a production branch and feature branches. New features, bug fixes,
configuration changes etc, should be developed in a dedicated feature branch
and then merged with `development` via a PR. Occasionally updates from the
`development` branch will be merged into the production branch.

Merging a PR generally requires that CI passes and that there is on approving
review from a different developer.

The Core developers who are admins for the repository have the ability to
overwrite the PR merge requirements. Ideally this should never be used to
overwrite failing CI. On the other hand overwriting the review requirement can
help to facilitate quicker development of the project. Below we collect some
guidelines for cases when such an overwrite seems generally justified and for
cases when it should be avoided as much as possible.

## Example Cases for Admin Merge overwrite

In the following cases, when the PR only contains the listed content it is
always acceptable to use admin overwrite to merge a PR. It might still be
acceptable in other cases based on individual judgement.

- Documentation only
- Hotfix
- Technical changes with a high amount of test coverage
- Features with no end user access. There can be several applicable situation.
  - Backend features that are not mapped to the frontend (yet)
  - Features that can only be accessed by special privileges. Such that uses
    who have access are likely aware of the experimental status.
  - Configuration changes not related prod
  - Prod configuration changes that are identical to already tested
    dev configuration changes.
- Improvements on CI as long as no major work overhead for other devs is expected.

## Examples of Features that should definitely be reviewed if at all possible

- Highly interconnected features
- Features with large expected user impact
- Features that are hard to test
