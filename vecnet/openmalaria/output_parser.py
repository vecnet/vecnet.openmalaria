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

import StringIO
from .input import XmlInputFile


class OutputParser:
    def __init__(self, input_file,
                 survey_output_file=None,
                 cts_output_file=None):
        if isinstance(input_file, (str, unicode)):
            input_file = StringIO.StringIO(input_file)
        self.xml = input_file.read()
        self.xml_input_file = XmlInputFile(self.xml)

        # Survey timesteps from input file are required to parse Survey output
        self.survey_time_list = self.xml_input_file.survey_timesteps

        # Parse continuous output file
        self._parse_continuous_output_file(cts_output_file)

        # Parse survey output file
        self._parse_survey_output_file(survey_output_file)

    def _parse_continuous_output_file(self, cts_output_file):
        # File format documented on
        # https://code.google.com/p/openmalaria/wiki/OutputFiles
        # Example:
        # ##	##
        #  timestep	simulated EIR	GVI coverage
        #  0	0.476359	0
        #  1	0.425191	0
        #  2	0.430878	0
        #  3	0.434576	0
        #  4	0.436511	0
        #  5	0.434047	0
        #  ...
        if cts_output_file is not None:
            if isinstance(cts_output_file, (str, unicode)):
                cts_output_file = StringIO.StringIO(cts_output_file)
            # skip first line in cts output file
            # (##  ##)
            cts_output_file.readline()
            # read and parse header
            # timestep <tab> simulated EIR <tab> GVI coverage
            header = cts_output_file.readline().strip("\r\n")
            measures = header.split("\t")
            # Sanity check
            if measures[0] != "timestep":
                raise TypeError("Invalid ctsoutput file, first column is not timestep")

            # Parse data in continuous output
            cts_output_data = {measure: [] for measure in measures}

            for line in cts_output_file:  # readline()
                data = line.split("\t")
                for i in range(0, len(measures)):
                    cts_output_data[measures[i]].append(float(data[i]))
            # Can also check if timesteps are in order
            cts_output_data.pop("timestep")
            self.cts_output_data = cts_output_data

    def _parse_survey_output_file(self, survey_output_file):
        # File format documented on
        # https://code.google.com/p/openmalaria/wiki/OutputFiles
        #
        # survey number <tab> third dimension <tab> measure <tab> value
        #
        # Example:
        # 1	1	0	1000
        #  1	1	3	382
        #  1	1	14	13816
        #  1	1	56	0
        #  1	0	36	0.348776
        #  2	1	0	1000
        #  2	1	3	371
        #  2	1	14	103
        #  2	1	56	585
        #  2	0	36	0.170824
        #  ...
        if survey_output_file is not None:
            if isinstance(survey_output_file, (str, unicode)):
                survey_output_file = StringIO.StringIO(survey_output_file)
            survey_output_data = dict()
            for line in survey_output_file:
                # Split string line into four numbers
                line = line.strip("\r\n")
                data = line.split("\t")
                # Check if we have exactly 4 columns
                assert len(data) == 4
                # The survey number starts from one and corresponds to the survey time point.
                # (Exception: measure 21
                # has one record from the end of the simulation and does not use the survey number or third dimension
                # columns.)
                survey_number = int(data[0])
                # Output can be associated with several different measures; the code under the label "id" in the first
                # column of the survey measures table appears in the third column of output.
                measure_id = int(data[2])
                # The "third dimension" (in the second column for historical reasons) specifies another dimension of the
                # output. For many measures it identifies the human age group, for a few measures it is unused, and
                # for some it holds a mosquito species, a drug identifier or a cohort number.
                try:
                    third_dimension = int(data[1])
                except ValueError as e:
                    # For vector measures (Vector_Nv0, Vector_Nv, Vector_Ov and Vector_Sv) third dimension is
                    # a species' name, not a number
                    if self.xml_input_file.measure_has_species_name(measure_id=measure_id):
                        third_dimension = str(data[1])
                    else:
                        # If not a vector measure, pass re-raise the exception
                        raise e
                # Value of measure for specified survey number (can be translated to timestep number)
                value = float(data[3])
                if (measure_id, third_dimension) in survey_output_data:
                    survey_output_data[(measure_id, third_dimension)].append(
                        [self.survey_time_list[survey_number - 1], value])
                else:
                    survey_output_data[(measure_id, third_dimension)] = \
                        [[self.survey_time_list[survey_number - 1], value]]
            self.survey_output_data = survey_output_data
            return survey_output_data

    def get_cts_measures(self):
        return self.cts_output_data.keys()

    def get_survey_measures(self):
        return self.survey_output_data.keys()

    def get_monitoring_age_group(self, third_dimension):
        return self.xml_input_file.monitoring_age_groups[third_dimension]

    def get_survey_measure_name(self, measure_id, third_dimension):
        measure_name = ""
        if surveyFileMap[measure_id][1] == "age group":
            age_group = self.get_monitoring_age_group(third_dimension - 1)
            age_group_name = "%s - %s" % (age_group["lowerbound"], age_group["upperbound"])
            measure_name = "(%s)" % age_group_name
        elif surveyFileMap[measure_id][1] == "vector species":
            measure_name = "(%s)" % third_dimension
        measure_name = surveyFileMap[measure_id][0] + measure_name
        return measure_name


continuousFileMap = \
    [
        ("N_v0", "30 - 32",
         "The number of mosquitoes that emerge and survive to first host seeking, per day (mosquito emergence rate)"),
        ("N_v", "30 - 32", "The total number of host seeking mosquitoes"),
        ("O_v", "30 - 32", "The number of infected host seeking mosquitoes"),
        ("S_v", "30 - 32", "The number of infectious host seeking mosquitoes"),
        ("P_A", "30 - 32", "The probability that a mosquito doesn't find a host and doesn't die on given night"),
        ("P_df", "30 - 32",
         "The probablity that a mosquito finds a host on a given night, feeds and survives "
         "to return to the host-seeking population"),
        ("P_dif", "30 - 32",
         "The probability that a mosquito finds a host on a given night, feeds, gets infected with P. falciparum "
         "and survives to return to the host-seeking population"),
        ("alpha", "30.1 - 32",
         "The availability rate of humans to mosquitoes (averaged across human population); "
         "units: humans/day (I think)"),
        ("P_B", "30.1 - 32",
         "The probability of a mosquito successfully biting a human after choosing, averaged across humans"),
        ("P_C*P_D", "30.1 - 32",
         "The probability of a mosquito successfully escaping a human and resting after biting, "
         "averaged across humans"),
        ("input EIR", "30 - 32",
         "Requested entomological infection rate. This is a fixed periodic value, for comparison with simulated EIR. "
         "Units (from schema version 24): inoculations per adult per timestep."),
        ("simulated EIR", "30 - 32",
         "EIR acting on simulated humans. Units: from schema version 26, inoculations per adult per timestep, "
         "previously inoculations per person per timestep."),
        ("hosts", "30 - 32", "Total number of human hosts (fixed)"),
        ("host demography", "30 - 32", "Number of humans less than 1, 5, 10, 15, and 25 years of age respectively"),
        ("recent births", "30 - 32", "Number of new humans since last report"),
        ("patent hosts", "30 - 32", "Number of humans with detectible parasite density"),
        ("human infectiousness", "30 - 32",
         "Infectiousness of humans to mosquitoes, also known as kappa. This is the probability that a mosquito "
         "becomes infected at any single feed on a human."),
        ("human age availability", "30 - 32",
         "Mean age-based availability of humans to mosquitoes relative to a human adult (doesn't include any other "
         "availability factors, such as vector-model rate or intervention protections)."),
        ("immunity h", "30 - 32",
         "Average of _cumulativeh parameter across humans, which is the cumulative number of infections received "
         "since birth"),
        ("immunity Y", "30 - 32",
         "Average (mean) of _cumulativeY parameter across humans, "
         "which is the cumulative parasite density since birth"),
        ("median immunity Y", "30 - 32",
         "Average (median) of _cumulativeY parameter across humans, "
         "which is the cumulative parasite density since birth"),
        ("new infections", "30 - 32",
         "Number of new infections since last report, including super infections as with survey measure 43."),
        ("num transmitting humans", "30 - 32",
         "Number of humans who are infectious to mosquitoes"),
        ("nets owned", "30 - 31",
         "Number of people owning a bed net. Note that people cannot own more than one of a single type of net, "
         "so this is usually also the number of nets owned. For version 32, use ITN coverage instead."),
        ("ITN coverage", "32",
         "The number of people owning any type of net divided by the population size. This does not count nets "
         "parameterised with the 'GVI' model, only those using the 'ITN' model."),
        ("IRS coverage", "32",
         "The number of people currently protected by any type of IRS divided by the population size. "
         "It does not count IRS configured with the 'GVI' model."),
        ("GVI coverage", "32",
         "The number of people currently protected by any GVI (generic vector intervention) divided by the population "
         "size. Note that even if 'GVI' is used to model two very different interventions (e.g. deterrents and nets), "
         "this is the coverage by 'at least one of' these interventions, not separate coverage levels. This includes "
         "nets, IRS and other interventions modelled using the 'GVI' intervention model but not those using the "
         "separate 'ITN' or 'IRS' models."),
        ("mean hole index", "30 - 31",
         "Average hole-index of all nets (will be not-a-number when no nets are owned)"),
        ("mean insecticide content", "30 - 31",
         "Average insecticide content of all nets in mg/m^2 (will be not-a-number when no nets are owned)"),
        ("IRS insecticide content", "30.1 - 31",
         "Average insecticide content of hut walls over all houses (new IRS model version 2 only); added in schema 30"),
        ("IRS effects", "30.1 - 31",
         "Average effect of IRS on the following three factors: availablity to mosquitoes, preprandial killing, "
         "postprandial killing; mean across all humans; both IRS models version 1 and 2; added in schema 30"),
        ("resource availability", "30.3 - 32",
         "Mean larval resources over a time-step (1/y for these models)"),
        ("requirements availability", "30.3 - 32",
         "Only for an as-yet unavailable mosquito population dynamics model")
    ]

# ## This is a map of the survey output measures
# Please refer to https://code.google.com/p/openmalaria/wiki/XmlMonitoring for additional details
surveyFileMap = \
    [
        ("nHost", "age group", "Total number of humans.Note: when using the IPTI_SP_MODEL option"),
        ("nInfect", "age group", "number of infected hosts"),
        ("nExpectd", "age group", "expected number of infected hosts"),
        ("nPatent", "age group", "number of patent hosts"),
        ("sumLogPyrogenThres", "age group", "Sum of the log of the pyrogen threshold"),
        ("sumlogDens", "age group", "Sum of the logarithm of the parasite density"),
        ("totalInfs", "age group", "Total infections"),
        ("nTransmit", "(unused)",
         "Infectiousness of human population to mosquitoes: sum(p(transmit_i)) across humans i"),
        ("totalPatentInf", "age group", "Total patent infections"),
        # Measure 9 name is taken from https://code.google.com/p/openmalaria/source/browse/util/plotResult.py
        ("contrib", "(removed)", "(removed)"),
        ("sumPyrogenThresh", "age group", "Sum of the pyrogenic threshold"),
        ("nTreatments1", "age group", "number of treatments (1st line) (added to 1-day model in 24.1)"),
        ("nTreatments2", "age group", "number of treatments (2nd line) (added to 1-day model in 24.1)"),
        ("nTreatments3", "age group", "number of treatments (inpatient) (added to 1-day model in 24.1)"),
        ("nUncomp", "age group", "number of episodes (uncomplicated)"),
        ("nSevere", "age group", "number of episodes (severe)"),
        ("nSeq", "age group", "recovered cases with sequelae"),
        ("nHospitalDeaths", "age group", "deaths in hospital"),
        ("nIndDeaths", "age group", "number of deaths (indirect)"),
        ("nDirDeaths", "age group", "number of deaths (direct)"),
        ("nEPIVaccinations", "age group", "number of EPI vaccine doses given"),
        ("allCauseIMR", "(unused)",
         "all cause infant mortality rate (returned as a single number over whole intervention period"),
        ("nMassVaccinations", "age group", "number of Mass / Campaign vaccine doses given"),
        ("nHospitalRecovs", "age group", "recoveries in hospital without sequelae"),
        ("nHospitalSeqs", "age group", "recoveries in hospital with sequelae"),
        ("nIPTDoses", "age group", "number of IPT Doses"),
        ("annAvgK", "(unused)",
         "Annual Average Kappa. Calculated once a year as sum of human infectiousness weighted by initial EIR for "
         "that time of year."),
        ("nNMFever", "age group", "Number of episodes of non-malaria fever"),
        # Measure 28 name is taken from https://code.google.com/p/openmalaria/source/browse/util/plotResult.py
        ('innoculationsPerDayOfYear',"(removed)","(removed"),
        # Measure 29 name is taken from https://code.google.com/p/openmalaria/source/browse/util/plotResult.py
        ('kappaPerDayOfYear',"(removed)","(removed"),
        ("innoculationsPerAgeGroup", "age group", "The total number of inoculations per age group"),
        ("Vector_Nv0", "vector species",
         "Number of emerging mosquitoes that survive to the first feeding search per day at this time-step "
         "(mosquito emergence rate)."),
        ("Vector_Nv", "vector species", "Host seeking mosquito population size at this time step."),
        ("Vector_Ov", "vector species", "Number of infected host seeking mosquitoes at this time step."),
        ("Vector_Sv", "vector species", "Number of infectious host seeking mosquitoes at this time step."),
        ("inputEIR", "(unused)",
         "(Previously Vector_EIR_Input.) Input EIR (rate entered into scenario file for vector/non-vector model). "
         "Units (schema 24 and later): average inoculations per adult over the time period since the last survey "
         "measured in infectious bites per person per time step."),
        ("simulatedEIR", "(unused)",
         "(Previously Vector_EIR_Simulated.) EIR generated by transmission model as measured by inoculations recieved "
         "by adults. Units as above (output 35)."),
        None,
        None,
        ("Clinical_RDTs", "(unused)", "Number of Rapid Diagnostic Tests used"),
        ("Clinical_DrugUsage", "drug ID", "Quantities of oral drugs used"),
        ("Clinical_FirstDayDeaths", "age group", "Direct death before treatment takes effect"),
        ("Clinical_HospitalFirstDayDeaths", "age group", "Direct death before treatment takes effect; hospital only"),
        ("nNewInfections", "age group", "The number of infections introduced since the last survey"),
        ("nMassITNs", "age group", "The number of ITNs delivered by mass distribution since last survey."),
        ("nEPI_ITNs", "age group", "The number of ITNs delivered through EPI since last survey."),
        ("nMassIRS", "age group", "The number of people newly protected by IRS since last survey."),
        ("nMassVA", "age group",
         "The number of people newly protected by a vector-availability intervention since the last survey."),
        ("Clinical_Microscopy", "(unused)", "Number of microscopy tests used"),
        ("Clinical_DrugUsageIV", "drug ID", "Quantities of intravenous drugs used"),
        ("nAddedToCohort", "age group", "Number of individuals added to cohort"),
        ("nRemovedFromCohort", "age group", "Number of individuals removed from cohort"),
        ("nMDAs", "age group",
         "Number of drug doses given via mass deployment (MDA or screen&treat) (where configured as screen&treat"),
        ("nNmfDeaths", "age group", "Direct deaths due to non-malaria fevers"),
        ("nAntibioticTreatments", "age group", "Report number of antibiotic treatments administered"),
        ("nMassScreenings", "age group", "Report number screens in MSAT"),
        ("nMassGVI", "age group", "Report the number of mass deployments of generic vector interventions"),
        ("nCtsIRS", "age group", "Report the number of IRS deployments via age-based deployment"),
        ("nCtsGVI", "age group", "Report the number of GVI deployments via age-based deployment"),
        ("nCtsMDA", "age group", "Report the number of MDA deployments via age-based deployment"),
        ("nCtsScreenings", "age group",
         "Report the number of screenings used by MDA/MSAT when deployed via age-based deployment"),
        ("nSubPopRemovalTooOld", "age group",
         "Number of removals from a sub-population due to expiry of duration of membership "
         "(e.g. intervention too old)."),
        ("nSubPopRemovalFirstEvent", "age group",
         "Number of removals from a sub-population due to first infection/bout/treatment (see onFirstBout & co)."),
        ("nPQTreatments", "age group", "Number of treatments given with primaquine (P. vivax model only)."),
        ("nTreatDiagnostics", "age group",
         "Number of diagnostic tests performed (if in the health system description, useDiagnosticUC='true').")

    # https://code.google.com/p/openmalaria/source/browse/util/plotResult.py
    # 65 : 'nMassRecruitOnly',
    # 66 : 'nCtsRecruitOnly',
    # 67 : 'nTreatDeployments',
    # 68 : 'sumAge',
    # 69 : 'nInfectByGenotype',
    # 70 : 'nPatentByGenotype',
    # 71 : 'logDensByGenotype',
    # 72 : 'nHostDrugConcNonZero',
    # 73 : 'sumLogDrugConcNonZero'
    ]