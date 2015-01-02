continuousMeasuresDescription = \
    {
        "N_v0":
            "The number of mosquitoes that emerge and survive to first host seeking, per day (mosquito emergence rate)",
        "N_v":
            "The total number of host seeking mosquitoes",
        "O_v":
            "The number of infected host seeking mosquitoes",
        "S_v":
            "The number of infectious host seeking mosquitoes",
        "P_A":
            "The probability that a mosquito doesn't find a host and doesn't die on given night",
        "P_df":
            "The probablity that a mosquito finds a host on a given night, feeds and survives to return to "
            "the host-seeking population",
        "P_dif":
            "The probability that a mosquito finds a host on a given night, feeds, gets infected with "
            "P. falciparum and survives to return to the host-seeking population",
        "alpha":
            "The availability rate of humans to mosquitoes (averaged across human population); "
            "units: humans/day (probably)",
        "P_B":
            "The probability of a mosquito successfully biting a human after choosing, averaged across humans",
        "P_C*P_D":
            "The probability of a mosquito successfully escaping a human and resting after biting, "
            "averaged across humans",
        "input EIR":
            "Requested entomological infection rate. This is a fixed periodic value, for comparison with simulated EIR."
            "Units (from schema version 24): inoculations per adult per timestep.",
        "simulated EIR":
            "EIR acting on simulated humans. "
            "Units: from schema version 26, inoculations per adult per timestep, "
            "previously inoculations per person per timestep.",
        "hosts":
            "Total number of human hosts (fixed)",
        "host demography":
            "Number of humans less than 1, 5, 10, 15, and 25 years of age respectively",
        "recent births":
            "Number of new humans since last report",
        "patent hosts":
            "Number of humans with detectible parasite density",
        "human infectiousness":
            "Infectiousness of humans to mosquitoes, also known as kappa. "
            "This is the probability that a mosquito becomes infected at any single feed on a human.",
        "human age availability":
            "Mean age-based availability of humans to mosquitoes relative to a human adult "
            "(doesn't include any other availability factors, such as vector-model rate or intervention protections).",
        "immunity h":
            "Average of _cumulativeh parameter across humans, which is the cumulative number of "
            "infections received since birth",
        "immunity Y":
            "Average (mean) of _cumulativeY parameter across humans, "
            "which is the cumulative parasite density since birth",
        "median immunity Y":
            "Average (median) of _cumulativeY parameter across humans, "
            "which is the cumulative parasite density since birth",
        "new infections":
            "Number of new infections since last report, including super infections as with survey measure 43.",
        "num transmitting humans": "Number of humans who are infectious to mosquitoes",
        "nets owned":
            "Number of people owning a bed net. Note that people cannot own more than one of a single "
            "type of net, so this is usually also the number of nets owned. "
            "For version 32, use ITN coverage instead.",
        "ITN coverage":
            "The number of people owning any type of net divided by the population size. This does not count nets "
            "parameterised with the 'GVI' model, only those using the 'ITN' model.",
        "IRS coverage":
            "The number of people currently protected by any type of IRS divided by the population size. "
            "It does not count IRS configured with the 'GVI' model.",
        "GVI coverage":
            "The number of people currently protected by any GVI (generic vector intervention) "
            "divided by the population size. Note that even if 'GVI' is used to model two very different interventions "
            "(e.g. deterrents and nets), this is the coverage by 'at least one of' these interventions, not separate "
            "coverage levels. This includes nets, IRS and other interventions modelled using the "
            "'GVI' intervention model but not those using the separate 'ITN' or 'IRS' models.",
        "mean hole index":
            "Average hole-index of all nets (will be not-a-number when no nets are owned)",
        "mean insecticide content":
            "Average insecticide content of all nets in mg/m^2 (will be not-a-number when no nets are owned)",
        "IRS insecticide content":
            "Average insecticide content of hut walls over all houses (new IRS model version 2 only); "
            "added in schema 30",
        "IRS effects":
            "Average effect of IRS on the following three factors: availablity to mosquitoes, preprandial killing, "
            "postprandial killing; mean across all humans; both IRS models version 1 and 2; added in schema 30",
        "resource availability":
            "Mean larval resources over a time-step (1/y for these models)",
        "requirements availability":
            "Only for an as-yet unavailable mosquito population dynamics model",
    }