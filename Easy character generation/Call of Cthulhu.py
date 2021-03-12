from random import randrange, choice

def d6():
    return randrange(6) + 1

def warn():
    print("input not recognized")

class Player:
    def __init__(self):
        self.stats = {
            "str": (d6() + d6() + d6())*5,
            "con": (d6() + d6() + d6())*5,
            "siz": (d6() + d6() + 6)*5,
            "dex": (d6() + d6() + d6())*5,
            "app": (d6() + d6() + d6())*5,
            "int": (d6() + d6() + 6)*5,
            "pow": (d6() + d6() + d6())*5,
            "edu": (d6() + d6() + 6)*5
        }
        self.age = 0
        self.luck = 0
        self.hp = 0
        self.mov = 0
        self.build = 0
        self.dmg_bonus = ""
        self.best_jobs = []
        self.job_skill_points = 0
        self.display(False)

    def alter_stat(self, stat, amt, max=90):
        if self.stats[stat] + amt > max:
            if max == 99:
                self.stats[stat] = 99
            else:
                print(f"cannot bring {stat} score above 90")
                return False
        else:
            self.stats[stat] += amt
            return True

    def add_d6(self):
        if input("add a d6 to stats? (y/n)  ") == "y":
            if input("random or fair? (r/f)  ") == "r":
                bonus = d6()
            else:
                stat_vals = list(self.stats.values())
                stat_vals.sort()
                val = (530-sum(stat_vals)-.5*stat_vals[-1]-.25*stat_vals[-2]-.5*self.stats["pow"]+.5*self.stats["app"])/5
                # stat total, highest stats, and willpower are all important, appearance not as much
                bonus = round(val**(.75)) if val > 1 else 1
            print()
            p.display(False)
            print(f"rolled a {bonus}!")
            while bonus > 0:
                add_stat = input("pick stat to improve (str/con/siz/dex/app/int/pow/edu):  ")
                if add_stat in self.stats:
                    max_improvement = min([bonus, int((90-self.stats[add_stat])/5)])
                    try:
                        add_amt = 1 if max_improvement == 1 else int(input(f"select value (1-{max_improvement}) to improve {add_stat} by:  "))
                        if add_amt <= 0 or add_amt > bonus:
                            print(f"{add_amt} is outside of the range 1-{max_improvement}")
                        elif self.alter_stat(add_stat, add_amt*5):
                            bonus -= add_amt
                            if bonus > 0:
                                print("\nnew stats:")
                                self.display(False)
                                print(f"remaining bonus: {bonus}")
                    except ValueError:
                        warn()
                else:
                    warn()
        print()
        p.display(False)

    def check_age(self, prompt, min, max):
        try:
            age = int(input(prompt))
        except ValueError:
            warn()
            return self.check_age(prompt, min, max)
        if age < min or age > max:
            print(f"choose a value between {min} and {max}")
            return self.check_age(prompt, min, max)
        return age

    def edu_improvement(self, num_checks):
        num_successes = 0
        for i in range(num_checks):
            if randrange(100) >= self.stats["edu"]:
                num_successes += 1
                self.alter_stat("edu", randrange(10) + 1, max=99)
        s  = "" if num_checks == 1 else "s"
        es = "" if num_successes == 1 else "es"
        print(f"{num_checks} edu improvement check{s}, {num_successes} success{es}")

    def reduce(self, deduct):
        print(f"you must deduct {deduct} points from str, con, or dex (split across one, two, or all three)")
        for ability in ["str", "con"]:
            if deduct == 0:
                break
            amt = 0
            while True:
                try:
                    minimum = max([0, deduct-self.stats["dex"]]) if ability == "con" else 0
                    maximum = min([self.stats[ability], deduct])
                    amt = int(input(f"number of points to deduct from {ability}:  "))
                    if amt > maximum or amt < minimum:
                        print(f"{amt} is outside the range {minimum}-{maximum}")
                    elif self.alter_stat(ability, -1*amt):
                        deduct -= amt
                        break
                except ValueError:
                    warn()
        self.alter_stat("dex", -1*deduct)

    def set_age(self):
        if input("auto age? (y/n)  ") == "y":
            if self.stats["edu"] > 50 or self.stats["app"] >= 70:
                self.age = 15 + randrange(20)
            else:
                self.age = 40 + randrange(20)
            self.age += int((90-self.stats["pow"])**2*self.stats["int"]/20000)
            # more likely to not go insane = more likely to be re-used = want to be younger
            print("age:", self.age)
        elif input("random age? (y/n)  ") == "y":
            lower_bound = self.check_age("lower bound:  ", 15, 88)
            upper_bound = self.check_age("upper bound:  ", lower_bound+1, 89)
            self.age = randrange(upper_bound-lower_bound) + lower_bound
            print("age:", self.age)
        else:
            self.age = self.check_age("enter your age:  ", 15, 89)

        if self.age < 20:
            self.luck = max([(d6() + d6() + d6())*5, (d6() + d6() + d6())*5])
            if input("choose a score to deduct 5 points from (str/siz):  ") == "str":
                self.alter_stat("str", -5)
            else:
                self.alter_stat("siz", -5)
            self.alter_stat("edu", -5)
        else:
            self.luck = (d6() + d6() + d6())*5
            if self.age < 40:
                self.edu_improvement(1)
            elif self.age < 50:
                self.reduce(5)
                self.alter_stat("app", -5)
                self.edu_improvement(2)
                self.mov -= 1
            elif self.age < 60:
                self.reduce(10)
                self.alter_stat("app", -10)
                self.edu_improvement(3)
                self.mov -= 2
            elif self.age < 70:
                self.reduce(20)
                self.alter_stat("app", -15)
                self.edu_improvement(4)
                self.mov -= 3
            elif self.age < 80:
                self.reduce(40)
                self.alter_stat("app", -20)
                self.edu_improvement(4)
                self.mov -= 4
            else:
                self.reduce(80)
                self.alter_stat("app", -25)
                self.edu_improvement(4)
                self.mov -= 5

    def hp_mov_build(self):
        s = self.stats
        self.hp = int((s["siz"] + s["con"])/10)
        self.mov += 7 if s["dex"] < s["siz"] and s["str"] < s["siz"] \
               else 9 if s["dex"] > s["siz"] and s["str"] > s["siz"] \
               else 8
        thicc = s["str"] + s["siz"]
        self.build = -2 if thicc < 65 else -1 if thicc < 85 else 0 if thicc < 125 else 1 if thicc < 165 else 2
        damage_bonuses = ["-2", "-1", "0", "+1d4", "+1d6"]
        self.dmg_bonus = damage_bonuses[self.build+2]

    def decide_occupation(self):
        best_attributes = self.stats.copy()
        for stat in ["con", "siz", "int"]:
            best_attributes.pop(stat)
        best_value = max(best_attributes.values())
        to_pop = []
        for stat in best_attributes:
            if best_attributes[stat] < best_value:
                to_pop.append(stat)
        for stat in to_pop:
            best_attributes.pop(stat)
        jobs = {
            "antiquarian": ["edu"],
            "artist": ["pow", "dex"],
            "athlete": ["dex", "str"],
            "author": ["edu"],
            "clergy": ["edu"],
            "criminal": ["dex", "str"],
            "dilletante": ["app"],
            "doctor": ["edu"],
            "drifter": ["app", "dex", "str"],
            "engineer": ["edu"],
            "entertainer": ["app"],
            "farmer": ["dex", "str"],
            "hacker": ["edu"],
            "journalist": ["edu"],
            "lawyer": ["edu"],
            "librarian": ["edu"],
            "military officer": ["dex", "str"],
            "missionary": ["edu"],
            "musician": ["dex", "pow"],
            "parapsychologist": ["edu"],
            "pilot": ["dex"],
            "police detective": ["dex", "str"],
            "police officer": ["dex", "str"],
            "private investigator": ["dex", "str"],
            "professor": ["edu"],
            "soldier": ["dex", "str"],
            "tribe member": ["dex", "str"],
            "zealot": ["app", "pow"]
        }
        for job in jobs:
            is_best_job = False
            for attribute in jobs[job]:
                if attribute in best_attributes:
                    is_best_job = True
                    break
            if is_best_job:
                self.best_jobs.append(job)
        self.job_skill_points = 2*self.stats["edu"] + 2*best_value

    def display(self, everything=True):
        if not everything:
            for s in self.stats:
                print(f"{s}: {self.stats[s]}    1/2: {int(self.stats[s]/2)}    1/5: {int(self.stats[s]/5)}\n")
        else:
            print("\n\n\n\nfinal stats:\n")
            self.display(False)
            print("hit points:", self.hp, end="\n\n")
            print("sanity:", self.stats["pow"], end="\n\n")
            print("luck:", self.luck, end="\n\n")
            print("age:", self.age, end="\n\n")
            print("move rate:", self.mov, end="\n\n")
            print("build:", self.build, "\ndamage bonus:", self.dmg_bonus, end="\n\n")
            print("best occupation choices:", self.best_jobs[0], end="")
            for i in range(1, len(self.best_jobs)):
                print(",", self.best_jobs[i], end="")
            print("\n\noccupation skill points (if one of the above is picked):", self.job_skill_points)
            print("personal interest skill points:", self.stats["int"]*2)

    def generate_backstory(self):
        if input("\ngenerate backstory? (y/n)  ") == "y":
            ideology_beliefs = [
                "There is a higher power that you worship and pray to (e.g. Vishnu, Jesus Christ, Haile Selassie I).",
                "Mankind can do just fine without religions (e.g. staunch atheist, humanist, secularist).",
                "Science has all the answers. Pick a particular aspect of interest (e.g. evolution, cryogenics, space exploration).",
                "A belief in fate (e.g. karma, the class system, superstitious).",
                "Member of a society or secret society (e.g. Freemason, Women's Institute, Anonymous).",
                "There is evil in society that should be rooted out (e.g. drugs, violence, racism).",
                "The occult (e.g. astrology, spiritualism, tarot).",
                "Politics (e.g. conservative, socialist, liberal).",
                "\"Money is power, and I'm going to get all I can\" (e.g. greedy, enterprising, ruthless).",
                "Campaigner/Activist (e.g. feminism, equal rights, union power)."
            ]
            significant_people = [
                "Parent (e.g. mother, father, stepmother).",
                "Grandparent (e.g. maternal grandmother, paternal grandfather).",
                "Sibling (e.g. brother, half-brother, stepsister).",
                "Child (son or daughter).",
                "Partner (e.g. spouse, fiancé, lover).",
                "Person who taught you your highest occupational skill. Identify the skill and consider who taught you "
                "(e.g. a schoolteacher, the person you apprenticed with, your father).",
                "Childhood friend (e.g. classmate, neighbor, imaginary friend).",
                "A famous person. Your idol or hero. You may never have even met (e.g. film star, politician, musician).",
                "A fellow investigator in your game. Pick one or choose randomly.",
                "An NPC in the game. Ask the Keeper to pick one for you."
            ]
            significant_reasons = [
                "You are indebted to them (e.g. financially, they protected you through hard times, got you your first job).",
                "They taught you something (e.g. a skill, to love, to be a man).",
                "They give your life meaning (e.g. you aspire to be like them, you seek to be with them, you seek to make them happy).",
                "You wronged them and seek reconciliation "
                "(e.g. stole money from them, informed the police about them, refused to help when they were desperate).",
                "Shared experience (e.g. you lived through hard times together, you grew up together, you served in the war together).",
                "You seek to prove yourself to them (e.g. by getting a good job, by finding a good spouse, by getting an education).",
                "You idolize them (e.g. for their fame, their beauty, their work).",
                "A feeling of regret"
                "(e.g. you should have died in their place, you fell out over something you said, you didn't step up and help them when you had the chance).",
                "You wish to prove yourself better than them. They had a flaw (e.g. lazy, drunk, unloving).",
                "They have crossed you and you seek revenge (e.g. death of a loved one, your financial ruin, marital breakup).",
            ]
            meaningful_locations = [
                "Your seat of learning (e.g. school, university).",
                "Your hometown (e.g. rural village, market town, busy city).",
                "The place you met your first love (e.g. a music concert, on holiday, a bomb shelter).",
                "A place for quiet contemplation (e.g. the library, country walks on your estate, fishing).",
                "A place for socializing (e.g. gentleman's club, local bar, uncle's house).",
                "A place connected with your ideology/belief (e.g. parish church, Mecca, Stonehenge).",
                "The grave of a significant person (e.g. a parent, a child, a lover).",
                "Your family home (e.g. a country estate, a rented flat, the orphanage in which you were raised).",
                "The place you were the happiest in your life (e.g. the park bench where you first kissed, your university).",
                "Your workplace (e.g. the office, library, bank)."
            ]
            treasured_possessions = [
                "An item connected with your highest skill (e.g. expensive suit, false ID, brass knuckles).",
                "An essential item for your occupation (e.g. doctor's bag, car, lock picks).",
                "A memento from your childhood (e.g. comics, pocketknife, lucky coin).",
                "A memento of a departed person (e.g. jewelry, a photograph in your wallet, a letter).",
                "Something given to you by your Significant Person (e.g. a ring, a diary, a map).",
                "Your collection (e.g. bus tickets, stuffed animals, records).",
                "Something you found but you don't know what it is——you seek answers "
                "(e.g. a letter you found in a cupboard written in an unknown language, "
                "a curious pipe of unknown origin found among your late father's effects, a curious silver ball you dug up in your garden).",
                "A sporting item (e.g. cricket bat, a signed baseball, a fishing rod).",
                "A weapon (e.g. service revolver, your old hunting rifle, the hidden knife in your boot).",
                "A pet (e.g. a dog, a cat, a tortise)."
            ]

            print("\nideology/belief:", choice(ideology_beliefs))
            print("\nsignificant person:", choice(significant_people))
            print("reason:", choice(significant_reasons))
            print("\nmeaningful location:", choice(meaningful_locations))
            print("\ntreasured possesion:", choice(treasured_possessions))

p = Player()
p.set_age()
# p.add_d6()
p.hp_mov_build()
p.decide_occupation()
p.display()
p.generate_backstory()
