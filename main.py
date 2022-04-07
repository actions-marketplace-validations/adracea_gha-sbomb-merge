import xml.etree.ElementTree as ET
import os
import os.path
import glob


def main():
    act_ver = os.environ["INPUT_CDXVERSION"]  # "1.3"
    act_input = os.environ["INPUT_FILES"]  # "./bom*.xml"
    act_input2 = os.environ["INPUT_OFILE"]  # "finalBom.xml"
    ns = {"default": f"http://cyclonedx.org/schema/bom/{act_ver}"}
    files = glob.glob(act_input)
    print("Found the following files:")
    print(files)
    tree = ET.parse(files[0])
    rootComps = []
    rootTools = []
    rootMetaComps = []
    rootDeps = []
    for fil in files[1:]:
        root1 = []
        root2 = []
        root3 = []
        root4 = []
        if (ET.parse(fil).getroot().find("default:components", ns)) is None:
            root1 = []
        else:
            root1 = (
                ET.parse(fil)
                .getroot()
                .find("default:components", ns)
                .findall("default:component", ns)
            )
        if (ET.parse(fil).getroot().find("default:metadata", ns)) is None:
            root2 = []
        else:
            if (
                ET.parse(fil)
                .getroot()
                .find("default:metadata", ns)
                .find("default:tools", ns)
            ):
                pass
            else:
                root2 = (
                    ET.parse(fil)
                    .getroot()
                    .find("default:metadata", ns)
                    .find("default:tools", ns)
                    .findall("default:tool", ns)
                )
        if (ET.parse(fil).getroot().find("default:metadata", ns)) is None:
            root3 = []
        else:
            root3 = (
                ET.parse(fil)
                .getroot()
                .find("default:metadata", ns)
                .findall("default:component", ns)
            )
        if (ET.parse(fil).getroot().find("default:dependencies", ns)) is None:
            root4 = []
        else:
            root4 = (
                ET.parse(fil)
                .getroot()
                .find("default:dependencies", ns)
                .findall("default:dependency", ns)
            )
        rootComps.extend(root1)
        rootTools.extend(root2)
        rootMetaComps.extend(root3)
        rootDeps.extend(root4)
    for element in rootComps:
        tree.getroot().find("default:components", ns).append(element)
    for element in rootTools:
        tree.getroot().find("default:metadata", ns).find(
            "default:tools", ns
        ).append(element)
    for element in rootMetaComps:
        tree.getroot().find("default:metadata", ns).append(element)
    for element in rootDeps:
        tree.getroot().find("default:dependencies", ns).append(element)
    tree.write(f"./{act_input2}")
    strfile = ""
    with open(f"./{act_input2}") as file:
        strfile = file.read().replace("ns0:", "").replace(":ns0", "")
        strfile = '<?xml version="1.0" encoding="UTF-8"?>' + strfile
    with open(f"./{act_input2}", "w") as file:
        file.write(strfile)
    print(f"Finished merging SBOMs into {act_input2}")
    print(f"::set-output name=success::{act_input2}")


if __name__ == "__main__":
    main()
