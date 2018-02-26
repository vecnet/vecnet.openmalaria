#!/bin/env python2
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
from xml.etree.ElementTree import Element
from xml.etree import ElementTree
import six

from vecnet.openmalaria.scenario.core import Section, attribute, attribute_setter, section, tag_value, tag_value_setter
from vecnet.openmalaria.scenario.healthsystem import HealthSystem


class Deploy(Section):
    @property
    @attribute
    def maxAge(self):
        return "maxAge", float

    @property
    @attribute
    def minAge(self):
        return "minAge", float

    @property
    @attribute
    def p(self):
        return "p", float

    @property
    def components(self):
        component_ids = []

        for component in self.et.findall("component"):
            component_ids.append(component.attrib["id"])

        return component_ids


class Deployment(Section):
    """ /scenario/intervention/human/deployment (multiple)
    """
    def create_from_xml(self, xml):
        et = ElementTree.fromstring(xml)
        self.et = et

    @property
    @attribute
    def name(self):
        return "name", str

    @property
    def components(self):
        component_ids = []

        for component in self.et.findall("component"):
            component_ids.append(component.attrib["id"])

        return component_ids
    @components.setter
    def components(self, value):
        if value is None or len(value) == 0:
            return

        for component in self.et.findall("component"):
            self.et.remove(component)

        for index, component_id in enumerate(value):
            component = Element("component")
            component.attrib["id"] = component_id
            self.et.insert(index, component)

    @property
    def timesteps(self):
        deployments = []
        for deploy in self.et.find("timed").findall("deploy"):
            deployments.append(
                {"time":    int(deploy.attrib["time"]),
                 "coverage": float(deploy.attrib["coverage"])}
            )
        return deployments
    @timesteps.setter
    def timesteps(self, value):
        timed = self.et.find("timed")

        if timed is not None:
            for deploy in timed.findall("deploy"):
                timed.remove(deploy)
        else:
            timed = Element("timed")
            self.et.append(timed)
            timed = self.et.find("timed")

        for deploy in value:
            deploy_element = Element("deploy")
            deploy_element.attrib["time"] = deploy["time"]
            deploy_element.attrib["coverage"] = deploy["coverage"]
            timed.append(deploy_element)

    @property
    def continuous(self):
        deployments = []
        if self.et.find("continuous") is None:
            return None
        for deploy in self.et.find("continuous").findall("deploy"):
            deployments.append(
                    {"targetAgeYrs": float(deploy.attrib["targetAgeYrs"]),
                     "begin": int(deploy.attrib["begin"]) if 'begin' in deploy else 0,
                     "end": int(deploy.attrib["end"] if 'end' in deploy else 2147483647)
                    }
            )
        return deployments
    @continuous.setter
    def continuous(self, value):
        continuous = self.et.find("continuous")

        if continuous is not None:
            for deploy in continuous:
                continuous.remove(deploy)
        else:
            continuous = Element("continuous")
            index = len(self.et.findall("component"))
            self.et.insert(index, continuous)
            continuous = self.et.find("continuous")

        for deploy in value:
            deploy_element = Element("deploy")
            deploy_element.attrib["targetAgeYrs"] = deploy["targetAgeYrs"]
            if "begin" in deploy:
                deploy_element.attrib["begin"] = deploy["begin"]
            if "end" in deploy:
                deploy_element.attrib["end"] = deploy["end"]

            continuous.append(deploy_element)

    def delete_component(self, id):
        for component in self.et.findall("component"):
            if component.attrib["id"] == id:
                self.et.remove(component)

        return len(self.components)


class Deployments(Section):
    """
    Deployments defined in /scenario/interventions/human section
    """
    @property
    def deployments(self):
        if self.et is None or self.et.find("deployment") is None:
            return []

        deployments = []
        for deployment in self.et.findall("deployment"):
            deployments.append(Deployment(deployment))

        return deployments

    def __iter__(self):
        for deployment in self.deployments:
            yield deployment

    def __getitem__(self, index):
        return self.deployments[index]

    def __len__(self):
        return len(self.deployments)


class Interventions(Section):
    """
    Inverventions section in OpenMalaria xml input file
    https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#preventative-interventions
    """
    @property  # changeHS
    def changeHS(self):
        """
        Change health system interventions
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#change-health-system
        Returns: list of HealthSystems together with timestep when they are applied
        """
        health_systems = []
        change_hs = self.et.find("changeHS")
        if change_hs is None:
            return health_systems
        for health_system in change_hs.findall("timedDeployment"):
            health_systems.append([int(health_system.attrib("time")), HealthSystem(self.et)])
        return health_systems

    @property  # changeEIR
    def changeEIR(self):
        change_eir = self.et.find("changeEIR")
        if change_eir is None:
            return None
        eir_daily = []
        for value in change_eir.findall("EIRDaily"):
            eir_daily.append(float(value.text))
        return eir_daily

    @property  # human
    def human(self):
        return HumanInterventions(self.et.find("human"))

    @property  # vectorPop
    def vectorPop(self):
        """
        rtype: VectorPop
        """
        return VectorPop(self.et.find("vectorPop"))

    @property
    def importedInfections(self):
        imported_infections_element = self.et.find("importedInfections")

        if imported_infections_element is None:
            return None

        return ImportedInfections(imported_infections_element)

    def __getattr__(self, item):
        raise KeyError

    def add_section(self, name):
        elem = Element(name)
        self.et.append(elem)

    def remove_section(self, name):
        element = self.et.find(name)

        if element is not None:
            self.et.remove(element)


class Component(Section):
    @property  # name
    @attribute
    def name(self):
        """
        An informal name/description of the intervention

        :rtype: str
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#name-of-component
        """
        return "name", str
    @name.setter
    @attribute_setter(attrib_type=str)
    def name(self, value):
        pass   # value of name attribute will be set by attribute_setter decorator


class AnophelesParams(Section):
    """
    Parameters of mosquitos affected by this ITN intervention

    https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#anophelesparams
    """
    @property
    @attribute
    def mosquito(self):
        """
        Name of the affected anopheles-mosquito species.

        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#anophelesparams
        """
        return "mosquito", str
    @mosquito.setter
    @attribute_setter(attrib_type=str)
    def mosquito(self, value):
        pass

    @property
    @attribute
    def propActive(self):
        """
        Proportion of bites for which net acts

        The proportion of bites, when nets are in use, for which the net has any action whatsoever on the mosquito.
        At the moment this is constant across humans and deterministic: relative attractiveness and survival factors
        are base(1-usagepropActing) + intervention_factorusagepropActing.
        See also "usage" (proportion of time nets are used by humans).

        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#proportion-of-bites-for-which-net-acts
        """
        return "propActive", float
    @propActive.setter
    @attribute_setter(attrib_type=float)
    def propActive(self, value):
        pass

    @property
    @tag_value
    def deterrency(self):
        return "deterrency", "value", float
    @deterrency.setter
    @tag_value_setter(tag="deterrency", attrib="value")
    def deterrency(self, value):
        pass

    @property
    @tag_value
    def preprandialKillingEffect(self):
        return "preprandialKillingEffect", "value", float
    @preprandialKillingEffect.setter
    @tag_value_setter(tag="preprandialKillingEffect", attrib="value")
    def preprandialKillingEffect(self, value):
        pass

    @property
    @tag_value
    def postprandialKillingEffect(self):
        return "postprandialKillingEffect", "value", float
    @postprandialKillingEffect.setter
    @tag_value_setter(tag="postprandialKillingEffect", attrib="value")
    def postprandialKillingEffect(self, value):
        pass


class ITN(Component):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)
        self.itn = et.find("ITN")
        self.id = self.et.attrib["id"]

    @property  # usage
    def usage(self):
        """
        Proportion of time nets are used by humans

        At the moment this is constant across humans and deterministic: relative attractiveness and survival factors
        are base(1-usagepropActing) + intervention_factorusagepropActing.
        See also "propActing" (proportion of bits for which net acts).

        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#proportion-of-time-nets-are-used-by-humans
        :rtype: float
        """
        return float(self.itn.find("usage").attrib["value"])
    @usage.setter
    def usage(self, value):
        assert isinstance(value, float)
        self.itn.find("usage").attrib["value"] = value

    @property
    # Same approach as with scenario.entomology.vectors may work here too
    def anophelesParams(self):
        """
        :rtype: AnophelesParams
        """
        list_of_anopheles = []
        for anophelesParams in self.itn.findall("anophelesParams"):
            list_of_anopheles.append(AnophelesParams(anophelesParams))
        return list_of_anopheles
    @anophelesParams.setter
    def anophelesParams(self, anopheles_params):
        for a_param in self.itn.findall("anophelesParams"):
            self.itn.remove(a_param) 

        for a_param in anopheles_params:
            assert isinstance(a_param, six.string_types)
            et = ElementTree.fromstring(a_param)
            anopheles = AnophelesParams(et)
            assert isinstance(anopheles.mosquito, six.string_types)
            assert isinstance(anopheles.propActive, float)
            assert isinstance(anopheles.deterrency, float)
            assert isinstance(anopheles.preprandialKillingEffect, float)
            assert isinstance(anopheles.postprandialKillingEffect, float)
            self.itn.append(et)

    def get_attrition_in_years(self):
        """
        Function for the Basic UI
        """
        attrition_of_nets = self.itn.find("attritionOfNets")
        function = attrition_of_nets.attrib["function"]
        if function != "step":
            return None
        L = attrition_of_nets.attrib["L"]
        return L

    def set_attrition_in_years(self, years):
        attrition_of_nets = self.itn.find("attritionOfNets")
        attrition_of_nets.attrib["function"] = "step"
        attrition_of_nets.attrib["L"] = years


class Decay(Section):
    """
    Description of decay of all intervention effects. Documentation:
    see DecayFunction type or http://code.google.com/p/openmalaria/wiki/ModelDecayFunctions

    https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#decay-n4
    """
    @property
    @attribute
    def function(self):
        return "function", str
    @function.setter
    @attribute_setter(attrib_type=str)
    def function(self, value):
        pass

    @property
    @attribute
    def L(self):
        return "L", float
    @L.setter
    @attribute_setter(attrib_type=float)
    def L(self, value):
        pass

    @property
    @attribute
    def k(self):
        return "k", float
    @k.setter
    @attribute_setter(attrib_type=float)
    def k(self, value):
        pass

    @property
    @attribute
    def mu(self):
        return "mu", float
    @mu.setter
    @attribute_setter(attrib_type=float)
    def mu(self, value):
        pass

    @property
    @attribute
    def sigma(self):
        return "sigma", float
    @sigma.setter
    @attribute_setter(attrib_type=float)
    def sigma(self, value):
        pass


class GVI(Component):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)
        self.gvi = et.find("GVI")
        self.id = self.et.attrib["id"]

    @property
    def anopheles_xml_snippet(self):
        xml = """<anophelesParams mosquito="gambiae" propActive="0">
                    <deterrency value="0.0" />
                    <preprandialKillingEffect value="0" />
                    <postprandialKillingEffect value="0" />
                  </anophelesParams>"""

        return xml

    def add_or_update_anophelesParams(self, params):
        et = None
        is_update = False

        for a_param in self.gvi.findall("anophelesParams"):
            if a_param.attrib["mosquito"] == params["mosquito"]:
                et = a_param
                is_update = True
                break

        if et is None:
            et = ElementTree.fromstring(self.anopheles_xml_snippet)

        anopheles = AnophelesParams(et)

        anopheles.mosquito = str(params["mosquito"])
        if "propActive" in params and params["propActive"] is not None:
            try:
                anopheles.propActive = float(params["propActive"])
            except ValueError:
                pass
        if "deterrency" in params and params["deterrency"] is not None:
            try:
                anopheles.deterrency = float(params["deterrency"])
            except ValueError:
                pass
        if "preprandialKillingEffect" in params and params["preprandialKillingEffect"] is not None:
            try:
                anopheles.preprandialKillingEffect = float(params["preprandialKillingEffect"])
            except ValueError:
                pass
        if "postprandialKillingEffect" in params and params["postprandialKillingEffect"] is not None:
            try:
                anopheles.postprandialKillingEffect = float(params["postprandialKillingEffect"])
            except ValueError:
                pass

        if not is_update:
            self.gvi.append(anopheles.et)

    def remove_anophelesParams(self, name):
        for a_param in self.gvi.findall("anophelesParams"):
            if a_param.attrib["mosquito"] == name:
                self.gvi.remove(a_param)

        #TODO: Need to flag entire section for removal if empty.

    @property
    def decay(self):
        """
        :rtype: Decay
        """
        return Decay(self.gvi.find("decay"))

    @property
    # Same approach as with scenario.entomology.vectors may work here too
    def anophelesParams(self):
        """
        :rtype: AnophelesParams
        """
        list_of_anopheles = []
        for anophelesParams in self.gvi.findall("anophelesParams"):
            list_of_anopheles.append(AnophelesParams(anophelesParams))
        return list_of_anopheles
    @anophelesParams.setter
    def anophelesParams(self, anopheles_params):
        for a_param in self.gvi.findall("anophelesParams"):
            self.gvi.remove(a_param) 

        for a_param in anopheles_params:
            assert isinstance(a_param, six.string_types)
            et = ElementTree.fromstring(a_param)
            anopheles = AnophelesParams(et)
            assert isinstance(anopheles.mosquito, six.string_types)
            assert isinstance(anopheles.propActive, float)
            assert isinstance(anopheles.deterrency, float)
            assert isinstance(anopheles.preprandialKillingEffect, float)
            assert isinstance(anopheles.postprandialKillingEffect, float)
            self.gvi.append(et)


class MDA(Component):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)
        self.mda = et.find("MDA")
        self.id = self.et.attrib["id"]

    @property
    def treatment_option_xml_snippet(self):
        xml = """<option name="0.5" pSelection="0.5">
                </option>"""

        return xml

    def add_or_update_treatment_option(self, params):
        et = None
        is_update = False

        effects = self.mda.find("effects")

        if effects is None:
            new_effects = Element("effects")
            self.mda.append(new_effects)
            effects = self.mda.find("effects")

        for option in effects.findall("option"):
            if option.attrib["name"] == params["name"]:
                et = option
                is_update = True
                break

        if et is None:
            et = ElementTree.fromstring(self.treatment_option_xml_snippet)

        treatment_option = et

        treatment_option.attrib["name"] = str(params["name"])
        if "pSelection" in params and params["pSelection"] is not None:
            treatment_option.attrib["pSelection"] = params["pSelection"]

        for deploy in treatment_option.findall("deploy"):
            treatment_option.remove(deploy)
        for clear_infection in treatment_option.findall("clearInfections"):
            treatment_option.remove(clear_infection)

        if "deploys" in params and params["deploys"] is not None:
            for deploy in params["deploys"]:
                deploy_element = Element("deploy")
                deploy_element.attrib["maxAge"] = deploy["maxAge"]
                deploy_element.attrib["minAge"] = deploy["minAge"]
                deploy_element.attrib["p"] = deploy["p"]

                for component_id in deploy["components"]:
                    component = Element("component")
                    component.attrib["id"] = component_id
                    deploy_element.append(component)

                treatment_option.append(deploy_element)

        if "clearInfections" in params and params["clearInfections"] is not None:
            for clear_infection in params["clearInfections"]:
                clear_infection_element = Element("clearInfections")
                clear_infection_element.attrib["stage"] = clear_infection["stage"]
                clear_infection_element.attrib["timesteps"] = clear_infection["timesteps"]

                treatment_option.append(clear_infection_element)

        if not is_update:
            effects.append(treatment_option)

    @property
    def treatment_options(self):
        treatment_options = []

        for option in self.mda.find("effects").findall("option"):
            option_info = {
                "name": "",
                "pSelection": float(option.attrib["pSelection"]),
                "deploys": [],
                "clearInfections": []
            }

            if "name" in option.attrib:
                option_info["name"] = option.attrib["name"]

            for deploy_section in option.findall("deploy"):
                option_info["deploys"].append(Deploy(deploy_section))

            for clear_infection in option.findall("clearInfections"):
                clear_infection_info = {
                    "stage": clear_infection.attrib["stage"],
                    "timesteps": int(clear_infection.attrib["timesteps"])
                }
                option_info["clearInfections"].append(clear_infection_info)

            treatment_options.append(option_info)

        return treatment_options


class Vaccine(Component):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)

        self.vaccine_type = "TBV"
        self.vaccine = et.find("TBV")
        if (et.find("PEV") is not None):
            self.vaccine_type = "PEV"
            self.vaccine = et.find("PEV")
        elif (et.find("BSV") is not None):
            self.vaccine_type = "BSV"
            self.vaccine = et.find("BSV")

        self.id = self.et.attrib["id"]

    @property
    def decay(self):
        """
        :rtype: Decay
        """
        return Decay(self.vaccine.find("decay"))

    @property
    def efficacyB(self):
        return float(self.vaccine.find("efficacyB").attrib["value"])
    @efficacyB.setter
    def efficacyB(self, value):
        assert isinstance(value, float)
        self.vaccine.find("efficacyB").attrib["value"] = str(value)

    @property
    def initialEfficacy(self):
        values = []
        for initial_efficacy in self.vaccine.findall("initialEfficacy"):
            values.append(float(initial_efficacy.attrib["value"]))
        return values
    @initialEfficacy.setter
    def initialEfficacy(self, value):
        for initial_efficacy in self.vaccine.findall("initialEfficacy"):
            self.vaccine.remove(initial_efficacy)
        for new_value in value:
            initial_efficacy = Element("initialEfficacy")
            initial_efficacy.attrib["value"] = str(new_value)
            self.vaccine.append(initial_efficacy)


class HumanInterventions(Section):
    """
    List of human interventions
    """
    def add(self, intervention, id=None):
        """
        Add an intervention to intervention/human section.
        intervention is either ElementTree or xml snippet
        """
        if self.et is None:
            return

        assert isinstance(intervention, six.string_types)
        et = ElementTree.fromstring(intervention)
        component = None

        if et.find("ITN") is not None:
            component = ITN(et)
        elif et.find("GVI") is not None:
            component = GVI(et)
        elif et.find("MDA") is not None:
            component = MDA(et)
        elif et.find("TBV") is not None or et.find("PEV") is not None or et.find("BSV") is not None:
            component = Vaccine(et)
        else:
            return

        assert isinstance(component.name, six.string_types)

        if id is not None:
            assert isinstance(id, six.string_types)
            et.attrib["id"] = id

        index = len(self.et.findall("component"))
        self.et.insert(index, et)

    @property
    def components(self):
        human_interventions = {}
        if self.et is None:
            # No /scenario/interventions/human section
            return {}
        for component in self.et.findall("component"):
            if component.find("ITN") is not None:
                human_interventions[component.attrib["id"]] = ITN(component)
            if component.find("GVI") is not None:
                human_interventions[component.attrib["id"]] = GVI(component)
            if component.find("MDA") is not None:
                human_interventions[component.attrib["id"]] = MDA(component)
            if component.find("TBV") is not None or component.find("PEV") is not None or component.find("BSV") is not None:
                human_interventions[component.attrib["id"]] = Vaccine(component)
        return human_interventions

    @property  # deployment
    def deployments(self):
        return Deployments(self.et)
    @deployments.setter
    def deployments(self, value):
        if self.et is None or value is None:
            return

        for deployment in self.et.findall("deployment"):
            self.et.remove(deployment)

        for deploy in value:
            if "xml" in deploy:
                # Preserve deployment section as is
                deployment = Deployment(None)
                deployment.create_from_xml(deploy["xml"])
                self.et.append(deployment.et)
                continue

            if "components" not in deploy or len(deploy["components"]) == 0:
                continue

            component_ids = [id for id in deploy["components"] if id in self.components]

            deployment_element = Element("deployment")

            if "name" in deploy:
                deployment_element.attrib["name"] = deploy["name"]

            deployment = Deployment(deployment_element)
            deployment.components = component_ids

            if "timesteps" in deploy:
                deployment.timesteps = deploy["timesteps"]
            if "continuous" in deploy:
                deployment.timesteps = deploy["continuous"]

            self.et.append(deployment.et)

    def __getitem__(self, item):
        """
        :rtype: Intervention
        """
        return self.components[item]

    def __getattr__(self, item):
        """
        :rtype: Intervention
        """
        return self.components[item]

    def __len__(self):
        return len(self.components)

    def __delitem__(self, key):
        for component in self.et.findall("component"):
            component_id = component.attrib["id"]
            if component_id == key:
                deployments_to_delete = []

                for deployment in self.deployments:
                    if deployment.delete_component(component_id) == 0:
                        # Prepare deployment for removal.
                        deployments_to_delete.append(deployment.et)

                for deployment_to_delete in deployments_to_delete:
                    self.et.remove(deployment_to_delete)

                self.et.remove(component)

                # TODO: Remove entire <human> section if this is the only component.

                return
        raise KeyError(key)

    def __iter__(self):
        """
        Iterator function. Allows using scenario.interventions.human in for statement
        i.e.
        for intervention in scenario.interventions.human:
           print intervention.name

        :rtype: Vector
        """
        if not self.components:
            return
        for intervention_name, intervention in self.components.items():
            yield intervention


class Anopheles(Section):
    """
    Mosquitos affected by VectorPop intervention

    https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#elt-anopheles
    """
    @property
    @attribute
    def mosquito(self):
        """
        Name of the affected anopheles-mosquito species.

        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#elt-anopheles
        """
        return "mosquito", str
    @mosquito.setter
    @attribute_setter(attrib_type=str)
    def mosquito(self, value):
        pass

    @property
    @tag_value
    def seekingDeathRateIncrease(self):
        return "seekingDeathRateIncrease", "initial", float
    @seekingDeathRateIncrease.setter
    @tag_value_setter(tag="seekingDeathRateIncrease", attrib="initial")
    def seekingDeathRateIncrease(self, value):
        pass

    @property
    @tag_value
    def probDeathOvipositing(self):
        return "probDeathOvipositing", "initial", float
    @probDeathOvipositing.setter
    @tag_value_setter(tag="probDeathOvipositing", attrib="initial")
    def probDeathOvipositing(self, value):
        pass

    @property
    @tag_value
    def emergenceReduction(self):
        return "emergenceReduction", "initial", float
    @emergenceReduction.setter
    @tag_value_setter(tag="emergenceReduction", attrib="initial")
    def emergenceReduction(self, value):
        pass

    @property
    def decays(self):
        section_names = ["seekingDeathRateIncrease", "probDeathOvipositing", "emergenceReduction"]
        decays = {}

        for section_name in section_names:
            section = self.et.find(section_name)

            if section is not None:
                decays[section_name] = Decay(section.find("decay"))

        return decays


class VectorPopIntervention(Section):
    """
    /scenario/intervention/vectorPop/intervention
    An intervention which may have various effects on the vector populations as a whole
    """
    @property
    def anopheles_xml_snippet(self):
        xml = """<anopheles mosquito="gambiae">
                    <emergenceReduction initial=".8">
                        <decay L="0.2465753424657534" function="step"/>
                    </emergenceReduction>
                 </anopheles>"""

        return xml

    def add_or_update_anopheles(self, params):
        et = None
        is_update = False
        desc = self.et.find("description")

        if desc is not None:
            for anopheles in desc.findall("anopheles"):
                if anopheles.attrib["mosquito"] == params["mosquito"]:
                    et = anopheles
                    is_update = True
                    break

        if et is None:
            et = ElementTree.fromstring(self.anopheles_xml_snippet)

        anopheles = Anopheles(et)

        if not is_update:
            anopheles.mosquito = str(params["mosquito"])

        default_decay_string = "<decay L='0.2465753424657534' function='step' />"
        new_decay_et = ElementTree.fromstring(default_decay_string)

        if "seekingDeathRateIncrease" in params and params["seekingDeathRateIncrease"] is not None:
            try:
                anopheles.seekingDeathRateIncrease = float(params["seekingDeathRateIncrease"])

                section = anopheles.et.find("seekingDeathRateIncrease")
                if section.find("decay") is None:
                    section.append(new_decay_et)
            except ValueError:
                pass
        if "probDeathOvipositing" in params and params["probDeathOvipositing"] is not None:
            try:
                anopheles.probDeathOvipositing = float(params["probDeathOvipositing"])

                section = anopheles.et.find("probDeathOvipositing")
                if section.find("decay") is None:
                    section.append(new_decay_et)
            except ValueError:
                pass
        if "emergenceReduction" in params and params["emergenceReduction"] is not None:
            try:
                anopheles.emergenceReduction = float(params["emergenceReduction"])

                section = anopheles.et.find("emergenceReduction")
                if section.find("decay") is None:
                    section.append(new_decay_et)
            except ValueError:
                pass

        if not is_update:
            if desc is None:
                new_description_element = ElementTree.Element("description")
                self.et.insert(0, new_description_element)
                desc = self.et.find("description")

            desc.append(anopheles.et)

    def remove_anopheles(self, name):
        desc = self.et.find("description")

        if desc is not None:
            for anopheles in desc.findall("anopheles"):
                if anopheles.attrib["mosquito"] == name:
                    desc.remove(anopheles)

        #TODO: Need to flag entire section for removal if empty.

    @property
    @attribute
    def name(self):  # name
        """
        Name of intervention (e.g. larviciding, sugar bait)
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#name-of-intervention-6
        rtype: str
        """
        return "name", str
    @name.setter
    @attribute_setter(attrib_type=str)
    def name(self, value):
        pass  # attribute_setter decorator will change name attribute

    @property
    def anopheles(self):
        """
        :rtype: Anopheles
        """
        list_of_anopheles = []
        desc = self.et.find("description")

        if desc is not None:
            for anopheles in desc.findall("anopheles"):
                list_of_anopheles.append(Anopheles(anopheles))

        return list_of_anopheles
    @anopheles.setter
    def anopheles(self, anopheles):
        desc = self.et.find("description")

        if desc is not None:
            for anoph in desc.findall("anopheles"):
                desc.remove(anoph) 

            for a in anopheles:
                assert isinstance(a, six.string_types)
                et = ElementTree.fromstring(a)
                anopheles = Anopheles(et)
                assert isinstance(anopheles.mosquito, six.string_types)
                if anopheles.seekingDeathRateIncrease is not None:
                    assert isinstance(anopheles.seekingDeathRateIncrease, float)
                if anopheles.probDeathOvipositing is not None:
                    assert isinstance(anopheles.probDeathOvipositing, float)
                if anopheles.emergenceReduction is not None:
                    assert isinstance(anopheles.emergenceReduction, float)
                desc.append(et)

    @property
    def timesteps(self):
        """
        Time-step at which this intervention occurs, starting from 0, the first intervention-period time-step.
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#-deploy-1
        rtype: list
        """
        timesteps = []
        timed = self.et.find("timed")

        if timed is not None:
            for deploy in timed.findall("deploy"):
                timesteps.append(deploy.attrib["time"])

        return timesteps


class VectorPop(Section):
    """
    /scenario/interventions/vectorPop
    Vector population intervention
    A list of parameterisations of generic vector host-inspecific interventions.
    https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#elt-vectorPop
    """
    def add(self, intervention, name=None):
        """
        Add an intervention to vectorPop section.
        intervention is either ElementTree or xml snippet
        """
        if self.et is None:
            return

        assert isinstance(intervention, six.string_types)
        et = ElementTree.fromstring(intervention)
        vector_pop = VectorPopIntervention(et)

        assert isinstance(vector_pop.name, six.string_types)

        if name is not None:
            assert isinstance(name, six.string_types)
            et.attrib["name"] = name

        index = len(self.et.findall("intervention"))
        self.et.insert(index, et)

    @property
    def interventions(self):
        """ Dictionary of interventions in /scenario/interventions/vectorPop section """
        interventions = {}
        if self.et is None:
            return interventions
        for intervention in self.et.findall("intervention"):
            interventions[intervention.attrib['name']] = VectorPopIntervention(intervention)
        return interventions

    def __len__(self):
        return len(self.interventions)

    def __delitem__(self, key):
        for intervention in self.et.findall("intervention"):
            if intervention.attrib["name"] == key:
                self.et.remove(intervention)
                # TODO: Remove entire <vectorPop> section if this is the only intervention.
                return

        raise KeyError(key)

    def __iter__(self):
        """
        Interator function. Allows using scenario.interventions.vectorPop in for statements
        for example:
        for interventions in scenario.interventions.vectorPop:
            print intervention.name
        :rtype: VectorPopIntervention
        """
        if len(self.interventions) == 0:
            return
        for intervention_name, intervention in self.interventions.items():
            yield intervention

    def __getitem__(self, item):
        """
        :rtype: VectorPopIntervention
        """
        return self.interventions[item]

    def __getattr__(self, item):
        """
        :rtype: VectorPopIntervention
        """
        return self.interventions[item]


class ImportedInfections(Section):
    @property
    @attribute
    def name(self):  # name
        """
        Name of imported infection.
        rtype: str
        """
        return "name", str
    @name.setter
    @attribute_setter(attrib_type=str)
    def name(self, value):
        pass  # attribute_setter decorator will change name attribute

    @property
    def period(self):
        timed = self.et.find("timed")

        try:
            return int(timed.attrib["period"])
        except KeyError:
            return 0
    @period.setter
    def period(self, value):
        timed = self.et.find("timed")

        if timed is None:
            timed_element = Element("timed")
            self.et.append(timed_element)
            timed = self.et.find("timed")

        timed.attrib["period"] = str(value)

    @property
    def rates(self):
        timed = self.et.find("timed")

        if timed is None:
            return

        rates = []

        for rate in timed.findall("rate"):
            rates.append({
                "time": int(rate.attrib["time"]),
                "value": int(rate.attrib["value"])
            })

        return rates
    @rates.setter
    def rates(self, value):
        if value is None or self.et is None:
            return

        timed = self.et.find("timed")

        if timed is None:
            timed_element = Element("timed")
            self.et.append(timed_element)
            timed = self.et.find("timed")

        for rate in timed.findall("rate"):
            timed.remove(rate)

        for rate in value:
            rate_element = Element("rate")
            rate_element.attrib["time"] = str(rate["time"])
            rate_element.attrib["value"] = str(rate["value"])
            timed.append(rate_element)
