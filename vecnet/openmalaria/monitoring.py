# -*- coding: utf-8 -*-
#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Helper functions for OpenMalaria Monitoring Section.
"""
from xml.etree.ElementTree import ParseError
from vecnet.openmalaria.scenario.monitoring import Monitoring


TIMESTEPS_PER_YEAR = 73


def get_survey_times(monitoring, start_date):
    monitor_type = "yearly"
    monitor_yrs = 0
    monitor_mos = 0
    monitor_start_date = 0

    times = monitoring.surveys
    for time_interval in times:
        if time_interval % TIMESTEPS_PER_YEAR != 0:
            if (time_interval-6) % TIMESTEPS_PER_YEAR == 0 or (time_interval-11) % TIMESTEPS_PER_YEAR == 0 or (time_interval-18) % TIMESTEPS_PER_YEAR == 0 or \
                (time_interval-24) % TIMESTEPS_PER_YEAR == 0 or (time_interval-30) % TIMESTEPS_PER_YEAR == 0 or (time_interval-36) % TIMESTEPS_PER_YEAR == 0 or \
                (time_interval-42) % TIMESTEPS_PER_YEAR == 0 or (time_interval-48) % TIMESTEPS_PER_YEAR == 0 or (time_interval-54) % TIMESTEPS_PER_YEAR == 0 or \
                (time_interval-60) % TIMESTEPS_PER_YEAR == 0 or (time_interval-66) % TIMESTEPS_PER_YEAR == 0:
                monitor_type = "monthly"
            else:
                monitor_type = "custom"

    if len(times) > 0:
        if monitor_type == "yearly":
            monitor_yrs = (times[-1] / TIMESTEPS_PER_YEAR) - (times[0] / TIMESTEPS_PER_YEAR)
            monitor_start_date = start_date + (times[0] / TIMESTEPS_PER_YEAR)
        elif monitor_type == 'monthly':
            mos_index = 0

            for i in range(len(times)-1, -1, -1):
                if times[i] % TIMESTEPS_PER_YEAR == 0:
                    monitor_yrs = (times[i] / TIMESTEPS_PER_YEAR) - (times[0] / TIMESTEPS_PER_YEAR)
                    mos_index = i
                    break

            for i in range(mos_index, len(times) - 1):
                monitor_mos += 1

            monitor_start_date = start_date + (times[0] / TIMESTEPS_PER_YEAR)

    monitor_info = {
        "type": monitor_type,
        "start_date": monitor_start_date,
        "yrs": monitor_yrs,
        "mos": monitor_mos,
        "timesteps": times[-1]
    }

    return monitor_info


def set_survey_times(sim_start_date, monitor_yrs, monitor_mos, monitor_start_date, output_measurement):
    surveys_list = []
    years_before_monitor_start = monitor_start_date - sim_start_date

    if output_measurement == "yearly":
        for yr in range(years_before_monitor_start, years_before_monitor_start + monitor_yrs + 1):
            surveys_list.append(str(TIMESTEPS_PER_YEAR * yr))
    elif output_measurement == "monthly":
        total_months = ((years_before_monitor_start + monitor_yrs) * 12) + monitor_mos
        months_before_monitor_start = years_before_monitor_start * 12

        new_timestep = 0
        month_count = 0
        for month in range(months_before_monitor_start, total_months + 1):
            timesteps_to_add_for_month = 0

            if month_count % 12 == 0:  # Begin next year.
                new_timestep = TIMESTEPS_PER_YEAR * (month / 12)
                month_count = 0
            elif month_count == 2:
                timesteps_to_add_for_month = 5
            elif month_count == 3:
                timesteps_to_add_for_month = 7
            else:
                timesteps_to_add_for_month = 6

            new_timestep += timesteps_to_add_for_month
            month_count += 1

            surveys_list.append(str(new_timestep))

    return surveys_list
