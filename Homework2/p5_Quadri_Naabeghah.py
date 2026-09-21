import os
import sys
import tempfile
import unittest
from datetime import datetime


def read_observations(filename: str):
    """Read weather observations from a file.
    Args:
        filename: Name of input file.
    Returns:
        A pair (observations, errors), where observations maps each station
        to a list of (date, temperature) tuples sorted by date.
    """
    observations = {}
    errors = []
    seen = set()

    with open(filename, "r", encoding="utf-8") as input_file:
        lines = input_file.readlines()

    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            errors.append((line_number, "Malformed line"))
            continue

        parts = [part.strip() for part in raw_line.split(",")]
        if len(parts) != 3 or any(part == "" for part in parts):
            errors.append((line_number, "Malformed line"))
            continue

        station, date_string, temperature_string = parts

        try:
            date_value = datetime.strptime(date_string, "%I:%M:%S %p %m/%d/%Y")
        except ValueError:
            errors.append((line_number, "Invalid date"))
            continue

        try:
            temperature = float(temperature_string)
            if temperature < -100.0 or temperature > 150.0:
                raise ValueError
        except ValueError:
            errors.append((line_number, "Invalid temperature"))
            continue

        key = (station, date_value)
        if key in seen:
            errors.append((line_number, "Duplicate station/date combination"))
            continue

        seen.add(key)
        observations.setdefault(station, []).append((date_string, temperature))

    for station in observations:
        observations[station].sort(key=lambda item: datetime.strptime(item[0], "%I:%M:%S %p %m/%d/%Y"))

    return observations, errors


def station_statistics(observations):
    """Return min, max, and mean temperature for each station."""
    statistics = {}
    for station in sorted(observations):
        temperatures = [temperature for _, temperature in observations[station]]
        statistics[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures),
        }
    return statistics


def station_outliers(observations):
    """Return outlying stations using a dictionary comprehension."""
    statistics = station_statistics(observations)
    return {
        station: (readings[-1][0], readings[-1][1], statistics[station]["mean"])
        for station, readings in observations.items()
        if readings and readings[-1][1] > statistics[station]["mean"]
    }


def write_statistics(filename: str, statistics):
    """Write station statistics to a text file in lexicographic order."""
    with open(filename, "w", encoding="utf-8") as output_file:
        for station in sorted(statistics):
            values = statistics[station]
            output_file.write(
                "{}, {:.1f}, {:.1f}, {:.1f}\n".format(
                    station,
                    values["min"],
                    values["max"],
                    values["mean"],
                )
            )


def main() -> None:
    """Read observation data, print summaries, and write statistics."""
    if len(sys.argv) != 3:
        print("Usage: python p5_Quadri_Naabeghah.py <input_file> <output_file>")
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except OSError as error:
        print("Error reading file: {}".format(error))
        return

    statistics = station_statistics(observations)
    outliers = station_outliers(observations)

    print("Statistics:")
    for station in sorted(statistics):
        data = statistics[station]
        print(
            "{}: min={}, max={}, mean={}".format(
                station,
                "{:.1f}".format(data["min"]),
                "{:.1f}".format(data["max"]),
                "{:.1f}".format(data["mean"]),
            )
        )

    print("\nOutliers:")
    if outliers:
        for station in sorted(outliers):
            date_value, temperature, mean = outliers[station]
            print(
                "{}: ({}, {:.1f}, {:.1f})".format(
                    station,
                    date_value,
                    temperature,
                    mean,
                )
            )
    else:
        print("None")

    if errors:
        print("\nErrors:")
        for line_number, message in errors:
            print("{}: {}".format(line_number, message))

    try:
        write_statistics(output_filename, statistics)
    except OSError as error:
        print("Error writing file: {}".format(error))
        return


class TestWeatherStation(unittest.TestCase):
    def test_read_observations_multiple_stations_are_sorted_by_date(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as file:
            file.write("B, 09:00:00 AM 04/20/2026, 70.0\n")
            file.write("A, 08:00:00 AM 04/19/2026, 65.0\n")
            file.write("A, 09:00:00 AM 04/20/2026, 75.0\n")
            file.write("B, 08:30:00 AM 04/19/2026, 60.0\n")
            filename = file.name

        try:
            observations, errors = read_observations(filename)
            self.assertEqual(errors, [])
            self.assertEqual(observations["A"], [("08:00:00 AM 04/19/2026", 65.0), ("09:00:00 AM 04/20/2026", 75.0)])
            self.assertEqual(observations["B"], [("08:30:00 AM 04/19/2026", 60.0), ("09:00:00 AM 04/20/2026", 70.0)])
        finally:
            os.unlink(filename)

    def test_read_observations_allows_negative_temperatures_in_range(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as file:
            file.write("North, 07:00:00 AM 04/15/2026, -100.0\n")
            file.write("South, 07:05:00 AM 04/15/2026, -1.5\n")
            filename = file.name

        try:
            observations, errors = read_observations(filename)
            self.assertEqual(errors, [])
            self.assertEqual(observations["North"], [("07:00:00 AM 04/15/2026", -100.0)])
            self.assertEqual(observations["South"], [("07:05:00 AM 04/15/2026", -1.5)])
        finally:
            os.unlink(filename)

    def test_read_observations_rejects_duplicate_station_date(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as file:
            file.write("Alpha, 08:00:00 AM 04/19/2026, 40.0\n")
            file.write("Alpha, 08:00:00 AM 04/19/2026, 42.0\n")
            filename = file.name

        try:
            observations, errors = read_observations(filename)
            self.assertEqual(observations, {"Alpha": [("08:00:00 AM 04/19/2026", 40.0)]})
            self.assertEqual(len(errors), 1)
            self.assertIn("Duplicate", errors[0][1])
        finally:
            os.unlink(filename)

    def test_read_observations_rejects_invalid_temperature_ranges(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as file:
            file.write("Low, 08:00:00 AM 04/19/2026, -100.1\n")
            file.write("High, 09:00:00 AM 04/19/2026, 150.1\n")
            filename = file.name

        try:
            observations, errors = read_observations(filename)
            self.assertEqual(observations, {})
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("Invalid temperature" in message for _, message in errors))
        finally:
            os.unlink(filename)

    def test_station_statistics_calculates_min_max_and_mean(self):
        observations = {
            "Alpha": [("04/20/2026", 70.0), ("04/21/2026", 90.0), ("04/22/2026", 80.0)],
            "Beta": [("04/20/2026", 20.0), ("04/21/2026", 30.0)],
        }

        expected = {
            "Alpha": {"min": 70.0, "max": 90.0, "mean": 80.0},
            "Beta": {"min": 20.0, "max": 30.0, "mean": 25.0},
        }
        self.assertEqual(station_statistics(observations), expected)

    def test_station_outliers_uses_latest_temperature_and_mean(self):
        observations = {
            "Alpha": [("08:00:00 AM 04/19/2026", 50.0), ("08:00:00 AM 04/20/2026", 90.0)],
            "Beta": [("08:00:00 AM 04/19/2026", 40.0), ("08:00:00 AM 04/20/2026", 35.0)],
            "Gamma": [("08:00:00 AM 04/19/2026", 80.0)],
        }

        self.assertEqual(station_outliers(observations), {"Alpha": ("08:00:00 AM 04/20/2026", 90.0, 70.0)})

    def test_write_statistics_sorts_stations_and_formats_numbers(self):
        statistics = {
            "Gamma": {"min": 10.0, "max": 30.0, "mean": 20.0},
            "Alpha": {"min": 5.5, "max": 8.5, "mean": 7.0},
        }

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as file:
            filename = file.name

        try:
            write_statistics(filename, statistics)
            with open(filename, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
            self.assertEqual(lines, ["Alpha, 5.5, 8.5, 7.0", "Gamma, 10.0, 30.0, 20.0"])
        finally:
            os.unlink(filename)

    def test_read_observations_missing_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            read_observations("this_file_does_not_exist.txt")


if __name__ == "__main__":
    main()
