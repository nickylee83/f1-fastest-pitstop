# Myo Thet Tun 2918551

""" tyre class is to do all the functions for tyres """

# set constant values according to the requirements
INIT_FUEL = 105  # initial fuel is 105kg
BASE_LAP_TIME = 90 # Seconds
TOTAL_LAP = 60
FUEL_PER_LAP = 1.72 # kg
PIT_STOP_TIME = 24 # seconds

class tyre ():

    # initialise tyre setting according to tyre type
    def __init__(self, tyre_type):

        self.change_tyre(tyre_type)

        # reset the tyre setting according to tyre type
        self.reset()
        # other tyre setting must be the same as the primary tyre
        self.other_tyre_reset()

        # set fuel to 105kg
        self.fuel = INIT_FUEL

    # create own equal function. all initial parameters of two tyres must be the same
    def eq(self):
        if (self.init_grip == self.other_grip) and \
            (self.init_deg == self.other_deg) and \
            (self.init_switch_point == self.other_switch_point) and \
            (self.init_switch_deg == self.other_switch_deg):

            return True
        else:
            return False

    def add_lap(self, current_fuel):
        # fuel effect is current fuel divided by 6 times of initial fuel load and add 0.83
        fuel_effect = (current_fuel/(6 * INIT_FUEL)) + 0.83
        # linear phase, grip is subtracted by deg according to fuel effect
        if self.grip > self.switch_point:
            print("Linear phase")
            self.grip = self.grip - (self.deg * fuel_effect)

        # high wear phase, grip less than switch point, but more than minimum, need to change to higher deg
        elif (self.grip <= self.switch_point) and (self.grip > 0.2):
            print("High wear phase")
            self.grip = self.grip - (self.deg * self.switch_deg) * fuel_effect

        # less than 0.2, no grips (cannot be used)
        elif self.grip < 0.2:
            print("Cannot be used")
            self.grip = 0
        current_fuel -= FUEL_PER_LAP

    def calculate_lap_time(self, fuel):
        # start lap time is the base lap time
        self.lap_time = BASE_LAP_TIME
        # grip is OK, just subtract grip from lap time
        if self.grip >= 0.2:
            self.lap_time = self.lap_time - self.grip
        # grip is about to destroy itself, change a new one
        elif self.grip < 0.2:
            self.lap_time = self.lap_time + 2 # why we need to add 2 here? maybe, change a new tyre

        # if current fuel is full (105 kg), no subtraction from lap time
        if fuel == INIT_FUEL:
            self.lap_time = self.lap_time - (0 * fuel)
        # if no fuel, no lap time remain to go
        elif fuel == 0:
            self.lap_time = self.lap_time - 2
        # there is fuel, not full nor empty, lap time - 2 times fuel load (not very clear why I need to do it)
        elif fuel < INIT_FUEL and fuel > 0:
            self.lap_time = self.lap_time - (2 * fuel)
            # fuel should be subtracted itself by 1.72 after each lap

        return self.lap_time

    def change_tyre(self, tyre_type):
        # setting for soft tyre
        if tyre_type == 1:
            self.init_grip = 2.0
            self.init_deg = 0.02
            self.init_switch_point = 1.8
            self.init_switch_deg = 1.55
        # setting for medium tyre
        elif tyre_type == 2:
            self.init_grip = 1.5
            self.init_deg = 0.015
            self.init_switch_point = 1.3
            self.init_switch_deg = 1.3
        # setting for hard tyre
        else:
            self.init_grip = 1.0
            self.init_deg = 0.01
            self.init_switch_point = 0.8
            self.init_switch_deg = 1.25

        print("Tyre type = " + str(tyre_type))

    def reset(self):
        # reset all parameters to initial state
        self.grip = self.init_grip
        self.deg = self.init_deg
        self.switch_point = self.init_switch_point
        self.switch_deg = self.init_switch_deg

    def other_tyre_reset(self):
        # reset other tyre to initial state
        self.other_grip = self.init_grip
        self.other_deg = self.init_deg
        self.other_switch_point = self.init_switch_point
        self.other_switch_deg = self.init_switch_deg

class strategy ():

    def __init__(self, init_tyre, num_of_stops, pit_in_laps, pit_tyres):
        self.init_tyre = init_tyre
        self.num_of_stops = num_of_stops
        self.pit_in_laps = pit_in_laps
        self.pit_tyres = pit_tyres

        self.lap_time_array = list()
        for i in range (0, 59):
            self.lap_time_array.insert(0, 0)

        self.race_total = self.simulate_race()


    def is_valid_strategy(self):
        # the function returns true or false to check according to race rules

        # number of stops must be at least one
        if self.num_of_stops < 1:
            print ("There must be at least one pit stop.")
            return False

        # pit tyre list must have at least two elements and these two elements cannot be the same
        # (must use different compound types
        for i in range (0, (len(self.pit_in_laps) - 1)):
            # assume user input has at least two elements
            if (self.pit_tyres[i] == self.pit_tyres[i + 1]):
                print ("There should have at least two different types of pit tyres")
                return False
        # assume user types in at least two elements of the list
        # first stop cannot be in lap 0 and last stop cannot be in lap 59.
        if (self.pit_in_laps[0] == 0) or (self.pit_in_laps[len(self.pit_in_laps) - 1] == 59):
            print ("Pit stops cannot be in the first lap or last lap.")
            return False
        # laps for pit stop cannot overlap and the second pit must be after the first pit
        # (not in the reverse order)
        for i in range (0, (len(self.pit_in_laps) - 1)):
            if self.pit_in_laps[i] >= self.pit_in_laps[i + 1]:
                print ("Pit stop laps must increase monotonically.")
                return False

        # all of the above conditions are OK
        return True

    def simulate_race(self):
        # fit with initial tyres
        my_tyre = tyre(self.init_tyre)
        my_tyre.reset()
        my_tyre.other_tyre_reset()
        # clear lap time array
        for i in range (0, 59):
            self.lap_time_array[i] = 0
        # load the fuel 105kg
        fuel_load = my_tyre.fuel

        # set initial total race time
        total_race_time = 5

        # if one of the conditions in valid_strategy function is not met
        if self.is_valid_strategy() == False:
            print("This is not a valid race strategy.")
            total_race_time = 10000
            return total_race_time

        j = 0
        for i in range (0, 59):

            current_lap_time = my_tyre.calculate_lap_time(fuel_load)
            my_tyre.add_lap(fuel_load)

            total_race_time = total_race_time + current_lap_time

            if self.pit_in_laps[j] == i:
                # pit stop found in the lap, add 24 seconds
                print("Pit stop " + str(j) + " in lap " + str(i) + " *************************************")
                current_lap_time += 24

                # change tyres
                if self.pit_tyres[j] == 1:
                    my_tyre.change_tyre(1)
                elif self.pit_tyres[j] == 2:
                    my_tyre.change_tyre(2)
                else:
                    my_tyre.change_tyre(3)

                my_tyre.reset()
                my_tyre.other_tyre_reset()

                if j < (len(self.pit_in_laps) - 1):
                    j += 1

            self.lap_time_array[i] = current_lap_time

            # rounding decimal numbers
            total_race_time = round(total_race_time, 4)
            current_lap_time = round(current_lap_time, 4)
            my_grip = round(my_tyre.grip, 4)

            # display results
            print("\nLap: ", i, "\nLap Time: ", current_lap_time, "\nTotal Race Time: ", str(total_race_time))
            print("Tyre Grip: ", str(my_grip), "\nFuel Load: ", fuel_load)
        return total_race_time


    def choose_random_tyre(self):
        pass

    def change_compound(self):
        pass

    def change_lap(self):
        pass

    def move(self):
        pass

    def show_plot(self):
        pass

class strategy_annealer ():
    pass


def main():
    initial_tyre = 1
    number_of_stops = 2
    pit_stop_laps = [20, 40]
    pit_tyre_types = [1, 2]

    race = strategy(initial_tyre, number_of_stops, pit_stop_laps, pit_tyre_types)

    print("\nTotal Race Time: ", race.race_total, " seconds")


if __name__ == '__main__':
    main()
