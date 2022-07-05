"""This script is for the web-based optimizer."""

from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from fleet_classes import Offer, ComponentOffer
from fleet_offers import Component
from get_spot import SpotCalculator

# from gevent import monkey
# monkey.patch_all()  ##internal use- Prevent an Error "greenlet.error: cannot switch to a different thread"

calc = SpotCalculator()
app = Flask(__name__)
CORS(app)


@app.route("/getAWSData", methods=["POST"])
@cross_origin()
def get_aws_data_tojson():
    """Get AWS Data tab."""
    print("Extracting Data- Linux")
    aws_data_linux = calc.get_ec2_from_cache("all", "linux")
    print("Extracting Data- Windows")
    aws_data_windows = calc.get_ec2_from_cache("all", "windows")
    with open("ec2_data_Linux.json", "w", encoding="utf-8") as f:
        json.dump(aws_data_linux, f, ensure_ascii=False, indent=4)
    with open("ec2_data_Windows.json", "w", encoding="utf-8") as f:
        json.dump(aws_data_windows, f, ensure_ascii=False, indent=4)
    return jsonify()


## AWS Single Instance
@app.route("/getAWSPrices", methods=["POST"])
@cross_origin()
def get_AWS_prices():
    """Single instance tab."""
    if request.method == "POST":
        filter = request.get_json()
        return single_instance_search(filter, "AWS")
    else:
        return jsonify()


## Azure Single Instance
@app.route("/getAzurePrices", methods=["POST"])
@cross_origin()
def get_Azure_prices():
    """AWS Single instance tab."""
    if request.method == "POST":
        filter = request.get_json()
        return single_instance_search(filter, "Azure")
    else:
        return jsonify()


## Hybrid Single Instance
@app.route("/getHybridPrices", methods=["POST"])
@cross_origin()
def get_Hybrid_prices():
    """AWS Single instance tab."""
    if request.method == "POST":
        filter = request.get_json()
        return single_instance_search(filter, "Hybrid")
    else:
        return jsonify()


## AWS fleet search
@app.route("/getAWSFleet", methods=["POST"])
@cross_origin()
def get_AWS_fleet_prices():
    """AWS Fleet search tab."""
    if request.method == "POST":
        filter = request.get_json()
        return fleet_search(filter, "AWS")
    else:
        return jsonify()


## Azure fleet search
@app.route("/getAzureFleet", methods=["POST"])
@cross_origin()
def get_Azure_fleet_prices():
    """Azure Fleet search tab."""
    if request.method == "POST":
        filter = request.get_json()
        return fleet_search(filter, "Azure")
    else:
        return jsonify()


## Hybrid Cloud Search
@app.route("/getHybridCloudFleet", methods=["POST"])
@cross_origin()
def get_hybrid_cloud_fleet_prices():
    """Hybrid Cloud Fleet search tab."""
    if request.method == "POST":
        filter = request.get_json()
        return fleet_search(filter, "Hybrid")
    else:
        return jsonify()


def serialize_group(group: Offer):
    """Serialize group in fleet option."""
    res = dict()
    res["price"] = round(group.total_price, 5)
    res["instances"] = list(map(lambda i: serialize_instance(i), group.instance_groups))
    res["region"] = group.region
    return res


def serialize_instance(instance):
    """Lower level of serialize group in fleet option."""
    result = instance.instance.copy()
    result["spot_price"] = round(instance.instance["spot_price"], 5)
    result["priceAfterDiscount"] = round(instance.instance["spot_price"] * (1 - instance.instance["discount"] / 100), 5) if \
        instance.instance["discount"] != 0 else round(instance.instance["spot_price"],5)
    # result['CPU/Price_Score'] = round(instance.instance['score_cpu_price'],5)
    # result['Memory/Price_Score'] = round(instance.instance['score_memory_price'],5)
    result["components"] = list(
        map(lambda param: serialize_component(param), instance.components)
    )
    return result


def serialize_component(component: ComponentOffer):
    """Lower level of serialize group in fleet option."""
    result = dict()
    result["appName"] = component.app_name
    result["componentName"] = component.component_name
    return result


def fleet_search(filter, provider):
    shared_apps = []  # list of components of shared apps
    partitions = []  ## list of ALL components
    app_size = dict()  ##size of each app
    for i, a in enumerate(filter["apps"]):
        app_size[i] = len(a["components"])
        if "share" in a and a["share"] is True:
            for c in a["components"]:
                shared_apps.append(Component(i, a["app"], c))
        else:
            app = []
            for c in a["components"]:
                app.append(Component(i, a["app"], c))
            if len(app) > 0:
                partitions.append(app)
    if len(shared_apps) > 0:
        partitions.append(shared_apps)
    os = filter["selectedOs"]
    if provider != "Hybrid":
        region = filter["region"] if "region" in filter else "all"
    else:
        region = "hybrid"
    payment = "spot" if filter["payment"] == "Spot" else "onDemand"
    filter_instances = (
        filter["filterInstances"] if "filterInstances" in filter else "NA"
    )
    availability_zone = (
        filter["availability_zone"] if "availability_zone" in filter else "NA"
    )
    architecture = filter["architecture"] if "architecture" in filter else "all"
    type_major = filter["type_major"] if "type_major" in filter else "all"
    offers_list = calc.get_fleet_offers(
        os, region, app_size, partitions, payment, architecture, type_major, filter_instances, provider
    )  ##architecture and typemajor are 'all'
    res = list(map(lambda g: serialize_group(g), offers_list))
    with open("FleetECresults.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    return jsonify(res)


def single_instance_search(filter, provider):
    os = filter["selectedOs"]
    v_cpus = float(filter["vCPUs"])
    memory = float(filter["memory"])
    storage_size = float(filter["size"]) if "size" in filter else 0
    if provider != "Hybrid":
        region = filter["selectedRegion"] if "selectedRegion" in filter else "all"
    else:
        region = "hybrid"
    payment = "spot" if filter["payment"] == "Spot" else "onDemand"
    type = filter["type"] if "type" in filter else "all"
    behavior = filter["behavior"] if "behavior" in filter else "terminate"
    storage_type = (
        filter["storageType"]
        if "storageType" in filter and filter["storageType"] is not None
        else "all"
    )
    iops = (
        float(filter["iops"])
        if "iops" in filter and filter["iops"] is not None
        else 0
    )
    throughput = (
        float(filter["throughput"])
        if "throughput" in filter and filter["throughput"] is not None
        else 0
    )
    frequency = float(filter["frequency"]) if "frequency" in filter else 4
    network = float(filter["network"]) if "network" in filter else 0
    burstable = True
    if network > 0:
        burstable = filter["burstable"] is True if "burstable" in filter else False
    res = calc.get_spot_estimations(payment, provider, os, v_cpus, memory, storage_size, region, type, behavior,
                                    storage_type, iops, throughput, frequency, network, burstable)
    with open("SingleInstanceECresults.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    return jsonify(res)


if __name__ == "__main__":
    app.run()
