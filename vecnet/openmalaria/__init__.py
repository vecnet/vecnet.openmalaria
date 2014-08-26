#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# An attempt to add __version__ field based on a post on stackoverflow
# from pkg_resources import get_distribution, DistributionNotFound
# import os.path
#
# try:
#     _dist = get_distribution('vecnet.openmalaria')
#     i="123"
#     # if not __file__.startswith(os.path.join(_dist.location, 'vecnet.openmalaria')):
#     #     print __file__
#     #     # not installed, but there is another version that *is*
#     #     raise DistributionNotFound
# except DistributionNotFound:
#     __version__ = 'vecnet.openmalaria is not found'
# else:
#     __version__ = _dist.version

from .experiment_creator_v2 import ExperimentDescription