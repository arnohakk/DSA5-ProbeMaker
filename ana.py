import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_pie(data2plot, ax, title):
    """Method to create a pie chart
    """
    colors = plt.get_cmap('Reds')(np.linspace(0.2, 0.7, len(data2plot)))
    ax.pie(data2plot, colors=colors, radius=4, center=(5, 5), labels=data2plot.index.values,
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
    ax.set(xlim=(0, 10), xticks=[], ylim=(0, 10), yticks=[])
    ax.title.set_text(title)


def plot_attr_probes(attr_probes):
    """ Method to create all plots relating to attribute probes
    """
    fig, ax = plt.subplots(1, 2, figsize=(15, 15))
    attr_count = attr_probes['attribute'].value_counts()
    plot_pie(attr_count, ax[0], 'Used Attributes')
    passed_count = attr_probes['passed'].value_counts()
    plot_pie(passed_count, ax[1], 'Passed')
    plt.show()


def plot_tal_probes(tal_probes):
    """ Method to create all plots relating to talent probes
    """
    fig, ax = plt.subplots(1, 2, figsize=(15, 15))
    tal_count = tal_probes['talent'].value_counts()
    plot_pie(tal_count, ax[0], 'Used talents')
    passed_count = tal_probes['passed'].value_counts()
    plot_pie(passed_count, ax[1], 'Passed')
    plt.show()


def plot_hits(data):
    """ Method to create all plots relating to taken and given hits
    """
    # Make pie charts
    fig, ax = plt.subplots(1, 4, figsize=(15, 15))
    title = data['event_type'][0]
    data_sc = data['source_class'].value_counts()
    plot_pie(data_sc, ax[0], title + ': Source')
    data_vic = data['victim'].value_counts()
    plot_pie(data_vic, ax[1], title + ': Victim')
    data_dea = data['dealer'].value_counts()
    plot_pie(data_dea, ax[2], title + ': Dealer')

    # Make histogram
    ax[3].hist(data['damage'])
    ax[3].title.set_text('Damage frequencies')

    plt.show()


# Get log data
f = open("probe.log", "r")
data = f.readlines()
f.close()

# Split data into event types
hits_taken = list()
hits_given = list()
tal_probes = list()
attr_probes = list()

for line in data:
    if "hit_taken" in line:
        line = line.split(';')
        hits_taken.append(line)
    elif "hit_given" in line:
        line = line.split(';')
        hits_given.append(line)
    elif 'tal_probe' in line:
        line = line.split(';')
        tal_probes.append(line)
    elif 'attr_probe' in line:
        line = line.split(';')
        attr_probes.append(line)

# Convert to pandas dataframes
colnames_hits_taken = ['date', 'event_type', 'victim', 'dealer', 'damage', 'source', 'source_class']
hits_taken = pd.DataFrame(hits_taken, columns=colnames_hits_taken)
colnames_hits_given = ['date', 'event_type', 'dealer', 'victim', 'damage', 'source', 'source_class']
hits_given = pd.DataFrame(hits_given, columns=colnames_hits_given)
colnames_tal_probes = ['date', 'event_type', 'performer', 'talent', 'values', 'Modifier', 'rolls', 'roll1', 'roll2',
                       'roll3', 'points_left', 'passed', 'meister', 'patz', 'mega_meister', 'mega_patz']
tal_probes = pd.DataFrame(tal_probes, columns=colnames_tal_probes)
colnames_attr_probes = ['date', 'event_type', 'performer', 'attribute', 'aalue', 'modifier', 'roll', 'result',
                        'passed', 'meister', 'patz']
attr_probes = pd.DataFrame(attr_probes, columns=colnames_attr_probes)

print(hits_taken)
print(hits_given)
print(attr_probes)

# Create plots
plot_attr_probes(attr_probes)
plot_tal_probes(tal_probes)
plot_hits(hits_taken)
plot_hits(hits_given)
