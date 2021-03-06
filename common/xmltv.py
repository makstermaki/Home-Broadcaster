from datetime import datetime, date
from dateutil.parser import parse
import time
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element

# IMPORTANT NOTE: The XML TV file generated by this module doesn't include the XML TV
# standard specified header lines so the output technically isn't fully complaint.
# For practical purposes though the XML TV file is still usable though so this
# will be kept as is.


def generate_new_xmltv():
    return Element('tv')


def open_xmltv(xmltv_path):
    tree = ET.parse(xmltv_path)
    return tree.getroot()


# This function removes all programme nodes where the stop time is before the current time
def remove_past_programmes(root):
    children_to_remove = []
    for child in root:
        if child.tag == 'programme':
            stop_time = parse(child.attrib['stop'], fuzzy=True).timestamp()
            curr_time = int(time.time())
            if curr_time > stop_time:
                children_to_remove.append(child)
    for child in children_to_remove:
        root.remove(child)


def remove_channel_programmes(channel, root):
    children_to_remove = []
    for child in root:
        if (child.tag == 'programme' and
                child.attrib['channel'] == (channel + '.tv')):
            children_to_remove.append(child)
    for child in children_to_remove:
        root.remove(child)


def add_channel_if_not_exists(root, channel):
    for node in root.findall('channel'):
        if node.attrib['id'] == channel + '.tv':
            # Element already exists for the channel
            return

    channel_node = Element('channel')
    channel_node.attrib['id'] = channel + '.tv'
    display_node = Element('display-name')
    display_node.attrib['lang'] = 'en'
    display_node.text = channel + '.tv'
    channel_node.append(display_node)
    root.insert(0, channel_node)


def remove_channel(channel, root):
    channel_node = None
    for node in root.findall('channel'):
        if node.attrib['id'] == channel + '.tv':
            channel_node = node
            break
    root.remove(channel_node)


def add_programme(root, channel, start_time, stop_time, title, subtitle, desc):
    programme_node = Element('programme')
    programme_node.attrib['channel'] = channel + '.tv'
    programme_node.attrib['start'] = start_time
    programme_node.attrib['stop'] = stop_time

    title_node = Element('title')
    title_node.attrib['lang'] = 'en'
    title_node.text = title
    programme_node.append(title_node)

    subtitle_node = Element('sub-title')
    subtitle_node.attrib['lang'] = 'en'
    subtitle_node.text = subtitle
    programme_node.append(subtitle_node)

    desc_node = Element('desc')
    desc_node.attrib['lang'] = 'en'
    desc_node.text = desc
    programme_node.append(desc_node)

    root.append(programme_node)


def save_to_file(root, file_path):
    ElementTree(root).write(file_path)
