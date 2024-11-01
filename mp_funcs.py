# just the functions from the original main.py file, 
# with a few tweaks to make them more suited for multiprocessing life
# (mainly changes to what they print to the console)

import datetime # for datetime in dataset
from matplotlib import pyplot as plt
import numpy as np


def test_path(path: str):
    """
    Tests whether the given path is viable before we do any big computations
    """
    try:
        with open(path, "r") as f:
            pass
    except FileNotFoundError:
        print(f"Couldn't find file \"{path}\". Exiting...")
        exit(1)
    except PermissionError:
        print(f"Didn't have permission to read file \"{path}\". Exiting...")
        exit(1)



### read a big file using generators
def yield_line(path: str):
    """
    Yields one line from file at (path)
    """

    for line in open(path, "r"):
        yield line


### filter and process some of the data in that file
# ideas for the simple profile dataset in fake_data.txt:
#   average length of usernames... per sex...? - horizontal bar chart
#   ratio of email domains occurences (gmail, hotmail, yahoo, others?) - pie chart
#   spread of birth years - bar chart


## username length
def yield_username_len(path: str):
    """
    Yields the length of a username from file at (path). Each line is assumed to be dict-shaped
    """

    for line in open(path, "r"):
        d = eval(line)
        yield len(d["username"])

def yield_sex(path: str):
    """
    Yields the sex markers from file at (path). Each line is assumed to be dict-shaped
    """

    for line in open(path, "r"):
        d = eval(line)
        yield d["sex"]

def yield_username_len_and_sex(path: str):
    """
    Combo of yield_username_len() and yield_sex(). Faster than using them separately.
    """
    for line in open(path, "r"):
        d = eval(line)
        yield len(d["username"]), d["sex"]


## email domains
def yield_email_domain(path: str):
    """
    Yields the domain of an email address from file at (path). Each line is assumed to be dict-shaped
    """

    for line in open(path, "r"):
        d = eval(line)
        email = d["mail"]
        yield email[email.find("@"):email.find(".com")].strip("@") # i.e. email[10:16] => "@gmail".strip("@") => "gmail"


## birthyears
def yield_birthyear(path: str):
    """
    Yields a birthyear from file at (path). Each line is assumed to be dict-shaped, and 'birthdate' values must be datetime.date objects
    """

    for line in open(path, "r"):
        d = eval(line)
        yield d["birthdate"].year


### process data

## usernames
def avg_username_len_sex(path: str) -> dict[str, int]:
    """
    Calculates the average length of a username per sex in file at (path), assumed to contain dicts. Returns a dict of shape {(sex) : (average username length)}
    """

    f_sum = 0
    m_sum = 0
    f_count = 0
    m_count = 0
    gen = yield_username_len_and_sex(path)
    for num, sex in gen:
        if sex == "F":
            f_sum += num
            f_count += 1
        elif sex == "M":
            m_sum += num
            m_count += 1
        if (f_count + m_count) % 10000 == 0:
            print(f"usernames: processed {f_count + m_count} rows.")
    return dict(F=(f_sum / f_count), M=(m_sum / m_count))


## email domains
def email_domains_ratio(path: str) -> dict[str, int]:
    """
    Returns a dict in the shape of {'email domain name' : (number of occurences)} as found in the file at (path), assumed to contain dicts.
    """

    gen = yield_email_domain(path)
    d = {}
    progress = 0
    for domain in gen:
        if domain in d.keys():
            d[domain] += 1
        else:
            d[domain] = 1
        progress += 1
        if progress % 10000 == 0:
            print(f"                                        emails: processed {progress} rows.")
    return d


## birthyears
def birthyear_spread(path: str) -> dict[int, int]:
    """
    Returns a dict in the shape of {(birthyear) : (number of occurences)} as found in the file at (path), assumed to contain dicts.
    """

    gen = yield_birthyear(path)
    d = {}
    progress = 0
    for year in gen:
        if year in d.keys():
            d[year] += 1
        else:
            d[year] = 1
        progress += 1
        if progress % 10000 == 0:
            print(f"                                                                                birthyears: processed {progress} rows.")
    return dict(sorted(d.items())) # sort by year (key)


### visualize data (with matplotlib)

def make_usernames_plot(path: str):
    title = "Average length of username per sex"
    plt.figure(title)

    res = avg_username_len_sex(path)

    # make plot
    fig = plt.barh(y=res.keys(), width=res.values(), height=0.3, color="#9aaa32")
    plt.bar_label(fig, label_type="center", color="w")

    # scoot bars closer together
    b, t = plt.ylim()
    pad = 0.6
    plt.ylim(bottom=b-pad, top=t+pad)

    plt.suptitle(title)
    plt.show()


def make_emails_plot(path: str):
    title = "Users' email domains"
    plt.figure(title)

    res = email_domains_ratio(path)

    # variables for plot
    blue_grad = [("blue", 0.2), ("blue", 0.4), ("blue", 0.6)]
    txt_props = dict(color="b", backgroundcolor="w")
    cool_labels = [k.capitalize() for k in res.keys()]

    def pie_vals(pct, data):
        # quick and dirty to show values on pie chart nicely, from 
        # https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
        vals = list(data.values())
        a = int(np.round(pct/100.*np.sum(vals)))
        return f"{pct:.1f}%\n({a:d})"

    # make plot
    plt.pie(res.values(), labels=cool_labels, colors=blue_grad, autopct=lambda pct: pie_vals(pct, res), startangle=90, textprops=txt_props)
    plt.suptitle(title, color="b")
    plt.show()


def make_birthyears_plot(path: str):
    title = "Users' years of birth"
    plt.figure(title, figsize=(18, 6))

    res = birthyear_spread(path)

    # variables for plot
    rainbow = ["red", "orange", "yellow", "yellowgreen", "green", "xkcd:turquoise", "blue", "xkcd:purple", "orchid"]

    # make plot
    fig = plt.bar(x=res.keys(), height=res.values(), width=1.0, tick_label=res.keys(), color=rainbow)
    plt.bar_label(fig, label_type="center", rotation=90.0, fontsize="x-small")
    plt.tick_params(axis='x', labelrotation=90)

    plt.suptitle(title)
    plt.show()