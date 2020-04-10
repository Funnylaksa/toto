########################################
"""
Aim: To find out what is the minimum tickets of lottery tickets bought that guarantees at least a group 7 win.
This means at least 3 numbers should match against the winning ticket.

Tried to increase coverage:
1) Uniform Distribution of numbers in tickets
2) Limit how many times a number can meet another number

But did not manage to find a solution lower than 163...

Odds of getting any prize is 1/53.6. But why are we not able to get a list of 54 tickets that can guarantee at least
a single group 7 win? 

Question of the day: Is there a link between the 2 variables?  
    1) Odds of getting any prize -> 1/53.6 
    2) Minimum tickets to buy to guarantee a group 7 win(3 matches) -> 163 tentatively
"""
#########################################
import random
import lotterywheel


def get_winning_ticket():
    """
    Generate winning ticket(6 digit + 1 additional number)
    :return: list   [[7, 14, 24, 41, 9, 34], 38]
    """
    num_list = list(range(1, 50))
    ticket = []
    full_ticket = []
    for _ in range(6):
        num = random.choice(num_list)
        ticket.append(num)
        num_list.remove(num)
    additional_num = random.choice(num_list)
    full_ticket.append(ticket)
    full_ticket.append(additional_num)
    return full_ticket


# print(get_winning_ticket())


def get_tickets(ticket_count):
    """
    Generate list of x(ticket_count) tickets - base template
    """
    tickets_list = []
    for _ in range(ticket_count):
        num_list = list(range(1, 50))
        ticket = []
        for _ in range(6):
            num = random.choice(num_list)
            ticket.append(num)
            num_list.remove(num)
        tickets_list.append(ticket)
    return tickets_list


# print(get_tickets(12))


def limit_to_x_meets(meet_count_list, ticket_list, x):
    """
    Checks if max times digit meet another digit is hit
    """
    for num in ticket_list:
        if meet_count_list.count(num) >= x:
            return True
    return False


def get_tickets_with_limits(ticket_count, meet_limit=0):
    """
    Generate list of x(ticket_count) tickets with criteria
    1) how many times a digit appear using num_count_dict
    2) meet_limit: max times each digit can meet another digit using meet_count_dict
    """
    num_count_dict = {}
    for num in range(1, 50):
        num_count_dict[num] = 0

    meet_count_dict = {}
    for num in range(1, 50):
        meet_count_dict[num] = []

    tickets_list = []

    for _ in range(ticket_count):
        ticket = []
        for _ in range(6):
            # Generate list of num from lowest counts in num_count_dict
            lowest_num_list = list(
                [num for num in num_count_dict.keys() if num_count_dict[num] == min(num_count_dict.values())])
            num = random.choice(lowest_num_list)

            # Choose new number if num already appear or meet limit has reached
            timeout_count = 0
            while num in ticket or limit_to_x_meets(meet_count_dict[num], ticket, meet_limit):
                lowest_num_list = list(
                    [num for num in num_count_dict.keys() if num_count_dict[num] == max(num_count_dict.values())])
                num = random.choice(lowest_num_list)
                # print(lowest_num_list, timeout_count)
                timeout_count += 1
                if timeout_count > 5:
                    timeout_count = 0
                    num = random.choice(list(num_count_dict.keys()))
                    # print('timeout:', num)

            # Add count after num confirmed
            num_count_dict[num] += 1
            ticket.append(num)
        tickets_list.append(ticket)

        # Populate meet_counts of each digit in ticket with other digits met
        for digit in ticket:
            other_nums = [x for x in ticket if x != digit]
            meet_count_dict[digit].extend(other_nums)
    print('num_count_dict:', (num_count_dict[1]))
    print('meet_count_dict:', (len(meet_count_dict[1])))
    return tickets_list


# print(get_tickets_with_limits(163, 4))


def get_win_count(trials, ticket_list):
    win_count_list = []
    for _ in range(trials):
        winning_ticket = get_winning_ticket()
        grp1 = grp2 = grp3 = grp4 = grp5 = grp6 = grp7 = 0

        for entry in ticket_list:
            matches = set(entry) & set(winning_ticket[0])
            if len(matches) == 3:
                if winning_ticket[1] in entry:
                    grp6 += 1
                else:
                    grp7 += 1
            elif len(matches) == 4:
                if winning_ticket[1] in entry:
                    grp4 += 1
                else:
                    grp5 += 1
            elif len(matches) == 5:
                if winning_ticket[1] in entry:
                    grp2 += 1
                else:
                    grp3 += 1
            elif len(matches) == 6:
                grp1 += 1
        sum_win_count = grp1 + grp2 + grp3 + grp4 + grp5 + grp6 + grp7
        win_count_list.append(sum_win_count)
    # print(win_count_list)
    print('No wins after {} tries?:'.format(trials), 0 in win_count_list)
    print('Number of times you do not even get a single win ', win_count_list.count(0))


if __name__ == "__main__":
    # Generate own list
    list_used = get_tickets_with_limits(300, 40)
    get_win_count(10000, list_used)

    # Using lottery wheel to get at least 1 win
    list_used = lotterywheel.list163num
    get_win_count(10000, list_used)
