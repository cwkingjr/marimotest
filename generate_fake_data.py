import random
from datetime import datetime, timedelta
import pytz


def get_random_assigneeidentity():
    assignees = [
        "alice",
        "bob",
        "charlie",
        "dave",
        "eve",
        "frank",
        "grace",
        "heidi",
        "ivan",
        "judy",
        "kathy",
        "larry",
        "mallory",
        "nina",
        "olivia",
        "peter",
        "quinn",
        "rachel",
        "steve",
        "trudy",
        "victor",
        "wendy",
        "xander",
        "yara",
        "zara",
    ]
    return random.choice(assignees)


def get_random_description():
    descriptions = [
        "This is a test description.",
        "Another example of a description.",
        "Randomly generated description for testing.",
        "Sample description for the request.",
        "This is a placeholder description.",
        "Description for testing purposes only.",
        "A brief description of the issue.",
        "Example description for demonstration.",
        "Test description to fill the field.",
        "Description generated for random data simulation.",
    ]
    return random.choice(descriptions)


def get_random_domain():
    domains = [
        "example.com",
        "test.com",
        "demo.com",
        "sample.com",
        "placeholder.com",
        "mockup.com",
        "fakedomain.com",
        "simulated.com",
        "randomdomain.com",
        "imaginary.com",
    ]
    return random.choice(domains)


def get_random_label():
    labels = [
        "GRMC-R",
        "GRMC-S",
        "GRMC-B",
    ]
    return random.choice(labels)


def get_random_submitteridentity():
    submitters = [f"submitter{x}" for x in range(1, 6)]
    return random.choice(submitters) + "@" + get_random_domain()


def get_random_requesteridentity():
    requesters = [f"requestor{x}" for x in range(1, 6)]
    return random.choice(requesters) + "@" + get_random_domain()


def get_random_datetime():
    """Gen a random date with timezone between now and 3 years ago."""
    timezone_name = "US/Central"
    # Create a tzinfo object from the timezone name
    tz = pytz.timezone(timezone_name)

    start_date = datetime.now(tz=tz) - timedelta(days=3 * 365)  # 3 years ago
    end_date = datetime.now(tz=tz)  # Now
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date


def get_random_priority():
    priorities = ["Low", "Medium", "High", "Critical"]
    return random.choice(priorities)


def get_random_severity():
    severities = list(range(1, 10))  # Severity levels from 1 to 9
    return random.choice(severities)


def get_random_shortid():
    return "V" + "".join(random.choices("12345678", k=8))


def get_random_title():
    us_state_abbreviations = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]

    us_state_names = [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]

    state_codes_names = us_state_abbreviations + us_state_names

    bracketed_prefixes = [
        "Legal Mail",
        "Bulk Forms",
        "DLS Only - DLS Imquiry",
        "Medical Paperwork Request/Clarification",
    ]

    unbrackeded_prefixes = [
        "TPA - WC External Comm: FW: blah blah",
    ]

    def get_random_line():
        if random.choice("0123456789") <= "8":  # ~80% chance to use a bracketed prefix
            return f"{random.choice(bracketed_prefixes)} [{random.choice(state_codes_names)}]"
        return (
            f"{random.choice(unbrackeded_prefixes)} {random.choice(state_codes_names)}"
        )

    return get_random_line()


def get_random_status():
    statuses = ["Assigned", "Work In Progress", "Resolved"]
    return random.choice(statuses)


def get_random_tags():
    tags = [
        "WHS",
        "HR",
        "PXT",
        "Sedgwick",
        "",  # Some tags are null/empty
        "Helmsman",
        '"Sedgwich,QACheck"',
        "AutoSimResolved",
    ]
    return random.choice(tags)


def get_random_nextstepaction():
    actions = [
        "Comment",
        "Placeholder-1",
        "Placeholder-2 ",
    ]
    return random.choice(actions)


def get_random_assignedfolderlabel():
    labels = [
        "Helmsman",
        "Sedgwick",
        "US WC",
        "Other",
        "GRMC Support: Tickets",
        "",  # empty
    ]
    return random.choice(labels)


def get_random_rank():
    ranks = ["1", "2", "3", "4", "5"]
    return random.choice(ranks)


def get_random_createandlastupdatedates():
    """Create these at the same time, so that the last update is always after the create date."""
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    good_date_order = False
    create_date = None
    last_updated_date = None

    while not good_date_order:
        create_date = get_random_datetime()
        last_updated_date = get_random_datetime()
        if create_date < last_updated_date:
            good_date_order = True

    return (
        create_date.strftime(DATE_FORMAT),
        last_updated_date.strftime(DATE_FORMAT),
    )


def get_random_tpa_from():
    return "TPA-" + str(random.choice(range(1, 11)))


def get_random_root_cause():
    return "Root cause " + str(random.randint(1, 21))


def print_examples():
    print("Random data formats:")
    create_date, last_update_date = get_random_createandlastupdatedates()
    print("assigned_folder_label:", get_random_assignedfolderlabel())
    print("assignee_identity:", get_random_assigneeidentity())
    print("create_date:", create_date)
    print("description:", get_random_description())
    print("domain:", get_random_domain())
    print("label:", get_random_label())
    print("last_updated_date:", last_update_date)
    print("next_step_action:", get_random_nextstepaction())
    print("priority:", get_random_priority())
    print("rank:", get_random_rank())
    print("requester_identity:", get_random_requesteridentity())
    print("resolved_by_identity:", get_random_assigneeidentity())
    print("root_cause:", get_random_root_cause())
    print("severity:", get_random_severity())
    print("shortid:", get_random_shortid())
    print("status:", get_random_status())
    print("submitter_identity:", get_random_submitteridentity())
    print("tags:", get_random_tags())
    print("title:", get_random_title())
    print("tpa_from:", get_random_tpa_from())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        num_rows = int(sys.argv[1])
        header_row = "Rank,Severity,ShortId,Title,Status,NextStepAction,CreateDate,LastUpdatedDate,AssignedFolderLabel,Labels,Description,RootCauses,Priority,Tags,AssigneeIdentity,ResolvedByIdentity,SubmitterIdentity,RequesterIdentity,tpa_from (string)"
        print(header_row)
        for _ in range(num_rows):
            create_date, last_update_date = get_random_createandlastupdatedates()
            row = (
                f"{get_random_rank()},"
                f"{get_random_severity()},"
                f"{get_random_shortid()},"
                f"{get_random_title()},"
                f"{get_random_status()},"
                f"{get_random_nextstepaction()},"
                f"{create_date},"
                f"{last_update_date},"
                f"{get_random_assignedfolderlabel()},"
                f"{get_random_label()},"
                f"{get_random_description()},"
                f"{get_random_root_cause()},"
                f"{get_random_priority()},"
                f"{get_random_tags()},"
                f"{get_random_assigneeidentity()},"
                f"{get_random_assigneeidentity()},"
                f"{get_random_submitteridentity()},"
                f"{get_random_requesteridentity()},"
                f"{get_random_tpa_from()}"
            )
            print(row)
    else:
        print(
            "No command line arguments provided. Generating one random data example per field."
        )
        print_examples()
        sys.exit(0)
